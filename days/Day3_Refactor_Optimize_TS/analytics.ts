// Access-log analytics for the API gateway.
//
// Given raw access-log lines like:   "GET /api/users 200 12ms"
// compute how often each endpoint (the request path) is hit, and the top-N hottest endpoints.
//
// This works on a handful of lines in the unit tests, but on a real log file it is O(n^2)
// and it mis-orders ties. Fix both. Keep the exported signatures identical.

export function parseEndpoint(line: string): string | null {
  // "GET /api/users 200 12ms" -> "/api/users".  Malformed lines -> null.
  const parts = line.trim().split(/\s+/);
  if (parts.length < 2) return null;
  return parts[1];
}

export function endpointCounts(lines: string[]): Map<string, number> {
  const endpoints: string[] = [];
  for (const line of lines) {
    const e = parseEndpoint(line);
    if (e !== null) endpoints.push(e);
  }

  const counts = new Map<string, number>();
  for (const e of endpoints) {
    // Re-scans the whole endpoint list for every single endpoint -> O(n^2).
    const c = endpoints.filter((x) => x === e).length;
    counts.set(e, c);
  }
  return counts;
}

export function topEndpoints(lines: string[], n: number): string[] {
  const entries: [string, number][] = [...endpointCounts(lines).entries()];

  // Sorts by hit count descending, but has no tie-break rule, so endpoints with equal
  // counts come out in whatever order the Map happened to store them.
  entries.sort((a, b) => b[1] - a[1]);

  return entries.slice(0, n).map((e) => e[0]);
}
