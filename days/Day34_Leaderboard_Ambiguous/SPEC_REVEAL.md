# SPEC REVEAL — open ONLY after your tests pass

The full rule set the "interviewer" had in mind. Compare against `spec_notes.md`; every rule you
didn't anticipate is a clarifying question you'd have needed to ask.

## Intended behavior
1. **add_score(player, score)** REPLACES the player's score (latest call wins) — it does not
   accumulate.
2. **top(n)** returns up to `n` player names, highest score first; ties broken by player name
   ascending. `n` larger than the population returns everyone.
3. **rank(player)** is 1-based with the highest score at rank 1. It uses **standard competition
   ranking**: `rank = 1 + (number of players with a strictly higher score)`. So two players tied for
   the top are both rank 1, and the next player is rank 3 (not 2).
4. **rank(unknown player)** raises `KeyError` — don't invent a score for someone who has none.
5. **top** on an empty leaderboard returns `[]`.

## Reconcile
- Did you assume replace vs. accumulate correctly? (Both are defensible — which is why you ask.)
- Did you anticipate standard competition ranking (tie → shared rank, gap after)?
- Did you decide unknown-player behavior before the test told you?
