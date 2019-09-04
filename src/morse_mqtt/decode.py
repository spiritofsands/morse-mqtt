#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
from typing import NamedTuple
import morse_talk as mtalk
import numpy as np
from scipy.cluster.vq import whiten


class Pulse(NamedTuple):
    on: float  # timestamp
    off: float  # timestamp

    def duration(self):
        return self.off - self.on


def classify_pulses(pulses):
    on = (p.duration() for p in pulses)
    off = (p1.on - p0.off for (p0, p1) in zip(pulses[:-1], pulses[1:]))
    features = np.fromiter(itertools.chain(on, off), float, count=-1)

    whitened = whiten(features).reshape((-1, 1))

    # Use different thresholds for classifying pulses and gaps
    n = len(pulses)
    pulses = [3 if w > 2.5 else 1 for w in whitened[:n]]
    gaps = [3 if w > 2 else 1 for w in whitened[n:]]
    return pulses, gaps


def decode_pulses(pulses):
    pulses, gaps = classify_pulses(pulses)
    assert (len(pulses) == len(gaps) + 1)

    binary_encoding = []
    for x, y in zip(pulses[:-1], gaps):
        binary_encoding.extend([1] * x)
        binary_encoding.extend([0] * y)
    binary_encoding.extend([1] * pulses[-1])

    try:
        return mtalk.decode(''.join(map(str, binary_encoding)),
                            encoding_type='binary')
    except KeyError:
        print(binary_encoding)
        return 'Err: decode failure'


if __name__ == "__main__":
    TESTDATA = [
        Pulse(on=1567608654.141699, off=1567608654.341356),
        Pulse(on=1567608654.549512, off=1567608655.234844),
        Pulse(on=1567608655.357414, off=1567608655.96127),
        Pulse(on=1567608656.672383, off=1567608657.184696),
        Pulse(on=1567608657.379306, off=1567608657.9863071),
        Pulse(on=1567608658.391364, off=1567608658.823227),
        Pulse(on=1567608659.441066, off=1567608659.595488),
        Pulse(on=1567608659.803642, off=1567608660.462555),
        Pulse(on=1567608660.610762, off=1567608660.814921),
        Pulse(on=1567608661.424991, off=1567608661.623817),
        Pulse(on=1567608662.0087569, off=1567608662.509867),
        Pulse(on=1567608662.635731, off=1567608663.1660428),
        Pulse(on=1567608663.1665401, off=1567608663.250591),
        Pulse(on=1567608663.9415581, off=1567608664.557454),
        Pulse(on=1567608664.663523, off=1567608664.8727438),
        Pulse(on=1567608665.067158, off=1567608665.27342)
    ]
    TESTDATA2 = [
        Pulse(on=1567608768.0885813, off=1567608768.3093312),
        Pulse(on=1567608768.5074263, off=1567608768.718118),
        Pulse(on=1567608768.926039, off=1567608769.1209602),
        Pulse(on=1567608769.3372715, off=1567608769.5440984),
        Pulse(on=1567608770.124031, off=1567608770.322572),
        Pulse(on=1567608770.9301946, off=1567608771.1807323),
        Pulse(on=1567608771.333441, off=1567608771.591475),
        Pulse(on=1567608771.7972283, off=1567608772.010662),
        Pulse(on=1567608772.2081735, off=1567608772.4160655),
        Pulse(on=1567608772.9580214, off=1567608773.166176)
    ]
    TESTDATA3 = [
        Pulse(on=1567612335.7476203, off=1567612335.9528375),
        Pulse(on=1567612336.1632333, off=1567612336.3199039),
        Pulse(on=1567612336.5725675, off=1567612336.7781076),
        Pulse(on=1567612336.9306922, off=1567612337.138929),
        Pulse(on=1567612337.7437553, off=1567612338.0129707),
        Pulse(on=1567612338.5543716, off=1567612338.7602694),
        Pulse(on=1567612338.9629095, off=1567612339.570158),
        Pulse(on=1567612339.8622646, off=1567612340.068103),
        Pulse(on=1567612340.274348, off=1567612340.63173),
        Pulse(on=1567612340.9935608, off=1567612341.199344),
        Pulse(on=1567612341.4051442, off=1567612342.0054407),
        Pulse(on=1567612342.2073634, off=1567612342.4116077),
        Pulse(on=1567612342.643149, off=1567612342.8444505),
        Pulse(on=1567612343.42973, off=1567612344.0316749),
        Pulse(on=1567612344.283503, off=1567612344.8443813),
        Pulse(on=1567612345.1071844, off=1567612345.6485472)
    ]

    print(decode_pulses(TESTDATA))
    print(decode_pulses(TESTDATA2))
    print(decode_pulses(TESTDATA3))
