import mido
from mido import MidiFile, MidiTrack, Message
import math
import threading
import argparse

#### CONFIGURATION ####
# if you have only one device connected, leave inputname empty
# if you have multiple devices connected, specify the name of the device you want to use
# If you want to use the LPD8 to change the midi channel, set midichannelcontrolmode to True
parser = argparse.ArgumentParser(description='MIDI Velocity Curve Changer')
parser.add_argument('--inputmididevicename', type=str, default="KOMPLETE", help='Search name for input device')
parser.add_argument('--inputmididevicename2', type=str, default="MPK mini", help='Second search name for input device')
parser.add_argument('--inputmididevicenamemidichannel', type=str, default="LPD8", help='Search name for input device to change midi channel')
parser.add_argument('--outputmididevicename', type=str, default="U2MIDI", help='Search name for output device')
parser.add_argument('--midi_max_value', type=int, default=80, help='Maximum MIDI value for velocity adjustment')
parser.add_argument('--midi_exponent', type=float, default=0.60, help='Exponent for velocity adjustment')

args = parser.parse_args()

inputmididevicename = args.inputmididevicename
inputmididevicename2 = args.inputmididevicename2
inputmididevicenamemidichannel = args.inputmididevicenamemidichannel
outputmididevicename = args.outputmididevicename
midi_max_value = args.midi_max_value
midi_exponent = args.midi_exponent
#### END CONFIGURATION ####

inputname  = ""
inputnamethru = ""
outputname = ""
channelchange = 1

# List available input ports
print("Available input ports:")
for port in mido.get_input_names():
    print(port)
    if inputmididevicename in port or inputmididevicename2 in port:
        print("Using port for INPUT. ", port)
        inputname = port

if inputmididevicenamemidichannel != "":
    print("Available input ports:")
    for port in mido.get_input_names():
        print(port)
        if inputmididevicenamemidichannel in port:
            print("Using port for change midi channel:", port)
            inputnamethru = port


# List available output ports
print("\nAvailable output ports:")
for port in mido.get_output_names():
    print(port)
    if outputmididevicename in port:
        print("Using port for OUTPUT: ", port)
        outputname = port

# Function to adjust the velocity curve
def adjust_velocity(velocity, max_value=midi_max_value, exponent=midi_exponent):
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
inputthru_port = mido.open_input(inputnamethru)
output_port = mido.open_output(outputname)

# Process incoming MIDI messages
def midithread():
    global inputname,outputname,channelchange
    for msg in input_port:
        print(msg)

        if msg.type == 'note_on' or msg.type == 'note_off':
            # Adjust the velocity
            msg.velocity = adjust_velocity(msg.velocity)
        if msg.type != 'control_change':
            msg.channel = channelchange
        elif msg.type == 'control_change' and msg.control == 1:
            msg.channel = channelchange
        # Send the modified message to the output port
        #print(msg)
        output_port.send(msg)

def midithruthread():
    global inputname,outputname,channelchange
    for msg in inputthru_port:
        #print(msg)
        #adjust midi channel
        if msg.type == "program_change":
            channelchange = msg.program - 1
        else:
            output_port.send(msg)
        

thread = threading.Thread(target=midithread)
thread.start()
if inputmididevicenamemidichannel == True:
    thread2 = threading.Thread(target=midithruthread)
    thread2.start()