# How to Install on Raspberry Pi
### Materials :
- SD card, above 16 GB
- Raspberry Pi
- Monitor, keyboard, mouse all wired, 
- Screen for Raspberry Pi
### Steps for Pi set up: 
1) On computer, download the Raspberry Pi Imager
2) Once downloaded open the Raspberry Pi Imager 
3) Insert SD card into computer
4) Select the Pi Raspbian OS, select the inserted SD card, and press Burn
5) Remove SD from computer and place it into Pi
6) Complete location, language, and wifi set up. Set username as pi and password as pi
   - This is important as the username will be the main directory set up under ~/home

Steps for application set up:
Connect to internet on the pi by selected the WiFi icon and inputting network information
Open terminal and run the following commands
pip install muselsl==2.0.0
sudo apt-get install libatlas-base-dev
The following steps will also be completed in the terminal and focus on replacing the liblsl library. 
cd /home/pi/.local/lib/python3.7/site-packages
wget ftp://sccn.ucsd.edu/pub/software/LSL/SDK/liblsl-C-C++-1.11.zip
unzip liblsl-C-C++-1.11.zip
sudo cp liblsl-bcm2708.so /home/pi/.local/lib/python3.72/site-packages/pylsl/liblsl32.so
The following step configures bluetooth
sudo setcap 'cap_net_raw,cap_net_admin+eip' `which hcitool`
Open terminal and type the following commands:
Git clone git@github.com:davidbichara/MuseAlarmPi.git
Go to the MuseAlarmPi directory and open the museStream.py file
Replace the address in quotations in the record_direct function to be the MAC address of the muse. 

Autolaunch:


Alternatives for other systems:
Uvicmuse
#Sudo python -m pip install “kivy[base]”
Sudo pip install pylsl==1.10.5 pygatt 
Sudo pip install --force-reinstall uvicmuse==3.3.3
sudo apt-get install libatlas-base-dev
Replace liblsl lib
cd /home/pi/.local/lib/python3.7/site-packages
wget ftp://sccn.ucsd.edu/pub/software/LSL/SDK/liblsl-C-C++-1.11.zip
unzip liblsl-C-C++-1.11.zip
sudo cp liblsl-bcm2708.so /home/pi/.local/lib/python3.72/site-packages/pylsl/liblsl32.so
