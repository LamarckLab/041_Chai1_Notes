"""
Inspect a Chai-1 output folder: load all scores.model_idx_*.npz inside
and print summary tables across models.

Usage:
    python read_chai_npz.py                # uses DEFAULT_DIR
    python read_chai_npz.py <folder>       # uses given folder
"""
import os
import sys
import glob
import numpy as np

DEFAULT_DIR = r'C:\Users\Lamarck\Desktop\chai1_outputs'


def load_all(folder):
    pattern = os.path.join(folder, 'scores.model_idx_*.npz')
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f'No scores.model_idx_*.npz in {folder}')
    data = {}
    for f in files:
        idx = int(os.path.basename(f).split('_')[-1].replace('.npz', ''))
        with np.load(f) as s:
            data[idx] = {k: np.array(s[k]) for k in s.files}
    return data, files


def detect_chain_count(data):
    sample = next(iter(data.values()))
    for k in ('per_chain_ptm', 'per_chain_pair_iptm'):
        if k in sample:
            return sample[k].shape[-1]
    return 1


def fmt_cell(v, width=10):
    if isinstance(v, (np.bool_, bool)):
        return f'{str(bool(v)):>{width}}'
    if np.issubdtype(type(v), np.integer):
        return f'{int(v):>{width}d}'
    return f'{float(v):>{width}.4f}'


def print_scalar_table(data):
    """rows = field, cols = model.  Only fields that collapse to a single number."""
    sample = next(iter(data.values()))
    keys = [k for k, v in sample.items() if v.size == 1]
    if not keys:
        return
    model_ids = sorted(data.keys())
    label_w = max(len(k) for k in keys) + 2
    col_w = 12

    title = 'Table 1 -- Scalar scores per model  (rows = field, cols = model)'
    bar = '=' * max(len(title), label_w + col_w * len(model_ids))
    print(bar); print(title); print(bar)

    header = ' ' * label_w + ''.join(f'{f"model_{m}":>{col_w}}' for m in model_ids)
    print(header); print('-' * len(header))

    for k in keys:
        row = f'{k:<{label_w}}'
        for m in model_ids:
            row += fmt_cell(data[m][k].flatten()[0], col_w)
        print(row)
    print()


def print_per_chain_table(data, n_chains):
    """rows = chain, cols = model.  For (1, C)-shaped fields, only when C > 1."""
    if n_chains <= 1:
        return
    sample = next(iter(data.values()))
    keys = [k for k, v in sample.items()
            if v.size == n_chains and v.size > 1 and v.ndim <= 2]
    if not keys:
        return
    model_ids = sorted(data.keys())
    label_w = 10
    col_w = 12

    for k in keys:
        title = f'Table -- {k}  (rows = chain, cols = model)'
        bar = '=' * max(len(title), label_w + col_w * len(model_ids))
        print(bar); print(title); print(bar)

        header = ' ' * label_w + ''.join(f'{f"model_{m}":>{col_w}}' for m in model_ids)
        print(header); print('-' * len(header))

        for c in range(n_chains):
            row = f'{f"chain_{c}":<{label_w}}'
            for m in model_ids:
                row += fmt_cell(data[m][k].flatten()[c], col_w)
            print(row)
        print()


def print_pair_matrices(data, n_chains):
    """One C×C matrix per model, for (1, C, C)-shaped fields, only when C > 1."""
    if n_chains <= 1:
        return
    sample = next(iter(data.values()))
    keys = [k for k, v in sample.items()
            if v.size == n_chains * n_chains and v.ndim == 3]
    if not keys:
        return
    model_ids = sorted(data.keys())
    label_w = 8
    col_w = 10

    for k in keys:
        title = f'Table -- {k}  ({n_chains}x{n_chains} matrix per model)'
        bar = '=' * max(len(title), 60)
        print(bar); print(title); print(bar)
        for m in model_ids:
            print(f'\n  model_idx_{m}:')
            mat = data[m][k].reshape(n_chains, n_chains)
            header = ' ' * label_w + ''.join(f'{f"c{c}":>{col_w}}' for c in range(n_chains))
            print('  ' + header)
            for r in range(n_chains):
                row = f'{f"c{r}":<{label_w}}'
                for c in range(n_chains):
                    row += fmt_cell(mat[r, c], col_w)
                print('  ' + row)
        print()


def print_ranking(data, n_chains):
    is_monomer = n_chains == 1
    metric = 'ptm' if is_monomer else 'aggregate_score'
    sample = next(iter(data.values()))
    if metric not in sample:
        return

    title = (f'Ranking by {metric}  '
             f'({"monomer -> ptm" if is_monomer else f"complex of {n_chains} chains -> aggregate_score"})')
    bar = '=' * max(len(title), 60)
    print(bar); print(title); print(bar)

    ranked = sorted(data.keys(),
                    key=lambda i: -float(data[i][metric].flatten()[0]))
    for rank, m in enumerate(ranked):
        v = float(data[m][metric].flatten()[0])
        flag = '  <-- best' if rank == 0 else ''
        print(f'  rank {rank+1}:  model_idx_{m}    {metric}={v:.4f}{flag}')
    print()


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    folder = os.path.abspath(folder)
    print(f'Folder:  {folder}')

    try:
        data, files = load_all(folder)
    except FileNotFoundError as e:
        print(f'[ERROR] {e}')
        return

    print(f'Found {len(files)} score file(s):  '
          + ', '.join(os.path.basename(f) for f in files))
    n_chains = detect_chain_count(data)
    kind = 'monomer' if n_chains == 1 else f'complex with {n_chains} chains'
    print(f'Detected: {kind}\n')

    print_scalar_table(data)
    print_per_chain_table(data, n_chains)
    print_pair_matrices(data, n_chains)
    print_ranking(data, n_chains)


if __name__ == '__main__':
    main()
