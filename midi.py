import mido
from mido import MidiFile, MidiTrack, Message
import math

inputname  = ""
outputname = ""
channelchange = 1

# List available input ports
print("Available input ports:")
for port in mido.get_input_names():
    print(port)
    if "MPK mini" in port or "KOMPLETE" in port:
        print("Using port for INPUT. ", port)
        inputname = port

# List available output ports
print("\nAvailable output ports:")
for port in mido.get_output_names():
    print(port)
    if "U2MIDI" in port:
        print("Using port for OUTPUT: ", port)
        outputname = port

# Function to adjust the velocity curve
def adjust_velocity(velocity, max_value=80, exponent=0.60):
    if velocity == 0:
        return 0
    result = 127 * math.pow((velocity / max_value), exponent)
    if result > 127:
        result = 127
    elif result < 1 or math.isnan(result):
        result = 1
    return int(result)

# Open the input and output ports
input_port = mido.open_input(inputname)
output_port = mido.open_output(outputname)

# Process incoming MIDI messages
for msg in input_port:
    print(msg)
    #adjust midi channel
    if msg.type == "control_change" and msg.control == 94 and msg.value < 16 and msg.value > 0:
        channelchange = msg.value
    msg.channel = channelchange
    if msg.type == 'note_on' or msg.type == 'note_off':
        msg.channel = channelchange
        # Adjust the velocity
        msg.velocity = adjust_velocity(msg.velocity)
    # Send the modified message to the output port
    print(msg)
    output_port.send(msg)
