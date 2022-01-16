#!/usr/bin/python3
# SPDX-License-Identifier: AGPL-3.0-only

import os
import subprocess
import time

chords = [("C", "X,3,2,0,1,0", "X,3,2,0,1,0")]

# A mnemosyne v2 file is a ZIP container consisting of:
#  - cards.xml, which is both complicated and important
#  - METADATA, a colon-delimited set of magic keys
#  - any linked media files
#
# To misquote @dril:
#
#    who the fuck is scraeming "STOP BLACKBOXING PROGRAMS YOU HAVE SOURCE FOR"
#    at my house. show yourself, coward. i will never stop blackboxing
files = ["cards.xml", "METADATA"]

with open("METADATA", "w") as f:
    f.write(f"""\
card_set_name:Guitar chords
author_name:https://github.com/frozencemetery/chordboard
author_email:
tags:guitar chords
date:{time.strftime('%a %b %d %Y')}
revision:1
notes:
""")

imgs = []
cards = []
links = []
for cname, frets, fingers in chords:
    dest = f"{cname}.png"
    files.append(dest)
    subprocess.check_call(["./main.py", frets, fingers, "-o", dest, "-x3"])
    imgs.append(f'<log type="13"><fname>{dest}</fname></log>')
    cards.append(f'<log type="16" o_id="{cname}">'
                 f'<f>{cname}</f>'
                 f'<b>&lt;img src="{dest}"&gt;</b>'
                 f'</log>')
    links.append(f'<log type="6" o_id="{cname}1" card_t="2" fact="{cname}" '
                 f'fact_v="2.1" tags="gchords" gr="-1" e="2.5" ac_rp="0" '
                 f'rt_rp="0" lps="0" ac_rp_l="0" rt_rp_l="0" l_rp="-1" '
                 f'n_rp="-1"></log>')
    links.append(f'<log type="6" o_id="{cname}2" card_t="2" fact="{cname}" '
                 f'fact_v="2.2" tags="gchords" gr="-1" e="2.5" ac_rp="0" '
                 f'rt_rp="0" lps="0" ac_rp_l="0" rt_rp_l="0" l_rp="-1" '
                 f'n_rp="-1"></log>')

data = imgs + cards + links
flat_data = "\n".join(data)
with open("cards.xml", "w") as f:
    f.write(f'<openSM2sync number_of_entries="{len(data) + 1}">'
            f'<log type="10" o_id="gchords"><name>guitar chords</name></log>'
            f'\n{flat_data}\n</openSM2sync>\n')

os.unlink("chords.cards")
subprocess.check_call(["zip", "chords.cards"] + files)

for f in files:
    os.unlink(f)
