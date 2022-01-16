# chordboard

Simple tool to create guitar fretboard diagrams, with optional ability to
generate a flashcard deck.

It can output images.  For instance:

```
$ # Awful chord to show off notation, image scaled up 3x
$ ./main.py 7,8,10,9,11,X T,1,3,2,4,X -o demo.png -x 3
```

produces the demo.png in this repo:

![the above chord](demo.png "the above chord")

Or it can output to the console:

```
$ # C major
$ ./main.py X,3,2,0,1,0 X,3,2,0,1,0
  X 3 2 0 1 0
  -----------
  | | | | * |
  | | * | | |
  | * | | | |
  | | | | | |
  | | | | | |
$ 
$ # Hendrix-style
$ ./main.py 0,7,6,7,8,0 0,2,1,3,4,0
  0 2 1 3 4 0
  -----------
6 | | * | | |
  | * | * | |
  | | | | * |
  | | | | | |
  | | | | | |
$ 
$ # Same thing, but notated in fifth position
$ ./main.py -p5 0,3,2,3,4,0 0,2,1,3,4,0
  0 2 1 3 4 0
  -----------
5 | | | | | |
  | | * | | |
  | * | * | |
  | | | | * |
  | | | | | |
$ 
```

There are many tools that *almost* generate these standard images, but all
that I've found aren't quite right - often they don't have fingerings at the
top, or write note names below (unhelpful for shape memorization), or any
number of other things.

I hope your music goes well!

## genmnemo.py

Tool that generates a
[mnemosnye](https://github.com/mnemosyne-proj/mnemosyne)-compatibile file of
cards for import.  Creates chords.cards, which can be imported into mnemosyne.

Chords are given as a space-separated value on stdin.  So one could do:

```
$ cat > chords.ssv <<EOF
Am X,0,2,2,1,0 X,0,2,3,1,0
Em 0,2,2,0,0,0 X,2,3,0,0,0
EOF
$ cat chords.ssv | ./genmnemo.py
```

which will produce chords.cards, suitable for mnemosnye import.

Aside: why no anki support?  The original reason is that I'd previously used
mnemosnye, and the storage format wasn't too hard to figure out.  That said, I
did look into adding it, but ran into two problems.  First, anki started using
rust, bazel, and nodejs, which means packaging it suddenly became really
complicated and it lags far behind upstream (see
[Debian](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=958853),
[Fedora](https://bugzilla.redhat.com/show_bug.cgi?id=1815782)).  Second, as of
this writing, the ankiweb server has been changed and will no longer sync with
distro clients.  This means that for my purposes, it's a dead project, so I
don't plan to add support myself.
