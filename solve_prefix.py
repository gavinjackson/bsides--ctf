#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import multiprocessing as mp
from base64 import b64encode
from collections import Counter
import argparse
from typing import List, Tuple


# Provided column bags (top-of-board vertical lists), one list per column 1..9
COLUMNS = [
    ['I', 'D', 'S', 'O', 'M', 'H', 'E', 'A', 'R', 'B', 'N', 'C'],  # col1
    ['A', 'S', 'A', 'D', 'I', 'B', 'E', 'R', 'N', 'A', 'F', 'A', 'S', 'C'],  # col2
    ['I', 'K', 'R', 'E', 'D', 'S', 'N', 'A', 'T', 'U', 'B', 'C'],  # col3
    ['D', 'D', 'S', 'B', 'R', 'B', 'W', 'N', 'E', 'A', 'E', 'I', 'C'],  # col4
    ['D', 'R', 'I', 'B', 'U', 'S', 'H', 'O', 'N', 'C', 'O', 'A', 'E'],  # col5
    ['I', 'N', 'K', 'I', 'R', 'E', 'M', 'A', 'D', 'R', 'N', 'B', 'S', 'C'],  # col6
    ['D', 'I', 'E', 'U', 'B', 'C', 'D', 'E', 'S', 'A', 'N', 'D', 'R', 'C'],  # col7
    ['R', 'A', 'E', 'S', 'H', 'S', 'E', 'N', 'D', 'I', 'B', 'C'],  # col8
    ['S', 'B', 'R', 'S', 'I', 'D', 'A', 'E', 'A', 'T', 'N', 'C'],  # col9
]

# From index.html
QUOTE = (
    "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
)
WIDTH = 9


def first35_columns(quote: str, width: int = WIDTH) -> List[int]:
    cols = [i % width for i, ch in enumerate(quote) if ch != ' '][:35]
    return cols


def sha256_b64(s: str) -> str:
    return b64encode(hashlib.sha256(s.encode()).digest()).decode()


def can_use_supply(prefix: str, cols: List[int], columns: List[List[str]]) -> bool:
    # Quick feasibility by counts only
    need = [Counter() for _ in range(len(columns))]
    for ch, c in zip(prefix, cols):
        need[c][ch] += 1
    have = [Counter(col) for col in columns]
    return all(all(need[c][ch] <= have[c][ch] for ch in need[c]) for c in range(len(columns)))


def backtrack_search(cols: List[int], columns: List[List[str]], target_b64: str, seed_greedy: bool = True, fixed: dict[int,str] | None = None) -> str | None:
    supplies = [Counter(col) for col in columns]
    fixed = fixed or {}

    # Greedy candidate (top-of-bag order) as a quick check
    if seed_greedy:
        greedy = []
        idxs = [0] * len(columns)
        for c in cols:
            if idxs[c] >= len(columns[c]):
                greedy = []
                break
            greedy.append(columns[c][idxs[c]])
            idxs[c] += 1
        if greedy:
            s = ''.join(greedy)
            if sha256_b64(s) == target_b64:
                return s

    # Order choices at each position by frequency (rarer letters first), and apply fixed-letter constraints
    per_pos_choices: List[List[str]] = []
    for i, c in enumerate(cols):
        if i in fixed:
            ch = fixed[i]
            # If the fixed letter is not in this column's bag, this is impossible
            if supplies[c][ch] <= 0:
                return None
            choices = [ch]
        else:
            choices = sorted(set(columns[c]), key=lambda ch: (supplies[c][ch], ch))
        per_pos_choices.append(choices)

    target_len = len(cols)
    cur = []

    def dfs(pos: int) -> str | None:
        if pos == target_len:
            s = ''.join(cur)
            if sha256_b64(s) == target_b64:
                return s
            return None
        c = cols[pos]
        for ch in per_pos_choices[pos]:
            if supplies[c][ch] <= 0:
                continue
            # Place
            supplies[c][ch] -= 1
            cur.append(ch)
            # There is no meaningful hash-based pruning for SHA-256; keep only count-feasible prefixes
            # Proceed
            res = dfs(pos + 1)
            if res is not None:
                return res
            # Undo
            cur.pop()
            supplies[c][ch] += 1
        return None

    return dfs(0)


