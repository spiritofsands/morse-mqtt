#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import morse_talk as mtalk
from typing import NamedTuple


class Pulse(NamedTuple):
    on: float  # timestamp
    off: float  # timestamp

    def duration(self):
        return self.off - self.on


def decode_pulses(pulses):
    if not pulses:
        return

    gaps = [p1.on - p0.off for (p0, p1) in zip(pulses[:-1], pulses[1:])]

    if not gaps:
        # single character, either `e` or `t`
        min_duration = pulses[0].duration()
    else:
        min_duration = min(gaps)

    assert(len(pulses) == len(gaps) + 1)

    gaps = (int(round(g / min_duration)) for g in gaps)
    pulse_durations = (int(round(p.duration() / min_duration)) for p in pulses)

    binary_encoding = []
    for (width_1, width_0) in itertools.zip_longest(pulse_durations, gaps, fillvalue=None):
        binary_encoding.extend([1]*width_1)

        if width_0 is not None:
            binary_encoding.extend([0]*width_0)
    try:
        return mtalk.decode(''.join(map(str, binary_encoding)),
                            encoding_type='binary')
    except KeyError:
        return 'Err: decode failure'


if __name__ == "__main__":
    pulses = [
        Pulse(1, 2),
        Pulse(3, 4),
        Pulse(5, 8),
    ]

    print(pulses)

    for p in pulses:
        print(p.duration())

    print(decode_pulses(pulses))
