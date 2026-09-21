// Day 7 — CSV field tokenizer.
//
// Part of an importer that ingests user-uploaded CSVs. The current implementation just splits on
// commas, which is fine until a real spreadsheet shows up: quoted fields that contain commas,
// escaped quotes ("" inside a quoted field), and surrounding quotes that need to be stripped.
//
// Make parseCsvLine handle a single CSV record per the tests. Keep the signature identical.
//
// Rules (RFC-4180-ish):
//   - Fields are comma-separated.
//   - A field MAY be wrapped in double quotes; inside quotes, commas are literal text.
//   - Inside a quoted field, "" is an escaped literal double-quote character.
//   - The wrapping quotes are removed from the returned value.
//   - Empty fields are allowed; a trailing comma yields a trailing empty field.
//   - Whitespace is significant (do not trim).

export function parseCsvLine(line: string): string[] {
  // Naive: works only when no field contains a comma or a quote.
  return line.split(",");
}
