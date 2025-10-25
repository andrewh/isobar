#!/usr/bin/env python3

#------------------------------------------------------------------------
# isobar: ex-static-pattern
#
# Bind a chord sequence to a static sequence, which is then referenced
# in other patterns.
#------------------------------------------------------------------------

from isobar.key import Key
from isobar.pattern.static import PStaticPattern
from isobar.pattern.sequence import PSequence
from isobar.pattern.chance import PWhite
from isobar.pattern.sequence import PCreep
from isobar.timelines.timeline import Timeline
import logging

def main():
    key_sequence = PSequence([
        Key("C", "minor"),
        Key("G", "minor"),
        Key("Bb", "major"),
        Key("F", "major"),
    ])
    key = PStaticPattern(key_sequence, 4)
    timeline = Timeline(120)
    timeline.schedule({
        "degree": 0,
        "key": key,
        "octave": 3
    })
    timeline.schedule({
        "degree": PCreep(PWhite(0, 6), 4, 4, 4),
        "key": key,
        "octave": 6,
        "duration": 0.25
    })
    timeline.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
    main()