def parallel_search(cols: List[int], columns: List[List[str]], target_b64: str, fanout: int = 2000, split_depth: int = 6, processes: int | None = None, fixed: dict[int,str] | None = None) -> str | None:
    # Split on first K positions to generate partial prefixes, then search each shard in parallel
    K = split_depth
    supplies = [Counter(col) for col in columns]
    fixed = fixed or {}
    per_pos_choices: List[List[str]] = []
    for i, c in enumerate(cols[:K]):
        if i in fixed:
            ch = fixed[i]
            if supplies[c][ch] <= 0:
                return None
            choices = [ch]
        else:
            choices = sorted(set(columns[c]), key=lambda ch: (supplies[c][ch], ch))
        per_pos_choices.append(choices)

    # Generate a limited number of partials (bounded by fanout)
    partials: list[tuple[str, List[Counter]]] = []
    def gen_partials(pos: int, cur: list[str], sup: List[Counter]):
        nonlocal partials
        if len(partials) >= fanout:
            return
        if pos == K:
            partials.append((''.join(cur), [Counter(s) for s in sup]))
            return
        c = cols[pos]
        for ch in per_pos_choices[pos]:
            if sup[c][ch] <= 0:
                continue
            sup[c][ch] -= 1
            cur.append(ch)
            gen_partials(pos + 1, cur, sup)
            cur.pop()
            sup[c][ch] += 1

    gen_partials(0, [], [Counter(col) for col in columns])

    # Worker to complete search from a partial
    def worker(args: tuple[str, List[Counter]]):
        pre, sup = args
        cur = list(pre)
        start = len(cur)
        # Build choices for remaining positions
        for pos in range(start, len(cols)):
            pass
        def dfs(pos: int) -> str | None:
            if pos == len(cols):
                s = ''.join(cur)
                if sha256_b64(s) == target_b64:
                    return s
                return None
            c = cols[pos]
            # Use deterministic order
            if pos in fixed:
                ch = fixed[pos]
                choices = [ch] if sup[c][ch] > 0 else []
            else:
                choices = sorted({ch for ch in columns[c] if sup[c][ch] > 0})
            for ch in choices:
                if sup[c][ch] <= 0:
                    continue
                sup[c][ch] -= 1
                cur.append(ch)
                res = dfs(pos + 1)
                if res is not None:
                    return res
                cur.pop()
                sup[c][ch] += 1
            return None
        return dfs(start)

    with mp.Pool(processes=processes or max(1, mp.cpu_count() - 1)) as pool:
        for res in pool.imap_unordered(worker, partials, chunksize=1):
            if res:
                pool.terminate()
                return res
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Find 35-char prefix matching the hidden checksum using column supplies.")
    parser.add_argument("--target", default='f2wY/HdX9INIR1BoLQV4Xp0HMMhUn8XZLYxlAfm1vRw=', help="Target SHA-256 base64 of the 35-char prefix")
    parser.add_argument("--split-depth", type=int, default=8, help="Parallel split depth (first K positions)")
    parser.add_argument("--fanout", type=int, default=20000, help="Limit of partials generated for parallel search")
    parser.add_argument("--processes", type=int, default=0, help="Number of worker processes (0 => cpu_count-1)")
    parser.add_argument("--no-greedy", action="store_true", help="Disable greedy seed check")
    parser.add_argument("--no-fixed", action="store_true", help="Disable fixed-letter constraints from h()")
    args = parser.parse_args()

    target_b64 = args.target
    cols = first35_columns(QUOTE, WIDTH)

    # Quick feasibility: ensure we even have enough letters per column for the first 35
    need_counts = Counter(cols)
    have_counts = {i: len(COLUMNS[i]) for i in range(len(COLUMNS))}
    if any(need_counts[i] > have_counts[i] for i in need_counts):
        raise SystemExit(f"Not enough supply per column for first 35: need {need_counts}, have {have_counts}")

    # Apply fixed-letter constraints from the game's h() check that fall within the first 35
    h_indices = [7, 11, 15, 16, 20, 23, 31, 37, 47, 56, 70, 71, 80, 90, 104, 113]
    h_string = "SKATEBOARDCANINE"
    fixed = {} if args.no_fixed else {i: ch for i, ch in zip(h_indices, h_string) if i < 35}

    # Try greedy and then backtracking
    sol = backtrack_search(cols, COLUMNS, target_b64, seed_greedy=not args.no_greedy, fixed=fixed)
    if sol is None:
        sol = parallel_search(
            cols,
            COLUMNS,
            target_b64,
            fanout=args.fanout,
            split_depth=args.split_depth,
            processes=(args.processes or None),
            fixed=fixed,
        )

    if sol:
        print("Found prefix:", sol)
        print("SHA-256 (base64):", sha256_b64(sol))
    else:
        print("No solution found within current search limits.")


if __name__ == '__main__':
    main()

