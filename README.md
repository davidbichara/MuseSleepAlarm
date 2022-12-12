# How to Install on Raspberry Pi
### Materials :
- SD card, above 16 GB
- Raspberry Pi
- Monitor, keyboard, mouse all wired, 
- Screen for Raspberry Pi

### Steps for Raspberry Pi configuration: 
1) On computer, download the Raspberry Pi Imager
2) Once downloaded open the Raspberry Pi Imager 
3) Insert SD card into computer
4) Select the Pi Raspbian OS, select the inserted SD card, and press Burn
5) Remove SD from computer and place it into Pi
6) Complete location, language, and wifi set up. Set username as pi and password as pi
   - This is important as the username will be the main directory set up under ~/home

### Steps for application set up on Raspberry Pi:
1) Connect to internet on the pi by selected the WiFi icon and inputting network information
2) Open terminal and run the following commands
   - ```pip install muselsl==2.0.0```
   - ```sudo apt-get install libatlas-base-dev```
3) The following steps will also be completed in the terminal and focus on replacing the liblsl library. 
   - ```cd /home/pi/.local/lib/python3.7/site-packages```
   - ```wget ftp://sccn.ucsd.edu/pub/software/LSL/SDK/liblsl-C-C++-1.11.zip```
   - ```unzip liblsl-C-C++-1.11.zip```
   - ```sudo cp liblsl-bcm2708.so /home/pi/.local/lib/python3.72/site-packages/pylsl/liblsl32.so```
4) The following step configures bluetooth
   - ```sudo setcap 'cap_net_raw,cap_net_admin+eip' `which hcitool```
5) Open terminal and type the following commands:
   - ```git clone git@github.com:davidbichara/MuseAlarmPi.git```
6) Check the paths which currently hold the value '/home/pi/Desktop/MuseSleep' with '.' or the equvalent path. 

### Steps for application set up on Laptop:
1) Install pip by following the documentation here: https://pip.pypa.io/en/stable/installation/
2) Open terminal and run the following commands
   - ```pip install muselsl==2.0.0```
3) Open terminal and type the following commands:
   - ```git clone git@github.com:davidbichara/MuseAlarmPi.git```
4) Check the paths which currently hold the value '/home/pi/Desktop/MuseSleep' with '.' or the equvalent path.

### Common Errors
1) Path errors
   - Repeat step 7 under 'steps for application set up on pi' 
2) bleak related exception
   - This exception occurs on windows and is relaetd to the bleak verison. 
   - Run ```pip install bleak==0.17.0```  
