#!/usr/bin/env python
# -*- coding: utf-8 -*-
from morse_mqtt.decode import Pulse, decode_pulses
import morse_talk as mtalk


# This will be replaced by the MQTT receiver
def encode_pulses(line):
    # Convert line to morse code binary encoding
    bin_enc = mtalk.encode(line.strip(), encoding_type='binary')

    # Convert binary encoding to a pulse sequence. We can just use something dumb for the timestamps for now.
    timestamps = [0]
    prev_value = bin_enc[0]
    assert (prev_value[0] == '1')

    for i, value in enumerate(bin_enc[1:], 1):
        if value != prev_value:
            prev_value = value
            timestamps.append(i)

    # Add the timestamp of the last falling edge
    timestamps.append(len(bin_enc))

    # Group in pairs and create a pulse sequence
    timestamps = [iter(timestamps)] * 2
    return [Pulse(x, y) for (x, y) in zip(*timestamps)]


if __name__ == "__main__":
    import fileinput

    for line in fileinput.input():
        pulses = encode_pulses(line)

        print(decode_pulses(pulses))
