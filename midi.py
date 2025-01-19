import mido
from mido import MidiFile, MidiTrack, Message
import math
import threading

#### CONFIGURATION ####
# if you have only one device connected, leave inputname empty
# if you have multiple devices connected, specify the name of the device you want to use
# If you want to use the LPD8 to change the midi channel, set lpd8controlMode to True
inputnamesearchname = "KOMPLETE"
inputnamesearchname2 = "MPK mini"
inputnamethrusearchname = "LPD8"
outputsearchname = "U2MIDI"
lpd8controlMode = True
midi_max_value = 80
midi_exponent = 0.60
#### END CONFIGURATION ####

inputname  = ""
inputnamethru = ""
outputname = ""
channelchange = 1

# List available input ports
print("Available input ports:")
for port in mido.get_input_names():
    print(port)
    if inputnamesearchname in port or inputnamesearchname2 in port:
        print("Using port for INPUT. ", port)
        inputname = port

if lpd8controlMode == True:
    print("Available input ports:")
    for port in mido.get_input_names():
        print(port)
        if "MPK mini" in port or "LPD8" in port:
            print("Using port for INPUTTHRU. ", port)
            inputnamethru = port


# List available output ports
print("\nAvailable output ports:")
for port in mido.get_output_names():
    print(port)
    if "U2MIDI" in port:
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
        #print(msg)

        if msg.type == 'note_on' or msg.type == 'note_off':
            # Adjust the velocity
            msg.velocity = adjust_velocity(msg.velocity)
        if msg.type != 'control_change':
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
if lpd8controlMode == True:
    thread2 = threading.Thread(target=midithruthread)
    thread2.start()