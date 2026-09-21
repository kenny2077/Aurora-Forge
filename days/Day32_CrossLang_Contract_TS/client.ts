// Day 32 — build the request body the Python server expects (see CONTRACT.md).
//
// The mobile TS client keeps drifting from the server's schema: it sends camelCase keys, the raw
// epoch-millisecond timestamp instead of an ISO string, unsorted tags, and drops `referrer` when
// it's null. Fix buildRequestBody so its output matches CONTRACT.md exactly.

export type User = {
  id: number;
  name: string;
  emailVerified: boolean;
  createdAtMs: number; // epoch milliseconds
  tags: string[];
  referrer: string | null;
};

export function buildRequestBody(user: User): Record<string, unknown> {
  const body: Record<string, unknown> = {
    userId: user.id,
    fullName: user.name,
    emailVerified: user.emailVerified,
    createdAt: user.createdAtMs,
    tags: user.tags,
  };
  if (user.referrer) body.referrer = user.referrer;
  return body;
}
