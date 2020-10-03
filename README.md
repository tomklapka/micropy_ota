# MicroPython OTA Update
This is a modified version of [micropython-ota-updater](https://github.com/rdehuyss/micropython-ota-updater) to
work with MicroPython v1.13 and devices with lower memory.

I wrote this for the ESP8622, but it should definitely work
with the ESP32 or any chips with RAM equal to or greater than the
ESP8622.


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
1. Specify the correct creds including:
   * WiFi SSID & password
   * GitHub repo to update from
2. Use Tags to specify which push is the 'latest' version
3. Run the equivalent code that's in `main.test()`


## How it Works

**Important Params**

| Param      | Description                                             |
|:-----------|:--------------------------------------------------------|
| `main_dir` | The directory containing the code you want auto-updated |


### Step 1) Check for Latest Version
1. Check to see if the GitHub repo has a 'latest' version
2. Continue if there is a new version available; exit the update otherwise
3. Create a file that stores the new version instructions
   * Create `/next/.version_on_reboot` directory in the project root
   * Store the version number as text in the file (e.g. `1.0.1`)
4. Continue to the next step


### Step 2) Download the Latest Version
1. Check to see if the `/next/.version_on_reboot` file exists
2. Open the file and get the version number saved
3. Download all the files into the `/next/` directory
4. Rename the `/next/.version_on_reboot` file to `/next/.version`
5. Rename `/next/` directory to `/project/` (or whatever main_dir is set to)



## Debugging

### Re-test Download | REPL
Run the following to un-do the download.

```python
import os
os.mkdir('next')
os.rename('/project/.version', '/next/.version_on_reboot')
```