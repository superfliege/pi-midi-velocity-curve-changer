# pi-midi-velocity-curve-changer
## Description 
This little python script will adjust the midi velocity curve from your keyboard to fix velocity issues if your keyboard does not handle the velocity well. 
Setup is like: Keyboard -> USB -> Rasbperry PI -> USB to Midi -> Midi In from your Synthesizer / MPC.

I had the following problem:
I have a Native Instruments KOMPLETE KONTROL A49 keyboard and an MPC ONE.
Although I think the keyboard is pretty good, it has a terrible velocity curve which unfortunately is not standalone customizable. I still have an old Raspberry Pi lying around and a USB-to-Midi adapter. With this Python script it was possible to put the Raspberry Pi between the keyboard and the MPC one to function as a “velocity adjuster”.

Optional: If you have an Akai LPD8 Controller you can use the prgm_change midi message to manipulate the midi messages from your input device.
With this functionality the script will give you a chance to change midi channel for your keyboard. 

The pygamemidi.py and pygamemidi.sh are experimental and are used to display the velocity curve, midichannel change. They are not necessary.

You also need: 

1. USB Keyboard
2. A USB to Midi device (e.g.: CME U2MIDI Pro)
3. Raspberry Pi
4. (Optional) Akai LPD8 Controller


# Setup 

# 1. Setup the midi.py and midi.sh file on your raspberry pi
# 2. Install the python libs:
   
   pip install mido

   pip install math
# 3. Identify Your MIDI Devices
   - Connect your MIDI devices to your computer.
   - Run the script to list available input and output ports. The script will print the names of all connected MIDI devices.
   

## 4. Configuration

### 1. Edit Configuration Variables

Open the script file (`midi.py`) in a text editor. Locate the configuration section at the top of the script.

### 2. Set Input Device Names

- `inputnamesearchname`: Set this to the name (or part of the name) of your primary MIDI input device (e.g., "KOMPLETE").
- `inputnamesearchname2`: Set this to the name (or part of the name) of an alternative MIDI input device (e.g., "MPK mini"). If you have only one input device leave this empty. 
- `inputnamethrusearchname`: Set this to the name (or part of the name) of the MIDI device used for the program_change will channel_change functionality (e.g., "LPD8"). If you do not need this leave this empty. 

### 3. Set Output Device Name

- `outputsearchname`: Set this to the name (or part of the name) of your MIDI output device (e.g., "U2MIDI").

### 4. (optional) Disable/Enable LPD8 Control Mode

- `lpd8controlMode`: Set this to `True` if you want to use the LPD8 to change the MIDI channel threw the program_change. Otherwise, set it to `False`. 

### Example Configuration

```python
inputnamesearchname = "KOMPLETE"
inputnamesearchname2 = "MPK mini"
inputnamethrusearchname = "LPD8"
outputsearchname = "U2MIDI"
lpd8controlMode = True
```

# 5. (optional) adjust the parameters from the function in the script for your optimal velocity settings.

# 6. Set up the autostart from your midi script:
   
   chmod 775 /home/user1/midi.sh
   
   crontab -e
   
   Input this in the crontab file:
   
   @reboot sh /home/user1/midi.sh

   ### Configuration Setup


## Thanks

Special thanks to @georg-zeiser!
Source: https://github.com/georg-zeiser/midi-velocity-mapper


