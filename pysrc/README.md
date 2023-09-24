## Python source for WiFi enabled switch

#### Steps to setup

1. Flash Micropython on to the NodeMCU board
	Download the latest Micropython firmware for ESP8266 from [here](https://micropython.org/download/ESP8266_GENERIC/). The latest firmware as of the time of this README was ESP8266_GENERIC-20230426-v1.20.0.bin
2. Clone this repository and cd into pysrc/
	`cd pysrc/`
3. Create a python virtual environment and install the esptool (for flashing the firmware) and ampy (utility for storing/getting files from the board)
	```
	python3 -m venv venv/
	source venv/bin/activate
	pip install -r requirements.txt
	```
4. Connect your board to your machine and find the serial port on your machine to which the board is connected to. Erase any existing data on the flash memory and flash the new micropython firmware onto the board
	```
	esptool.py -p /dev/cu.usbserial-1 erase_flash
	esptool.py -p /dev/cu.usbserial-1 -b 115200 write_flash --flash_size=detect 0 ESP8266_GENERIC-20230426-v1.20.0.bin
	```
   Replace /dev/cu-usbserial-1 with the port on your machine and ESP8266_GENERIC-20230426-v1.20.0.bin with the path of the Micropython firmware for ESP8266 you downloaded in Step 1
