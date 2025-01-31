# pi-midi-velocity-curve-changer
## Description 
This little python script will adjust the midi velocity curve from your keyboard to fix velocity issues if your keyboard does not handle the velocity well. 
Setup is like: Keyboard -> USB -> Rasbperry PI -> USB to Midi -> Midi In from your Synthesizer / MPC.

I had the following problem:
I have a Native Instruments KOMPLETE KONTROL A49 keyboard and an MPC ONE.
Although I think the keyboard is pretty good, it has a terrible velocity curve which unfortunately is not standalone customizable. I still have an old Raspberry Pi lying around and a USB-to-Midi adapter. With this Python script it was possible to put the Raspberry Pi between the keyboard and the MPC one to function as a “velocity adjuster”.

Optional: If you possess an additional midi controller like the Akai LPD8 Controller, you can utilize the program change MIDI message to manipulate the MIDI channel from your input keyboard device. This functionality allows the script to provide the capability to change the MIDI channel for your keyboard.

In the experimental folder are a few attempts to display the Velocity Curve on a MiniDisplay using PyGame. Currently this does not work well and is not necessary for the functionality. 

You also need: 
1. USB Keyboard
2. A USB to Midi device (e.g.: CME U2MIDI Pro)
3. Raspberry Pi
4. (Optional) Akai LPD8 Controller or a other device which supports program change midi messages.

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

# 1. Copy the midi.py and start-midi.sh file on your raspberry pi for example: /home/youruser/

# 2. Install the python libs:
   
   ```sh
   pip install mido
   pip install math
   ```

# 3. Identify Your MIDI Devices

Run the script to list available input and output ports. The script will print the names of all connected MIDI devices
Simply use a part of the name to store this in the parameters as a search word. 

## 4. Configuration

Open the start-midi.sh and configure your settings:

Minimum Startup Commmands, only adjust velocity:
```sh
python3 midi.py --inputmididevicename "KOMPLETE" --outputmididevicename "U2MIDI" --midi_max_value 80 --midi_exponent 0.60
```

Full Configuration with velocity adjustment and midi channel control over second midi device program change events:
```sh
python3 midi.py --inputmididevicename "KOMPLETE" --inputmididevicenamemidichannel "LPD8" --outputmididevicename "U2MIDI" --midi_max_value 80 --midi_exponent 0.60
```

Here's a breakdown of each argument:
```sh
--inputmididevicename "KOMPLETE": Specifies the name of your MIDI Keyboard device as "KOMPLETE".
--outputmididevicename "U2MIDI": Specifies the name of the output MIDI adapter as "U2MIDI".
--midi_max_value 80: Sets the maximum MIDI value to 80.
--midi_exponent 0.60: Sets the exponent value for MIDI processing to 0.60.
--inputmididevicenamechannelcontrol "LPD8": Specifies the name of the MIDI device to control with the program_change event the midi channel for inputmididevicename. (optional)
```


# 6. Set up the autostart from your midi script:
   
   ```sh
   chmod 775 /home/youruser/start-midi.sh

   crontab -e

   # Input this in the crontab file:
   @reboot sh /home/youruser/start-midi.sh
   ```

## Thanks

Special thanks to @georg-zeiser!
Source: https://github.com/georg-zeiser/midi-velocity-mapper


