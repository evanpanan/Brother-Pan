#!/usr/bin/env python3
"""Search the small metadata index without reading all source/assets."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def search(query, limit=8):
    words = query.lower().split()
    rows = json.loads((ROOT / 'assets/registry.json').read_text())['assets']
    hits = []
    for row in rows:
        corpus = ' '.join(str(row.get(k, '')) for k in ['id', 'tags', 'description', 'kind']).lower()
        score = sum(word in corpus for word in words)
        if score:
            hits.append((score, row))
    return [row for _, row in sorted(hits, key=lambda x: (-x[0], x[1]['id']))[:limit]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='+')
    parser.add_argument('--limit', type=int, default=8)
    args = parser.parse_args()
    print(json.dumps(search(' '.join(args.query), args.limit), ensure_ascii=False, indent=2))
