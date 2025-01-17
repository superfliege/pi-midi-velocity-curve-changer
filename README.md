# pi-midi-velocity-curve-changer

1. Setup the midi.py and midi.sh file on your raspberry pi
2. Install the python libs:
   pip install mido
   pip install math
3. Start the python script. The script will show you the name of your connected midi devices and will crash.
   Copy the full name from your usb input device (keyboard) and your usb output device (usb to midi).
5. (optional) adjust the parameters from the function in the script for your optimal velocity settings.
6. Set up the autostart from your midi script:
   chmod 775 /home/user1/midi.sh
   crontab -e
   Input this in the crontab file: 
   @reboot sh /home/user1/midi.sh
8. Reboot   

Special thanks to @georg-zeiser!
Source: https://github.com/georg-zeiser/midi-velocity-mapper


