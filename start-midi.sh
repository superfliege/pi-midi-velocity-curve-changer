#!/bin/bash
# Enhanced MIDI Velocity Curve Changer Startup Script

# Method 1: Using JSON configuration (recommended)
# Create a config.json file with your settings and uncomment the line below:
#python3 midi.py --config config.json

# Method 2: Command line arguments (legacy)
# Basic velocity adjustment
python3 midi.py --inputmididevicename "KOMPLETE" --outputmididevicename "U2MIDI" --midi_exponent -60

# Method 3: With debug mode
#python3 midi.py --inputmididevicename "KOMPLETE" --outputmididevicename "U2MIDI" --midi_exponent -60 --debugmode

# Method 4: Full configuration with channel control
#python3 midi.py --inputmididevicename "KOMPLETE" --outputmididevicename "U2MIDI" --inputmididevicenamechannelcontrol "LPD8" --midi_exponent -60 --curve_type bezier

# Method 5: Using different curve types
#python3 midi.py --inputmididevicename "KOMPLETE" --outputmididevicename "U2MIDI" --midi_exponent 0.4 --curve_type exponential --sensitivity 0.9