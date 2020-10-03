# MicroPython OTA Update
This is a modified version of [micropython-ota-updater](https://github.com/rdehuyss/micropython-ota-updater) to
work with MicroPython v1.13 and devices with lower memory.

I wrote this for the ESP8266, but it should definitely work
with the ESP32 or any chips with RAM equal to or greater than the
ESP8266.


### Features
* Works for MicroPython v1.13
* Only updates scripts in the directory specified (e.g. `/project`)

### ToDo
* Be able to revert to the previous version
* Be able to download a specific version
* Failsafes
  * If no version exists - download the last stable version
  * If the device powers off mid update, revert to previous



## Usage

#### Helpful Params
| Param        | Description                                                      |
|:-------------|:-----------------------------------------------------------------|
| `main_dir`   | The directory containing the code you want auto-updated          |
| `wifi_ssd`   | The WiFi network name                                            |
| `wifi_pass`  | The WiFi network pass                                            |
| `github_url` | The URL to the GitHub repository the updates are downloaded from |

### TLDR Usage
1. Specify the Params (see [Setup & Prerequisites section](#setup--prerequisites))
2. Call `check_for_updates()` in `main.py` to check for new updates
3. Call `install_updates()` in `main.py` to download and install updates
4. Reboot the device




## Setup & Prerequisites
Make sure these steps are completed before you run the OTA.


### Set Credentials
Specify the required credentials including:
   * WiFi SSID & password
   * GitHub repo to update from

These credentials are currently in `main.py`.

If the chip is already connected to WiFi that step can be skipped - or ignored if you already
have a WiFi script you prefer to use.  Just be sure to check for a WiFi connection before running
the OTA.

The GitHub repo needs to be set to the repository the updates will be downloaded from.  The
repository must have the `main_dir` specified above as that is the data that will be downloaded.


### Use Tags to Specify the Latest Release
You must specify a 'latest' version in GitHub.  The code will query GitHub for the latest
repo release and if the release is newer than what is installed it will download the update.

You must use semantic versioning for this (e.g. `1.0.0`).  Below is a quick review of how to do this:

1. In Git specify  the version and number: `git tag -a "v1.0.0" -m "beta"`
2. Push the version number: `git push origin master --tags`
3. Login to GitHub and Publish the release
   * Click on the 'Tags' link
   * Click the version you want to publish
   * Click the 'Edit tag' button
   * Click 'Publish release'

You can view the current version with `git describe`.


## Logic
Below is how the script works.

### Checking for Updates
1. Call the `OTACheck` class and pass in the following arguments
   * 'github_url' - This the URL to the repository you want to download updates from
   * 'main_dir' - This is the directory that contains the updated code
2. Query GitHub for the latest repo version
3. If the version is newer than what is on the device
   * Create a `/next/` directory and save the newest version ID in `/next/.version_on_reboot`
4. Exit OTA

#### Download & Install Logic
1. Check to see if a `/next/.version_on_reboot` file exists
2. Open the file and get the version number saved
3. Query GitHub to get the files for that version number
4. Download all the files into the `/next/` directory
5. Rename the `/next/.version_on_reboot` file to `/next/.version`
6. Rename `/next/` directory to the 'main_dir' value
7. _Note: You will need to reboot the device `machine.reboot()` to apply the updates, but this has not been added to the code yet._


## Debugging

### Moving Files
Run `import move_files` in REPL to move and delete the specified files.  This is due to a
bug with PyCharm renaming all files inside sub-directories and moving them to /root.

### Re-test Download | REPL
Run the following to convince the script to re-download the GitHub files.

```python
import os
os.mkdir('next')
os.rename('/project/.version', '/next/.version_on_reboot')
```