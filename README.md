# pi-midi-velocity-curve-changer

1. Setup the midi.py file on your raspberry pi
2. Install the python libs:
   pip install mido
   pip install math
3. Start the python script and copy the full name from your usb input device (keyboard) and your usb output device (usb to midi).
4. (optional) adjust the parameters from the function in the script for your optimal velocity settings.
5. Set up the autostart:
   crontab -e
   chmod 775 /home/user1/midi.sh
   @reboot sh /home/user1/midi.sh
6. Reboot   

Special thanks to @georg-zeiser!
Source: https://github.com/georg-zeiser/midi-velocity-mapper


