import mido
from mido import MidiFile, MidiTrack, Message
import math
import threading
import argparse

# Load Configuration for the MIDI Velocity Curve Changer
parser = argparse.ArgumentParser(description='MIDI Velocity Curve Changer')
parser.add_argument('--inputmididevicename', type=str, default="", help='Search name for input device')
parser.add_argument('--inputmididevicenamechannelcontrol', type=str, default="", help='Search name for input device to change midi channel')
parser.add_argument('--outputmididevicename', type=str, default="", help='Search name for output device')
parser.add_argument('--midi_max_value', type=int, default=100, help='Maximum MIDI value for velocity adjustment')
parser.add_argument('--midi_exponent', type=float, default=0.60, help='Exponent for velocity adjustment')
args = parser.parse_args()

inputmididevicename = args.inputmididevicename
inputmididevicenamechannelcontrol = args.inputmididevicenamechannelcontrol
outputmididevicename = args.outputmididevicename
midi_max_value = args.midi_max_value
midi_exponent = args.midi_exponent
# End of Configuration

inputname  = ""
inputnamethru = ""
outputname = ""
channelchange = 1

# Functions
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
        print(msg)
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
# Functions end

# List available input ports
print("\033[91mAvailable input ports:\033[0m")
for port in mido.get_input_names():
    print(port)

print("\033[91m\nAvailable output ports:\033[0m")
for port in mido.get_output_names():
    print(port)

if not inputmididevicename or not outputmididevicename:
    print("\033[91mInput or output MIDI device name is empty. Exiting program. Please specify the names in the parameters.\033[0m")
    exit()
# List available input ports end



# Configure the midi ports
print("\033[93mStarting configuring MIDI Velocity Curve Changer\033[0m")
for port in mido.get_input_names():
    if inputmididevicename in port:
        print("Using port for INPUT. ", port)
        inputname = port
        break

if inputmididevicenamechannelcontrol != "":
    for port in mido.get_input_names():
        if inputmididevicenamechannelcontrol in port:
            print("Using port for change midi channel:", port)
            inputnamethru = port
            break

for port in mido.get_output_names():
    if outputmididevicename in port:
        print("Using port for OUTPUT: ", port)
        outputname = port
        break

input_port = mido.open_input(inputname)
output_port = mido.open_output(outputname)
if inputmididevicenamechannelcontrol != "":
    inputthru_port = mido.open_input(inputnamethru)
# Configure the midi ports end
 
# Start the threads
print("\033[93mStarting threads MIDI Velocity Curve Changer\033[0m")
thread = threading.Thread(target=midithread)
thread.start()

if inputmididevicenamechannelcontrol != "":
    thread2 = threading.Thread(target=midithruthread)
    thread2.start()
# Start the threads end