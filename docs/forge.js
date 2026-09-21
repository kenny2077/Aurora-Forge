/* Aurora Forge — shared motion + pixel field.
   One rAF loop drives everything scroll-linked; pixel fields only redraw when the
   cursor warms them or the page scrolls, so an idle page costs nothing. */
(function () {
  const RM = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const COARSE = matchMedia("(pointer: coarse)").matches;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const Forge = (window.Forge = {});

  /* ---------- smooth scroll (Lenis), native fallback ---------- */
  let lenis = null;
  if (!RM && window.Lenis) {
    lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 0.95, smoothWheel: true });
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }
  Forge.scrollTo = (target, offset) => {
    const el = typeof target === "string" ? document.querySelector(target) : target;
    if (!el) return;
    const off = offset == null ? -90 : offset;
    if (lenis) lenis.scrollTo(el, { offset: off, duration: 1.3 });
    else window.scrollTo({ top: el.getBoundingClientRect().top + scrollY + off, behavior: RM ? "auto" : "smooth" });
  };
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || a.getAttribute("href").length < 2) return;
    const t = document.querySelector(a.getAttribute("href"));
    if (t) { e.preventDefault(); Forge.scrollTo(t); }
  });

  /* ---------- colour helpers ---------- */
  const hex = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  const mix = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
  const EMBER = [hex("#ff8a3d"), hex("#ffb347"), hex("#ffd28a")];
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5].map((v) => (v + 0.5) / 16);
  const bayer = (x, y) => BAYER[(y & 3) * 4 + (x & 3)];
  const hash = (x, y) => { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); };
  const vnoise = (x) => { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return hash(i, 7) * (1 - u) + hash(i + 1, 7) * u; };

  /* ---------- PixelField: low-res buffer, nearest-neighbour upscale, ember heat under the cursor ---------- */
  const fields = [];
  class PixelField {
    constructor(canvas, opts) {
      this.c = canvas; this.ctx = canvas.getContext("2d");
      this.low = document.createElement("canvas"); this.lctx = this.low.getContext("2d");
      this.paint = opts.paint; this.cellFor = opts.cell; this.radius = opts.radius || 2.6; this.light = !!opts.light; this.bg = opts.bg ? hex(opts.bg) : null; this.decay = opts.decay || 0.86; this.mixHeat = !!opts.mixHeat || this.light;
      this.dirty = true; this.visible = true; this.last = null;
      this.resize();
      new ResizeObserver(() => { this.resize(); }).observe(canvas);
      new IntersectionObserver(([e]) => { this.visible = e.isIntersecting; if (this.visible) this.dirty = true; }).observe(canvas);
      fields.push(this);
    }
    resize() {
      const w = this.c.clientWidth, h = this.c.clientHeight;
      if (!w || !h) return;
      const dpr = Math.min(2, devicePixelRatio || 1);
      this.cell = this.cellFor(w, h);
      this.cols = Math.ceil(w / this.cell); this.rows = Math.ceil(h / this.cell);
      this.c.width = Math.round(w * dpr); this.c.height = Math.round(h * dpr);
      this.scale = this.cell * dpr;
      this.low.width = this.cols; this.low.height = this.rows;
      this.img = this.lctx.createImageData(this.cols, this.rows);
      this.base = new Float32Array(this.cols * this.rows * 3);
      this.heat = new Float32Array(this.cols * this.rows);
      this.repaint();
    }
    repaint(state) { this.paint(this.base, this.cols, this.rows, state); this.dirty = true; }
    warm(clientX, clientY) {
      const r = this.c.getBoundingClientRect();
      const x = (clientX - r.left) / this.cell, y = (clientY - r.top) / this.cell;
      if (x < -6 || y < -6 || x > this.cols + 6 || y > this.rows + 6) { this.last = null; return; }
      // stamp along the path so fast strokes leave a continuous trail
      const p = this.last || [x, y], steps = Math.max(1, Math.ceil(Math.hypot(x - p[0], y - p[1]) / 1.2));
      for (let s = 1; s <= steps; s++) this.stamp(p[0] + (x - p[0]) * s / steps, p[1] + (y - p[1]) * s / steps);
      this.last = [x, y]; this.dirty = true;
    }
    stamp(cx, cy) {
      const R = this.radius, x0 = Math.max(0, Math.floor(cx - R)), x1 = Math.min(this.cols - 1, Math.ceil(cx + R));
      const y0 = Math.max(0, Math.floor(cy - R)), y1 = Math.min(this.rows - 1, Math.ceil(cy + R));
      for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
        const d = Math.hypot(x + 0.5 - cx, y + 0.5 - cy) / R; if (d >= 1) continue;
        const i = y * this.cols + x, v = 1 - d * d * 0.9;
        if (v > this.heat[i]) this.heat[i] = Math.min(1, this.heat[i] * 0.35 + v * 0.8);
      }
    }
    frame() {
      if (!this.visible || !this.img) return;
      let hot = false; const H = this.heat;
      for (let i = 0; i < H.length; i++) if (H[i] > 0) { H[i] = H[i] < 0.08 ? 0 : H[i] * this.decay; hot = true; }
      if (!hot && !this.dirty) return;
      const d = this.img.data, B = this.base;
      for (let i = 0, n = H.length; i < n; i++) {
        let r = B[i * 3], g = B[i * 3 + 1], b = B[i * 3 + 2];
        const h = H[i];
        const isBg = this.bg && r === this.bg[0] && g === this.bg[1] && b === this.bg[2];
        if (h > 0.38 && !isBg) {
          const q = Math.ceil(h * 5) / 5; // quantised heat keeps the pixel look
          const e = q < 0.5 ? mix(EMBER[0], EMBER[1], q * 2) : mix(EMBER[1], EMBER[2], (q - 0.5) * 2);
          if (this.mixHeat) { const k = 0.72 + q * 0.28; r += (e[0] - r) * k; g += (e[1] - g) * k; b += (e[2] - b) * k; }
          else { const a = 0.55 + q * 0.4; // bright ember cells, no faint brown tail
            r = Math.min(255, r * (1 - a * 0.6) + e[0] * a); g = Math.min(255, g * (1 - a * 0.6) + e[1] * a); b = Math.min(255, b * (1 - a * 0.6) + e[2] * a); }
        }
        d[i * 4] = r; d[i * 4 + 1] = g; d[i * 4 + 2] = b; d[i * 4 + 3] = 255;
      }
      this.lctx.putImageData(this.img, 0, 0);
      const ctx = this.ctx; ctx.imageSmoothingEnabled = false;
      ctx.drawImage(this.low, 0, 0, this.cols * this.scale, this.rows * this.scale);
      // 1px seams at exact cell boundaries (works for fractional cell sizes)
      ctx.fillStyle = this.light ? "rgba(228,237,232,.55)" : "rgba(2,10,9,.38)";
      for (let x = 1; x <= this.cols; x++) ctx.fillRect(Math.round(x * this.scale) - 1, 0, 1, this.c.height);
      for (let y = 1; y <= this.rows; y++) ctx.fillRect(0, Math.round(y * this.scale) - 1, this.c.width, 1);
      this.dirty = false;
    }
  }
  Forge.PixelField = PixelField;
  if (!COARSE) addEventListener("pointermove", (e) => { for (const f of fields) f.warm(e.clientX, e.clientY); }, { passive: true });


  /* ---------- hand-authored 5x7 pixel font ---------- */
  const GLYPHS = {
    A: ".###.|#...#|#...#|#####|#...#|#...#|#...#", U: "#...#|#...#|#...#|#...#|#...#|#...#|.###.",
    R: "####.|#...#|#...#|####.|#.#..|#..#.|#...#", O: ".###.|#...#|#...#|#...#|#...#|#...#|.###.",
    F: "#####|#....|#....|####.|#....|#....|#....", G: ".###.|#...#|#....|#.###|#...#|#...#|.###.",
    E: "#####|#....|#....|####.|#....|#....|#####",
    0: ".###.|#...#|#...#|#...#|#...#|#...#|.###.", 1: "..#..|.##..|..#..|..#..|..#..|..#..|.###.",
    2: ".###.|#...#|....#|...#.|..#..|.#...|#####", 3: "####.|....#|....#|.###.|....#|....#|####.",
    4: "...#.|..##.|.#.#.|#..#.|#####|...#.|...#.", 5: "#####|#....|####.|....#|....#|#...#|.###.",
    6: "..##.|.#...|#....|####.|#...#|#...#|.###.", 7: "#####|....#|...#.|..#..|.#...|.#...|.#...",
    8: ".###.|#...#|#...#|.###.|#...#|#...#|.###.", 9: ".###.|#...#|#...#|.####|....#|...#.|.##..",
    "%": "##...|##..#|...#.|..#..|.#...|#..##|...##", " ": "...|...|...|...|...|...|..."
  };
  // returns {w, h, on(x,y)} bitmap for a string, 1px gap between glyphs
  function bitmap(str) {
    const rows = [...String(str).toUpperCase()].map((ch) => (GLYPHS[ch] || GLYPHS[" "]).split("|"));
    const w = rows.reduce((a, g) => a + g[0].length, 0) + Math.max(0, rows.length - 1);
    const grid = Array.from({ length: 7 }, () => new Array(w).fill(false));
    let ox = 0;
    rows.forEach((g) => { g.forEach((line, y) => { [...line].forEach((c, x) => { if (c === "#") grid[y][ox + x] = true; }); }); ox += g[0].length + 1; });
    return { w, h: 7, on: (x, y) => y >= 0 && y < 7 && x >= 0 && x < w && grid[y][x] };
  }
  Forge.pixelSVG = function (str, cls) {
    const b = bitmap(str); let d = "";
    for (let y = 0; y < 7; y++) for (let x = 0; x < b.w; x++) if (b.on(x, y)) d += `M${x} ${y}h1v1h-1z`;
    const NS = "http://www.w3.org/2000/svg", s = document.createElementNS(NS, "svg");
    s.setAttribute("viewBox", `0 0 ${b.w} 7`); s.setAttribute("shape-rendering", "crispEdges"); s.setAttribute("aria-hidden", "true");
    if (cls) s.setAttribute("class", cls);
    const p = document.createElementNS(NS, "path"); p.setAttribute("d", d); p.setAttribute("fill", "currentColor"); s.appendChild(p);
    return s;
  };
  // paints a bitmap string centred in the field; `pad` cells of margin
  Forge.bitmapPainter = function (str, opt) {
    const o = Object.assign({ bg: "#020a09", on: null, pad: 1 }, opt);
    const b = bitmap(str), BG = hex(o.bg), ON = o.on ? o.on.map(hex) : null;
    return function (buf, cols, rows) {
      const ox = o.left ? 0 : Math.floor((cols - b.w) / 2), oy = Math.floor((rows - 7) / 2);
      for (let y = 0; y < rows; y++) for (let x = 0; x < cols; x++) {
        const j = (y * cols + x) * 3, lit = b.on(x - ox, y - oy), u = (x - ox) / b.w, v = (y - oy) / 7;
        let c = BG;
        if (lit) {
          c = ON ? mix(ON[0], ON[1], v) : mix(mix(AUR[0], AUR[1], clamp(u * 1.8, 0, 1)), AUR[2], clamp(u * 1.8 - 0.8, 0, 1));
          if (!ON && !b.on(x - ox, y - oy - 1)) c = mix(c, [255, 255, 255], 0.22); // lit top edge: a pixel-art bevel
        }
        buf[j] = c[0]; buf[j + 1] = c[1]; buf[j + 2] = c[2];
      }
    };
  };
  Forge.bitmapWidth = (str) => bitmap(str).w;

  /* ---------- painters ---------- */
  const SKY = [[0, hex("#020a09")], [0.3, hex("#04160f")], [0.55, hex("#061a2a")], [0.8, hex("#05161a")], [1, hex("#030d0c")]];
  const skyAt = (v) => { for (let i = 1; i < SKY.length; i++) if (v <= SKY[i][0]) return mix(SKY[i - 1][1], SKY[i][1], (v - SKY[i - 1][0]) / (SKY[i][0] - SKY[i - 1][0])); return SKY[SKY.length - 1][1]; };
  const AUR = [hex("#3fe0c8"), hex("#3aa0e8"), hex("#8b7dff")];
  const STAR = hex("#d8f2ec"), RIDGE1 = hex("#041311"), RIDGE2 = hex("#020908");

  Forge.auroraPainter = function (opts) {
    const o = Object.assign({ top: 0.3, ridge: 0.8 }, opts);
    return function (buf, cols, rows, st) {
      const phase = (st && st.phase) || 0, glow = st && st.glow != null ? st.glow : 1;
      for (let y = 0; y < rows; y++) {
        const v = y / rows;
        for (let x = 0; x < cols; x++) {
          const u = x / cols, i = (y * cols + x) * 3;
          let c = skyAt(Math.min(1, (Math.floor(v * 18) + bayer(x, y) * 0.9) / 18));
          const hs = hash(x, y);
          if (v < o.ridge - 0.08 && hs > 0.993) c = mix(c, STAR, 0.08 + 0.26 * hash(y, x) * hash(y, x));
          // two ribbons; only scroll (phase) moves them
          let best = 0, tone = 0;
          for (let k = 0; k < 2; k++) {
            const yc = o.top + 0.075 * Math.sin(u * 5.6 + phase + k * 1.9) + 0.035 * Math.sin(u * 14.1 - phase * 1.3 + k)
              + (k ? 0.09 : 0);
            const th = 0.04 + 0.018 * Math.sin(u * 8.7 + phase * 0.8 + k * 2.1);
            let I = Math.exp(-Math.pow((v - yc) / th, 2)) * (0.6 + 0.4 * Math.sin(u * 6.9 + phase * 0.6 + k * 3));
            if (v > yc) I = Math.max(I, Math.exp(-(v - yc) / 0.07) * 0.26 * (0.5 + 0.5 * Math.sin(x * 0.45 + k)) * (k ? 0.6 : 1));
            I *= k ? 0.7 : 1;
            if (I > best) { best = I; tone = 0.5 + 0.5 * Math.sin(u * 7.7 + phase * 0.5 + k * 2.4); }
          }
          const lvl = Math.floor(best * glow * 4 + bayer(x, y) * 0.8) / 4;
          if (lvl > 0) {
            const t = Math.min(2, Math.floor(tone * 3));
            c = mix(c, AUR[t], Math.min(0.92, lvl * 0.85));
          }
          const r1 = o.ridge + 0.05 * vnoise(u * 4 + 2) + 0.03 * vnoise(u * 13);
          const r2 = o.ridge + 0.1 + 0.045 * vnoise(u * 6 + 9) + 0.02 * vnoise(u * 21);
          if (v > r2) c = RIDGE2; else if (v > r1) c = RIDGE1;
          buf[i] = c[0]; buf[i + 1] = c[1]; buf[i + 2] = c[2];
        }
      }
    };
  };

  Forge.textPainter = function (text, opt) {
    const o = Object.assign({ bg: "#020a09", dot: "#0a1f1b", on: null, center: false }, opt);
    const tc = document.createElement("canvas"), tx = tc.getContext("2d", { willReadFrequently: true });
    const BG = hex(o.bg), DOT = hex(o.dot), ON = o.on ? o.on.map(hex) : null;
    return function (buf, cols, rows) {
      tc.width = cols; tc.height = rows;
      tx.clearRect(0, 0, cols, rows); tx.fillStyle = "#fff"; tx.textBaseline = "alphabetic";
      let size = rows * 1.02; tx.font = `800 ${size}px "Big Shoulders Display", Impact, sans-serif`;
      const w = tx.measureText(text).width; if (w > cols * 0.98) { size *= (cols * 0.98) / w; tx.font = `800 ${size}px "Big Shoulders Display", Impact, sans-serif`; }
      tx.textAlign = o.center ? "center" : "left"; tx.fillText(text, o.center ? cols / 2 : 0, rows * 0.86);
      const a = tx.getImageData(0, 0, cols, rows).data;
      for (let y = 0; y < rows; y++) for (let x = 0; x < cols; x++) {
        const j = y * cols + x, on = a[j * 4 + 3] > 110, u = x / cols, v = y / rows;
        let c;
        if (on) c = ON ? mix(ON[0], ON[1], clamp(v * 1.2 - 0.1, 0, 1)) : mix(mix(AUR[0], AUR[1], clamp(u * 1.6, 0, 1)), AUR[2], clamp(u * 1.6 - 0.6, 0, 1));
        else c = (x + y) % 2 ? BG : DOT;
        buf[j * 3] = c[0]; buf[j * 3 + 1] = c[1]; buf[j * 3 + 2] = c[2];
      }
    };
  };

  /* ---------- hero field + wordmark wiring ---------- */
  let hero = null, heroInner = null, heroEl = null, heroExtras = [];
  Forge.initHero = function (sel, opts) {
    heroEl = document.querySelector(sel); if (!heroEl) return;
    heroInner = heroEl.querySelector(".hero-inner"); heroExtras = [...heroEl.querySelectorAll(".try,.scroll-cue")];
    const canvas = heroEl.querySelector("canvas.field");
    const painter = Forge.auroraPainter(opts);
    hero = new PixelField(canvas, { paint: painter, radius: 3.4, decay: 0.9, cell: (w) => (w < 700 ? 9 : w < 1200 ? 11 : 13) });
    // single orchestrated load moment: the aurora ignites once
    if (!RM) {
      const t0 = performance.now();
      const ignite = (t) => { const k = clamp((t - t0) / 1400, 0, 1); hero.repaint({ phase: heroPhase(), glow: 1 - Math.pow(1 - k, 3) }); if (k < 1) requestAnimationFrame(ignite); };
      requestAnimationFrame(ignite);
    }
  };
  const heroPhase = () => scrollY * 0.0026;
  Forge.initWordmark = function (canvas, text) {
    if (!canvas) return;
    const w0 = Forge.bitmapWidth(text);
    new PixelField(canvas, { paint: Forge.bitmapPainter(text, { left: true }), radius: 2.6, decay: 0.9, bg: "#020a09", mixHeat: true,
      cell: (w) => { const c = w / w0; canvas.style.height = Math.round(c * 7) + "px"; return c; } });
  };
  Forge.initNumerals = function (sel) {
    document.querySelectorAll(sel).forEach((cv) => new PixelField(cv, {
      paint: Forge.bitmapPainter(cv.dataset.text, { bg: "#e4ede8", on: ["#062520", "#0f6f62"] }), bg: "#e4ede8",
      cell: (w, h) => Math.max(6, Math.floor(Math.min(w / 7, h / 9))), radius: 2.4, light: true }));
  };

  /* ---------- scroll-linked effects ---------- */
  const statements = [], stacks = [];
  Forge.initStatement = function (sectionSel) {
    const s = document.querySelector(sectionSel); if (!s) return;
    const p = s.querySelector("p");
    const words = [];
    const walk = (node, hot) => {
      [...node.childNodes].forEach((n) => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            const w = document.createElement("span"); w.className = "w" + (hot ? " hot" : ""); w.textContent = part;
            words.push(w); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) walk(n, hot || n.tagName === "EM");
      });
    };
    walk(p, false);
    statements.push({ s, words, lit: -1 });
  };
  Forge.initStack = function (sel) { const els = [...document.querySelectorAll(sel)]; if (els.length) stacks.push(els); };

  const nav = document.querySelector(".nav");
  function onScroll() {
    const y = scrollY, vh = innerHeight;
    if (nav) {
      nav.classList.toggle("solid", y > 24);
      const probe = (parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--nav-h")) || 64) + 6;
      let onPaper = false;
      document.querySelectorAll(".paper").forEach((p) => { const r = p.getBoundingClientRect(); if (r.top <= probe && r.bottom >= probe) onPaper = true; });
      document.body.classList.toggle("on-paper", onPaper);
    }
    if (hero && y < vh * 1.3) {
      hero.repaint({ phase: heroPhase(), glow: 1 });
      if (heroInner && !RM) { heroInner.style.transform = `translate3d(0,${(y * 0.32).toFixed(1)}px,0)`; heroInner.style.opacity = clamp(1 - y / (vh * 0.5), 0, 1).toFixed(3);
        for (const x of heroExtras) { x.style.opacity = heroInner.style.opacity; x.style.transform = `translate3d(0,${(y * 0.18).toFixed(1)}px,0)`; } }
    }
    for (const st of statements) {
      const r = st.s.getBoundingClientRect();
      const prog = clamp(-r.top / Math.max(1, r.height - vh), 0, 1);
      const lit = RM ? st.words.length : Math.floor(prog * 1.12 * st.words.length);
      if (lit !== st.lit) { st.words.forEach((w, i) => w.classList.toggle("lit", i < lit)); st.lit = lit; }
    }
    if (!RM) for (const els of stacks) {
      if (innerWidth <= 760) { els.forEach((e) => (e.style.transform = "")); continue; }
      els.forEach((e, i) => {
        const nx = els[i + 1]; if (!nx) { e.style.transform = ""; return; }
        const a = e.getBoundingClientRect(), b = nx.getBoundingClientRect();
        const cover = clamp((a.bottom - b.top) / a.height, 0, 1);
        e.style.transform = cover ? `scale(${(1 - cover * 0.05).toFixed(4)})` : "";
        e.style.filter = cover ? `brightness(${(1 - cover * 0.12).toFixed(3)})` : "";
      });
    }
  }
  const pageEl = document.querySelector(".page"), footEl = document.querySelector(".site-footer");
  const markEl = footEl && footEl.querySelector(".mark-wrap");
  function footerReveal() {
    if (!pageEl || !markEl) return;
    const t = clamp((innerHeight - pageEl.getBoundingClientRect().bottom) / footEl.offsetHeight, 0, 1);
    const k = RM ? 1 : clamp((t - 0.35) / 0.5, 0, 1);
    markEl.style.opacity = k.toFixed(3); markEl.style.transform = `translate3d(0,${((1 - k) * 40).toFixed(1)}px,0)`;
  }
  let lastY = -1;
  function loop() {
    if (scrollY !== lastY) { lastY = scrollY; onScroll(); footerReveal(); }
    for (const f of fields) f.frame();
    requestAnimationFrame(loop);
  }
  addEventListener("resize", () => { lastY = -1; });
  requestAnimationFrame(loop);

  /* ---------- cursor light on options / rows (local, CSS-driven) ---------- */
  if (!COARSE) document.addEventListener("pointermove", (e) => {
    const t = e.target.closest && e.target.closest(".opt,.day");
    if (!t) return;
    const r = t.getBoundingClientRect();
    t.style.setProperty("--mx", (e.clientX - r.left) + "px"); t.style.setProperty("--my", (e.clientY - r.top) + "px");
  }, { passive: true });

  /* ---------- pixel tally strip helper ---------- */
  Forge.cells = function (host, n) { host.innerHTML = ""; for (let i = 0; i < n; i++) host.appendChild(document.createElement("i")); return [...host.children]; };
  Forge.stopScroll = (on) => { if (lenis) on ? lenis.stop() : lenis.start(); };
})();
