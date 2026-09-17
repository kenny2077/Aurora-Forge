// Day 22 — minimum meeting rooms.
//
// Given meeting time intervals [start, end) (end-EXCLUSIVE: a meeting ending at 10 and one starting
// at 10 can share a room), return the minimum number of rooms needed so no two overlapping meetings
// share a room. Scheduling says we're over-provisioning rooms — meetings that merely touch are
// being counted as conflicts.
//
// Fix minMeetingRooms to satisfy meeting_rooms.test.ts. Keep the signature.
//
// Contract:
//   - [] -> 0.
//   - Intervals are [start, end) with end exclusive; touching intervals do NOT conflict.
//   - Return the peak number of simultaneously-active meetings.

export function minMeetingRooms(intervals: [number, number][]): number {
  const n = intervals.length;
  const starts = intervals.map((i) => i[0]).sort((a, b) => a - b);
  const ends = intervals.map((i) => i[1]).sort((a, b) => a - b);

  let rooms = 0;
  let maxRooms = 0;
  let i = 0;
  let j = 0;
  while (i < n) {
    if (starts[i] <= ends[j]) {
      rooms++;
      i++;
    } else {
      rooms--;
      j++;
    }
    maxRooms = Math.max(maxRooms, rooms);
  }
  return maxRooms;
}
