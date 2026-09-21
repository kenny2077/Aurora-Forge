// Day 15 — resolve a user-supplied file path safely.
//
// Endpoint: GET /files?path=<user input>. It serves files out of a fixed base directory. The
// current code just joins the base and the user path, which lets an attacker escape the base with
// "../" or an absolute path ("/etc/passwd") — a classic path-traversal vulnerability.
//
// Make resolveUserFile return the absolute path ONLY when it stays inside baseDir; otherwise throw
// Error("unsafe path"). Keep the signature identical.
//
// Contract (see safe_path.test.ts):
//   - A normal relative file resolves to baseDir + path.
//   - "../" escapes, absolute paths, and sneaky "a/../../x" all THROW "unsafe path".
//   - Normalization that stays inside ("a/../b.txt" -> baseDir/b.txt) is allowed.
import path from "node:path";

export function resolveUserFile(baseDir: string, userPath: string): string {
  return path.join(baseDir, userPath);
}
