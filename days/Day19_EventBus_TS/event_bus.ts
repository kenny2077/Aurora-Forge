// Day 19 — a tiny event bus (pub/sub).
//
// Used across the app to decouple modules. Two bugs reported:
//   1. If a handler unsubscribes another handler while an event is being emitted, that other
//      handler gets skipped in the SAME emit (listeners are iterated live).
//   2. once() never actually fires "once" — it behaves exactly like on() and fires every time.
//
// Fix emit and once to satisfy event_bus.test.ts. Keep the public API identical.
//
// Contract:
//   on(event, handler)   -> subscribe; returns an unsubscribe function.
//   emit(event, payload) -> call every handler that is subscribed AT THE START of this emit,
//                           each exactly once, with payload. Handlers subscribing/unsubscribing
//                           during the emit do not change who is called in THIS emit.
//   once(event, handler) -> fire the handler at most once, then auto-unsubscribe. Returns an
//                           unsubscribe function too (in case it's cancelled before firing).

type Handler = (payload: unknown) => void;

export class EventBus {
  handlers: Map<string, Handler[]> = new Map();

  on(event: string, handler: Handler): () => void {
    if (!this.handlers.has(event)) this.handlers.set(event, []);
    this.handlers.get(event)!.push(handler);
    return () => this.off(event, handler);
  }

  off(event: string, handler: Handler): void {
    const arr = this.handlers.get(event);
    if (!arr) return;
    const idx = arr.indexOf(handler);
    if (idx >= 0) arr.splice(idx, 1);
  }

  emit(event: string, payload: unknown): void {
    const arr = this.handlers.get(event);
    if (!arr) return;
    for (const handler of arr) {
      handler(payload);
    }
  }

  once(event: string, handler: Handler): () => void {
    return this.on(event, handler);
  }
}
