import mido
from mido import MidiFile, MidiTrack, Message
import math

# List available input ports
print("Available input ports:")
for port in mido.get_input_names():
    print(port)

# List available output ports
print("\nAvailable output ports:")
for port in mido.get_output_names():
    print(port)


import math

# Function to adjust the velocity curve, change default values for your best setup:
def adjust_velocity(velocity, max_value=100, exponent=0.70):
    if velocity == 0:
        return 0
    result = 127 * math.pow((velocity / max_value), exponent)
    if result > 127:
        result = 127
    elif result < 1 or math.isnan(result):
        result = 1
    return int(result)

# Open the input and output ports
input_port = mido.open_input('KOMPLETE KONTROL A49:KOMPLETE KONTROL A49 MIDI 1 24:0')
output_port = mido.open_output('U2MIDI Pro:U2MIDI Pro MIDI 1 20:0')

# Process incoming MIDI messages
for msg in input_port:
    if msg.type == 'note_on' or msg.type == 'note_off':
        # Adjust the velocity
        msg.velocity = adjust_velocity(msg.velocity)
    # Send the modified message to the output port
    output_port.send(msg)

