#!/usr/bin/python3
# SPDX-License-Identifier: AGPL-3.0-only

import argparse

try:
    import png # type: ignore
except ModuleNotFoundError:
    png = None

def sl(fret: str, n: int) -> str:
    if fret in ['x', 'X', '0']:
        return fret
    return str(int(fret) - n)

# Fonts are 6 wide and 8 tall.
def load_font() -> dict[str, list[list[int]]]:
    font: dict[str, list[list[int]]] = {}
    curchar = None
    with open("font", "r") as f:
        while line := f.readline():
            if line[-1] == '\n':
                line = line[:-1]
            if line == '':
                continue
            if ":" in line:
                curchar = line[0]
                font[curchar] = []
                continue
            row = [0 if c != ' ' else 255 for c in list(line)]
            assert(curchar)
            font[curchar].append(row)

    for k in font.keys():
        glyph = font[k]
        for i in range(len(glyph)):
            while len(glyph[i]) < 6:
                glyph[i].append(255)
        while len(glyph) < 8:
            glyph.append([255] * 6)
        font[k] = glyph

    return font

def dump_png(path: str, rows: list[list[str]], scale: int) -> None:
    # Fonts are 6x8, though most characters actually define as 5x7.  By
    # implicitly anchoring them to the top left, we can slam them together
    # without worrying about spacing.
    font = load_font()
    arr = []
    for row in rows:
        if '-' in row:
            continue

        for i in range(8):
            line = []
            seen_space = False
            seen_nonspace = False
            leftside = True
            for j, c in enumerate(row):
                if not seen_space and c == ' ':
                    seen_space = True
                    continue
                if c == ' ' and seen_nonspace:
                    continue
                if c != ' ':
                    seen_nonspace = True
                if j == len(row) - 1:
                    if c == '|':
                        c = 'c'
                    elif c == '*':
                        c = 'r'
                if leftside and c == '|':
                    leftside = False
                    c = 'o'
                elif leftside and c == '*':
                    leftside = False
                    c = 'l'

                line += font[c][i]
            arr.append(line)

    # padding
    rowlen = len(arr[0])
    arr.insert(0, [255] * rowlen)
    arr.append([255] * rowlen)
    for out_row in arr:
        out_row.insert(0, 255)

    if scale != 1:
        bigger = []
        for out_row in arr:
            nr = []
            for p in out_row:
                for _ in range(scale):
                    nr.append(p)
            for _ in range(scale):
                bigger.append(nr)
        arr = bigger

    png.from_array(arr, 'L').save(args.output_png)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--position", type=int, default=0)
    parser.add_argument("-o", "--output-png", type=str)
    parser.add_argument("-x", "--scale-by", type=int, default=1)
    parser.add_argument("frets")
    parser.add_argument("fingers")
    args = parser.parse_args()

    if args.output_png and not png:
        print("python3-pypng is required to output images")
        exit(1)
    if args.scale_by and not args.output_png:
        print("Scale is not usable unless outputting an image")
        parser.print_help()
        exit(1)

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
            row = list(''.join(row))
        rows.append(row)

    if not args.output_png:
        print("\n".join([''.join(r) for r in rows]))
        exit(0)

    dump_png(args.output_png, rows, args.scale_by)
