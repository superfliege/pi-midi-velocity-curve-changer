#!/bin/bash
# Minimum Startup Script
#python3 midi.py --inputmididevicename "KOMPLETE" --outputmididevicename "U2MIDI" --midi_exponent 80
# Minimum Startup Script with debug mode
python3 midi.py --inputmididevicename "KOMPLETE" --outputmididevicename "U2MIDI" --midi_exponent -80 --debugmode 1
# Full Startup Script
#python3 midi.py --inputmididevicename "KOMPLETE" --outputmididevicename "U2MIDI" --inputmididevicenamechannelcontrol "LPD8"  --midi_exponent 50