// Day 24 — trie-backed autocomplete.
//
// Powers the search box's suggestions. `insert` is done; implement `suggest` so the box can offer
// completions for a prefix.
//
// Contract (see trie.test.ts):
//   insert(word)               -> add a word (inserting the same word twice is a no-op / dedup).
//   suggest(prefix, limit)     -> up to `limit` inserted words that START WITH prefix, returned in
//                                 ascending lexicographic order.
//                                 - The prefix itself counts if it was inserted as a word.
//                                 - An empty prefix matches every word.
//                                 - No matches -> [].

type TrieNode = {
  children: Map<string, TrieNode>;
  isWord: boolean;
};

function makeNode(): TrieNode {
  return { children: new Map(), isWord: false };
}

export class Trie {
  root: TrieNode = makeNode();

  insert(word: string): void {
    let node = this.root;
    for (const ch of word) {
      if (!node.children.has(ch)) node.children.set(ch, makeNode());
      node = node.children.get(ch)!;
    }
    node.isWord = true;
  }

  suggest(prefix: string, limit: number): string[] {
    throw new Error("not implemented: walk to the prefix node, then collect words in order");
  }
}
