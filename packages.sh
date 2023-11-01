#!/bin/bash

apt-get update  # Update package list

sudo wget https://raw.githubusercontent.com/arkh91/public_script_files/main/python.sh && chmod u+x python.sh && ./python.sh
echo -e "\033[32mPython script dowanloaded and installed.\033[m"
apt-get install -y net-tools python3-pip #package2 package3   Replace with actual package names
pip install pytz
