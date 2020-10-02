# MicroPython OTA Update

### Features
* Works for MicroPython v1.13
* Only updates scripts in the directory specified (e.g. `/project`)

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

```python
import os
os.mkdir('next')
os.rename('/project/.version', '/next/.version_on_reboot')
```