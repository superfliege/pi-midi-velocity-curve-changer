import mido
from mido import MidiFile, MidiTrack, Message
import math
import pygame
import threading
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode([800,480])
running = True

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

size=384
offset=(15, ((480-size)//2))
# Test values
test_values = range(0,127)
# Calculate and print results
results = [(v*size/127 + offset[0], (127 - adjust_velocity(v))*size/127 + offset[1]) for v in test_values]

# Open the input and output ports
input_port = mido.open_input(inputname)
output_port = mido.open_output(outputname)

# Process incoming MIDI messages
def midithread():
    global inputname,outputname,channelchange
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

thread = threading.Thread(target=midithread)
thread.start()
pygame.font.init()
my_font = pygame.font.SysFont("Verdana",90)
clock=pygame.time.Clock()
while running:
    screen.fill((0,0,0))

    text_surface = my_font.render(str(channelchange),False,(255,255,255))
    screen.blit(text_surface,(470,250)) 
    
    pygame.draw.line(screen,(255,255,255),offset,(offset[0],offset[1]+size))
    pygame.draw.line(screen,(255,255,255),(offset[0],offset[1]+size),(offset[0]+size,offset[1]+size))
    pygame.draw.lines(screen,(255,255,0),False,results)
    pygame.display.flip()
    events=pygame.event.get()
 
    for e in events:
      if e.type == pygame.KEYDOWN:  
          if e.key == pygame.K_ESCAPE:
              running = false
    clock.tick(10)






