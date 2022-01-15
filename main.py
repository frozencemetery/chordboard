#!/usr/bin/python3
# SPDX-License-Identifier: AGPL-3.0-only

import argparse

try:
    import png
except ModuleNotFoundError:
    png = None

def sl(fret: str, n: int) -> str:
    if fret in ['x', 'X', '0']:
        return fret
    return str(int(fret) - n)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--position", type=int, default=0)
    parser.add_argument("-o", "--output-png", type=str)
    parser.add_argument("frets")
    parser.add_argument("fingers")
    args = parser.parse_args()

    fingers = args.fingers.split(",")
    frets = args.frets.split(",")

    minfret = -1
    maxfret = 0
    for fret in frets:
        if fret in ['x', 'X', '0']:
            continue
        fret = int(fret)
        if fret > maxfret:
            maxfret = fret
        elif minfret == -1 or fret < minfret:
            minfret = fret

    position = args.position
    if position == 0:
        position = minfret
        if position > 1: # automatic position adjustment
            frets = [sl(fret, position - 1) for fret in frets]
            maxfret -= position - 1

    rows = []
    pad = ' ' * len(str(position))
    rows.append(list(f"{pad} {' '.join(fingers)}"))
    rows.append(list(f"{pad} -----------"))
    for i in range(1, max(maxfret, 5) + 1):
        row = []
        if i == 1 and position != 1:
            row.append(str(position))
        else:
            row.append(pad)

        for fret in frets:
            if fret != 0 and str(i) == fret:
                row.append(" *")
            else:
                row.append(" |")
        rows.append(row)
    print("\n".join([''.join(r) for r in rows]))

    if not args.output_png:
        exit(0)
    if not png:
        print("python3-pypng is required to output images")
        exit(1)

    arr = [[255, 0, 0, 255], [0, 255, 255, 0]]
    png.from_array(arr, 'L').save(args.output_png)
