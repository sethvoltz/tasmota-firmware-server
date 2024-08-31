# Firmware Server for Tasmota OTA

This is a simple server that serves Tasmota firmware to Tasmota devices for OTA updates.

> **NOTE:** Do not run updates from within Arc browser. The "smart" feature to open the OTA tab in a side-by-side pane messes up the update process and can cause it to update twice, or possibly stall
it in an unstable state.

## Setup

```bash
pyenv virtualenv 3.10.13 tasmota
pyenv activate tasmota
pip install -r requirements.txt
```

## Usage

Get minimal firmware from: https://ota.tasmota.com/tasmota/release/
Get TLS from https://github.com/tasmota/install/blob/firmware/firmware/unofficial/tasmota-tls.bin.gz

Put both in the `firmware/` directory as `tasmota-minimal.bin.gz` and `tasmota-tls.bin.gz` respectively. Optionally, you can save the firmware with a version number appended to them, then symlink to the expected names. This way you can keep multiple versions of the firmware around in case you need to roll back.

Usage:
```bash
python server.py -d <net_iface>   (default: eth0)
# or
python server.py -i <ip_address>
```

Example:
```bash
python server.py -d wlan0
# or
python server.py -i 192.168.1.10
```

Then from within Tasmota, go to the firmware update page and use

`http://<your_ip>:38266/tasmota-tls.bin.gz`. This will check the TLS, see it's too big, OTA the minimal, then OTA the TLS.

## Wish List

- [ ] Only store the firmware by version and detect unversioned requests, then serve the latest version.

## Credits

I found this code by Gennaro Tortone on the Tasmota site but it was broken. I have cleaned it up and made it work with some additional changes, including this Readme and setup instructions for recent Python.
