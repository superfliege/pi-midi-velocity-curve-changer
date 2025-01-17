# pi-midi-velocity-curve-changer
## Description 
This little python script will adjust the midi velocity curve from your keyboard to fix velocity issues if your keyboard does not handle the velocity well. 
Setup is like: Keyboard -> USB -> Rasbperry PI -> USB to Midi -> Midi In from your Synthesizer / MPC.

I had the following problem:
I have a Native Instruments KOMPLETE KONTROL A49 keyboard and an MPC ONE.
Although I think the keyboard is pretty good, it has a terrible velocity curve which unfortunately is not standalone. I still have an old Raspberry Pi lying around and a USB-to-Midi adapter. With this Python script it was possible to put the Raspberry Pi between the keyboard and the MPC one to function as a “velocity adjuster”.

You also need: 

1. USB Keyboard
2. A USB to Midi device (e.g.: CME U2MIDI Pro)


## Setup 

1. Setup the midi.py and midi.sh file on your raspberry pi
2. Install the python libs:
   
   pip install mido

   pip install math
4. Start the python script. The script will show you the name of your connected midi devices and will crash.
   Copy the full name from your usb input device (keyboard) and your usb output device (usb to midi).
5. (optional) adjust the parameters from the function in the script for your optimal velocity settings.
6. Set up the autostart from your midi script:
   
   chmod 775 /home/user1/midi.sh
   
   crontab -e
   
   Input this in the crontab file:
   
   @reboot sh /home/user1/midi.sh

   
8. Reboot

## Thanks

Special thanks to @georg-zeiser!
Source: https://github.com/georg-zeiser/midi-velocity-mapper


