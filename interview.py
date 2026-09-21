#!/usr/bin/env python3
"""Interactive mock-interview runner for the vibe-coding training program.

Usage:
    python3 interview.py                       # list days, pick one
    python3 interview.py Day6_Concurrency_Race # run a specific day

Each day folder contains an `interview.json` manifest:
{
  "title": "...",
  "difficulty": "L4 (mid-level)",
  "time_min": 50,
  "prompt": "the DELIBERATELY vague opening line the interviewer gives you",
  "test_cmd": "python3 -m pytest -q",          # run from inside the day folder
  "clarifications": [                            # revealed only when you ask
    {"keywords": ["edge", "empty"], "answer": "Good question — yes, handle empty input."}
  ],
  "hints": ["first nudge", "second, more direct nudge", "..."]
}

The runner never writes to your code or tests — only appends a session record to the day's
AI_LOG.md when you type `done`. It's a coach, not an autograder.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DAYS = os.path.join(HERE, "days")  # the coding-day folders live under days/


def _c(text: str, code: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


def bold(t): return _c(t, "1")
def dim(t): return _c(t, "2")
def cyan(t): return _c(t, "36")
def green(t): return _c(t, "32")
def yellow(t): return _c(t, "33")
def red(t): return _c(t, "31")


def find_days() -> list[str]:
    days = []
    for name in sorted(os.listdir(DAYS)):
        if os.path.isfile(os.path.join(DAYS, name, "interview.json")):
            days.append(name)
    return days


def pick_day() -> str | None:
    days = find_days()
    if not days:
        print(red("No day folders with interview.json found."))
        return None
    print(bold("\nAvailable interview days:\n"))
    for i, d in enumerate(days, 1):
        try:
            m = json.load(open(os.path.join(DAYS, d, "interview.json")))
            label = f"{m.get('title', d)}  {dim('· ' + m.get('difficulty', ''))}"
        except Exception:
            label = d
        print(f"  {bold(str(i))}. {d}\n     {label}")
    print()
    choice = input(bold("Pick a day (number or folder name): ")).strip()
    if choice.isdigit() and 1 <= int(choice) <= len(days):
        return days[int(choice) - 1]
    return choice if choice in days else None


def load_manifest(folder: str) -> dict | None:
    path = os.path.join(DAYS, folder, "interview.json")
    if not os.path.isfile(path):
        print(red(f"No interview.json in {folder}"))
        return None
    try:
        return json.load(open(path))
    except Exception as e:
        print(red(f"Could not read manifest: {e}"))
        return None


def match_clarification(question: str, clarifications: list[dict]) -> str | None:
    q = question.lower()
    q_tokens = set(t.strip("?.,!") for t in q.split())
    best, best_score = None, 0
    for c in clarifications:
        kws = [k.lower() for k in c.get("keywords", [])]
        score = sum(1 for k in kws if k in q or k in q_tokens)
        if score > best_score:
            best, best_score = c, score
    return best["answer"] if best and best_score > 0 else None


def run_tests(folder: str, test_cmd: str) -> bool:
    print(dim(f"\n$ {test_cmd}   (in {folder})\n"))
    try:
        proc = subprocess.run(
            test_cmd, shell=True, cwd=os.path.join(DAYS, folder),
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        print(red("Tests timed out (120s). If this is the perf day, you're still O(n^2)."))
        return False
    out = (proc.stdout or "") + (proc.stderr or "")
    tail = "\n".join(out.strip().splitlines()[-15:])
    print(tail)
    passed = proc.returncode == 0
    print(green("\n✓ all tests pass") if passed else red("\n✗ tests still failing"))
    return passed


def fmt_elapsed(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def debrief(folder: str, manifest: dict, elapsed: float, hints_used: int,
            questions_asked: int, last_pass: bool | None) -> None:
    print(bold("\n=== Interviewer debrief ===\n"))
    budget = manifest.get("time_min", 50)
    print(f"  Time: {fmt_elapsed(elapsed)}  (budget {budget} min)")
    print(f"  Clarifying questions asked: {questions_asked}")
    print(f"  Hints used: {hints_used}")
    print(f"  Tests: {'passing' if last_pass else 'not passing / not run'}\n")

    fb = []
    if questions_asked == 0:
        fb.append(red("• You never asked a clarifying question. In the real round that's the #1 "
                      "way to lose points — scope out loud before coding."))
    elif questions_asked >= 2:
        fb.append(green("• Good scoping — you clarified before diving in."))
    if hints_used == 0 and last_pass:
        fb.append(green("• Solved it without hints. Strong."))
    elif hints_used >= 3:
        fb.append(yellow("• Leaned on hints a lot — revisit this topic until you can drive it solo."))
    if last_pass and elapsed <= budget * 60:
        fb.append(green("• Under budget with passing tests. That's an on-site pass."))
    elif last_pass:
        fb.append(yellow("• Correct but over time — practice the pattern to build speed."))
    else:
        fb.append(red("• Tests aren't green yet. Don't stop here — finish the loop."))
    for line in fb:
        print("  " + line)

    print(bold("\nSelf-score (1–5), Enter to skip:"))
    scores = {}
    for metric in ["Scoping", "Prompt quality", "Verification", "Ownership", "Communication"]:
        val = input(f"  {metric}: ").strip()
        if val:
            scores[metric] = val

    record = [
        f"\n---\n## Interview session — {datetime.now():%Y-%m-%d %H:%M}",
        f"- Time: {fmt_elapsed(elapsed)} (budget {budget} min)",
        f"- Clarifying questions: {questions_asked} · Hints used: {hints_used}",
        f"- Tests passing at end: {bool(last_pass)}",
    ]
    if scores:
        record.append("- Self-score: " + ", ".join(f"{k} {v}" for k, v in scores.items()))
    log_path = os.path.join(DAYS, folder, "AI_LOG.md")
    try:
        with open(log_path, "a") as f:
            f.write("\n".join(record) + "\n")
        print(green(f"\nSession appended to {folder}/AI_LOG.md"))
    except Exception as e:
        print(red(f"Could not write AI_LOG.md: {e}"))


def run(folder: str) -> None:
    manifest = load_manifest(folder)
    if not manifest:
        return
    clarifications = manifest.get("clarifications", [])
    hints = list(manifest.get("hints", []))
    test_cmd = manifest.get("test_cmd", "python3 -m pytest -q")

    print(bold("\n" + "=" * 68))
    print(bold(f"  {manifest.get('title', folder)}"))
    print(f"  {dim(manifest.get('difficulty', ''))}  ·  budget {manifest.get('time_min', 50)} min")
    print(bold("=" * 68))
    print(cyan("\nInterviewer: ") + manifest.get("prompt", "(no prompt)"))
    print(dim("\nCommands: ask <question> · hint · test · time · done · quit"))
    print(dim("Tip: read the folder's README + code in your editor; drive the mock from here.\n"))

    start = time.time()
    hints_used = 0
    questions_asked = 0
    last_pass: bool | None = None

    while True:
        try:
            raw = input(bold("you> ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue
        cmd, _, arg = raw.partition(" ")
        cmd = cmd.lower()

        if cmd in ("quit", "exit"):
            print(dim("Left the session without a debrief. Come back and finish the loop."))
            return
        elif cmd == "ask":
            if not arg.strip():
                print(cyan("Interviewer: ") + "What would you like to clarify?")
                continue
            questions_asked += 1
            ans = match_clarification(arg, clarifications)
            if ans:
                print(cyan("Interviewer: ") + ans)
            else:
                print(cyan("Interviewer: ") +
                      "What's your instinct? State an assumption and I'll tell you if it's off.")
        elif cmd == "hint":
            if hints:
                hints_used += 1
                print(yellow(f"Hint {hints_used}: ") + hints.pop(0))
            else:
                print(dim("No more hints — you've got everything you need."))
        elif cmd == "test":
            last_pass = run_tests(folder, test_cmd)
        elif cmd == "time":
            print(dim(f"Elapsed {fmt_elapsed(time.time() - start)} / "
                      f"{manifest.get('time_min', 50)} min budget"))
        elif cmd == "done":
            debrief(folder, manifest, time.time() - start, hints_used, questions_asked, last_pass)
            return
        else:
            print(dim("Unknown command. Use: ask <q> · hint · test · time · done · quit"))


def main() -> None:
    folder = sys.argv[1] if len(sys.argv) > 1 else pick_day()
    if not folder:
        print(red("No day selected."))
        sys.exit(1)
    if not os.path.isdir(os.path.join(DAYS, folder)):
        print(red(f"No such folder: {folder}"))
        sys.exit(1)
    run(folder)


if __name__ == "__main__":
    main()
