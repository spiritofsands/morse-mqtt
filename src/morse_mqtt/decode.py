#!/usr/bin/env python
# -*- coding: utf-8 -*-
import morse_talk as mtalk
from typing import NamedTuple


class Pulse(NamedTuple):
    on: float  # timestamp
    off: float  # timestamp

    def duration(self):
        return self.off - self.on


def decode_pulses(pulses):
    min_duration = min(p.duration() for p in pulses)

    binary_encoding = []
    prev_pulse = None
    for p in pulses:
        if prev_pulse is not None:
            gap_width = p.on - prev_pulse.off
            binary_encoding.extend([0] * gap_width)

        pulse_width = p.duration() // min_duration
        binary_encoding.extend([1] * pulse_width)

        prev_pulse = p

    return mtalk.decode(''.join(map(str, binary_encoding)),
                        encoding_type='binary')


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
