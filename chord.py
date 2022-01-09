#!/usr/bin/python3
# SPDX-License-Identifier: AGPL-3.0-only

# Text format should look something like:
#   X 0 1 2 3 4
#   -----------
# 3 | | * | | |
#   | | | * | |
#   | | | | * |
#   | | | | | *
#   | | | | | |

fingerings = ['X', '0', '1', '2', '3', '4']
offset = 3
frets = [0, 0, 1, 2, 3, 4]

print(f"  {' '.join(fingerings)}")
print("  -----------")
for i in range(5):
    row = []
    if i == 0 and offset != 0:
        row.append(str(offset))
    else:
        row.append(' ')

    for fret in frets:
        if fret != 0 and i == fret:
            row.append(" *")
        else:
            row.append(" |")
    print(''.join(row))
