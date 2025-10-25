from ..constants import DEFAULT_TEMPO, DEFAULT_TICKS_PER_BEAT, MIN_CLOCK_DELAY_WARNING_TIME
from ..util import make_clock_multiplier

import time
import random
import logging
import threading
from typing import Any

logger = logging.getLogger(__name__)

class BaseClockTarget:
    def tick(self):
        raise NotImplementedError("Subclasses should implement this")

class BaseClockSource:
    def __init__(self,
                 clock_target: Any = None,
                 ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT):
        self.clock_target = clock_target
        self._ticks_per_beat: int = ticks_per_beat

    def get_ticks_per_beat(self) -> int:
        return self._ticks_per_beat

    def set_ticks_per_beat(self, ticks_per_beat: int):
        self._ticks_per_beat = ticks_per_beat

    ticks_per_beat = property(get_ticks_per_beat, set_ticks_per_beat)
    """ Returns the number of ticks per beat. """

    def run(self):
        raise NotImplementedError("Subclasses should implement this")

class Clock (BaseClockSource):
    def __init__(self,
                 clock_target: BaseClockTarget = None,
                 tempo: float = DEFAULT_TEMPO,
                 ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT):
        """
        A Clock generates tick events at a regular interval, defined by the `ticks_per_beat` property.
        The higher the number of ticks per beat, the finer the granularity events can be triggered.

        Different clocking systems vary in their granularity, typically specified in ticks per beat (crotchet),
        aka "pulses per quarter note", PPQN:
         - MIDI I/O has a resolution of 24 PPQN
         - MIDI files commonly have a resolution of 96 or 120 PPQN, but can vary by file

        isobar defaults to 480 PPQN, which equates to a tick per 1.04ms. This means that events can be
        scheduled in the Timeline with a ~1ms granularity.

        Clock division is needed to interact with other clocking systems, which is handled by
        `make_clock_multiplier`. Timeline contains logic to multiplex between multiple different clock outputs.

        Args:
            clock_target: Clock target, which must have a `tick()` method and `ticks_per_beat` property.
            tempo: Tempo, in BPM.
            ticks_per_beat: The number of tick events generated per quarter-note.
        """
        super().__init__(clock_target, ticks_per_beat)
        self._tempo: float = tempo
        self.tick_duration_seconds: float = None
        self.tick_duration_seconds_orig: float = None
        self._calculate_tick_duration()

        self.warpers = []
        self.accelerate: float = 1.0
        self.thread: threading.Thread = None
        self.running: bool = False
        self.jitter: float = 0.0

        target_ticks_per_beat = self.clock_target.ticks_per_beat if self.clock_target else ticks_per_beat
        self.clock_multiplier = make_clock_multiplier(target_ticks_per_beat, self.ticks_per_beat)
    
    def _calculate_tick_duration(self):
        self.tick_duration_seconds = 60.0 / (self.tempo * self.ticks_per_beat)
        self.tick_duration_seconds_orig = self.tick_duration_seconds

    def get_ticks_per_beat(self) -> int:
        return self._ticks_per_beat

    def set_ticks_per_beat(self, ticks_per_beat: int):
        self._ticks_per_beat = ticks_per_beat
        self._calculate_tick_duration()

    ticks_per_beat = property(get_ticks_per_beat, set_ticks_per_beat)

    def get_tempo(self):
        return self._tempo

    def set_tempo(self, tempo):
        self._tempo = tempo
        self._calculate_tick_duration()

    tempo = property(get_tempo, set_tempo)
    """ The tempo of this clock, in BPM. """

    def background(self):
        """ Run this clock in a background thread. """
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        # High-precision scheduling loop using a target timestamp to minimise drift.
        start = time.perf_counter() * self.accelerate
        next_tick_time = start + self.tick_duration_seconds
        self.running = True
        while self.running:
            now = time.perf_counter() * self.accelerate
            # Handle late scheduling and accumulate missed ticks.
            while now >= next_tick_time and self.running:
                ticks = next(self.clock_multiplier)
                for _ in range(ticks):
                    self.clock_target.tick()
                # Reset tick duration and apply any warpers.
                self.tick_duration_seconds = self.tick_duration_seconds_orig
                for warper in self.warpers:
                    warp = pow(2, next(warper))
                    self.tick_duration_seconds *= warp
                next_tick_time += self.tick_duration_seconds
                now = time.perf_counter() * self.accelerate
            # Sleep most of the remaining time (if any) leaving a short busy-wait tail.
            remaining = next_tick_time - now
            if remaining > 0.0004:
                time.sleep(remaining - 0.0002)
            elif remaining > 0.00005:
                time.sleep(remaining * 0.5)
            # Busy-wait for very short intervals (<50us) to improve precision.

    def stop(self):
        self.running = False

    def warp(self, warper):
        self.warpers.append(warper)

    def unwarp(self, warper):
        self.warpers.remove(warper)

    def rewind(self):
        self.clock_target.set_song_pos(0)

class DummyClock (BaseClockSource):
    """
    Clock subclass used in testing, which ticks at the highest rate possible.
    """

    def run(self):
        while True:
            self.clock_target.tick()
