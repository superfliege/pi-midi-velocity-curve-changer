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

# Basic Hardware Setup
![Screenshot 2025-01-31 195321](https://github.com/user-attachments/assets/baad05cb-7537-4d38-9271-32a55b285580)



# Velocity Curve examples

## Light
midi_max_value = 100
midi_exponent = 0.80
![Screenshot 2025-01-31 194711](https://github.com/user-attachments/assets/8d43c2b7-941a-47c3-8a10-a86edf0a164e)

## Middle (Recommended)
midi_max_value = 80
midi_exponent = 0.60
![Screenshot 2025-01-31 194445](https://github.com/user-attachments/assets/983e6e9d-31c0-477c-ae0d-ea19702bc97c)

## Strong
midi_max_value = 80
midi_exponent = 0.40
![Screenshot 2025-01-31 194836](https://github.com/user-attachments/assets/e72b6f35-ce86-4b08-9395-1df7d7773c7e)


# Setup 

# 1. Setup the midi.py and start-midi.sh file on your raspberry pi
# 2. Install the python libs:
   
   ```sh
   pip install mido
   pip install math
   ```

# 3. Identify Your MIDI Devices
   - Run the script to list available input and output ports. The script will print the names of all connected MIDI devices.

## 4. Configuration

Open the start-midi.sh and configure your settings:

Minimum Startup Commmands, only adjust velocity:
```sh
python3 midi.py --inputmididevicename "KOMPLETE" --inputmididevicename2 "MPK mini" --outputmididevicename "U2MIDI" --midi_max_value 80 --midi_exponent 0.60
```

Full Configuration with velocity adjustment, an altertnative input name and midi channel control over second midi device over program change:
```sh
python3 midi.py --inputmididevicename "KOMPLETE" --inputmididevicename2 "MPK mini" --inputmididevicenamemidichannel "LPD8" --outputmididevicename "U2MIDI" --midi_max_value 80 --midi_exponent 0.60
```

Here's a breakdown of each argument:
```sh
--inputmididevicename "KOMPLETE": Specifies the name of the first input MIDI device as "KOMPLETE".
--inputmididevicename2 "MPK mini": Specifies the name of the second input MIDI device as "MPK mini".
--inputmididevicenamemidichannel "LPD8": Specifies the name of the MIDI device for a specific MIDI channel as "LPD8". (optional)
--outputmididevicename "U2MIDI": Specifies the name of the output MIDI device as "U2MIDI".
--midi_max_value 80: Sets the maximum MIDI value to 80.
--midi_exponent 0.60: Sets the exponent value for MIDI processing to 0.60.
```


# 6. Set up the autostart from your midi script:
   
   ```sh
   chmod 775 /home/user1/start-midi.sh

   crontab -e

   # Input this in the crontab file:
   @reboot sh /home/user1/start-midi.sh
   ```

   ### Configuration Setup


## Thanks

Special thanks to @georg-zeiser!
Source: https://github.com/georg-zeiser/midi-velocity-mapper


