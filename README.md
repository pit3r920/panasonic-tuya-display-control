# panasonic-tuya-display-control
## Python application based on Flask

Application allow you to control your Panasonic Smart TV, smart outlet and external display.

## Installation

### Libraries used in this project:

flask https://github.com/pallets/flask

panasonic_viera https://github.com/florianholzapfel/panasonic-viera

tinytuya https://github.com/jasonacox/tinytuya

monitorcontrol https://github.com/newAM/monitorcontrol


## Configuration
After setting up your Tuya devices configuration files are created in  %userprofile% folder.

```python 
tv = ""
id = ""
ip = ""
key = ""
```

Change values of:

tv - Panasonic TV IP address

id, ip and key - you can find these values in the devices.json file within %userprofile% folder.





Application at first is checking if any  devices (TV, Smart Outlet, TV) are configured properly - if any at the time of starting are not correctly configured they wouldn't appear.

## Known issues
### When turning the display off crash can occur - more exception handling is required.
