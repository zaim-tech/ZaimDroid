# ZaimDroid

ZaimDroid is a Windows command-line utility for managing and testing Android devices through **ADB** and **scrcpy**.

It provides a simple menu for authorized device administration, screen control, camera testing, device inspection, and Android shell commands.

## Disclaimer

Use ZaimDroid only with devices that you own or are explicitly authorized to test. Do not use it to access, monitor, record, or control another person's device without permission. You are responsible for following all applicable laws and policies.

## Features

- Connect to an Android device over USB.
- Connect to an authorized device using its serial number.
- Connect over a TCP/IP address.
- Mirror and control the device with scrcpy.
- Test the front or back camera.
- Record the screen or camera output to `output.mp4`.
- Record camera video with microphone input when supported by the device.
- List installed Android packages.
- Display Android device properties.
- Send authorized ADB shell commands.
- Disconnect ADB connections.

## Requirements

- Windows 10 or newer.
- Python 3.10 or newer if running from source.
- An Android device with USB debugging enabled.
- A USB cable for the first USB connection or Android wireless debugging configured on the same network.
- The following files in the project folder:
  - `adb.exe`
  - `scrcpy.exe`
  - scrcpy's required DLL files
  - `scrcpy-server`

The included ADB and scrcpy files are already referenced by `main.py` and are expected to be beside it.

## Installation

1. Open PowerShell in this project folder.
2. Install the Python dependency:

   ```powershell
   python -m pip install colorama
   ```

3. Connect your authorized Android device.
4. Unlock the device and accept the USB debugging authorization prompt.

## Run From Source

```powershell
python main.py
```

The main menu contains these options:

| Option | Action |
| --- | --- |
| 1 | Connect to a device by serial number, IP address, or USB |
| 2 | Open camera and recording options |
| 3 | Disconnect ADB connections |
| 4 | Display device information |
| 5 | List installed apps/packages |
| 6 | Send a command through `adb shell` |
| 7 | Exit the program |

## USB Connection

1. Enable **Developer options** and **USB debugging** on the Android device.
2. Connect the device with a USB cable.
3. Run `python main.py`.
4. Choose `1`, then choose `3. Connect via USB`.

If the device is not shown, run this from PowerShell to check its ADB status:

```powershell
.\adb.exe devices
```

The device should appear with the status `device`, not `unauthorized`.

## Wireless Connection

Use wireless debugging only on a network you trust and only for devices you are authorized to manage.

1. Enable wireless debugging on the Android device.
2. Find the device IP address and ADB port.
3. Start ZaimDroid and choose `1`, then `2. By IP address`.
4. Enter an address such as `192.168.1.100:5555`.

The device and computer must normally be connected to the same network. If Android displays a pairing code or pairing port, complete that pairing using the Android platform-tools workflow first.

## Camera and Recording

Choose `2. Access camera` from the main menu. Available actions include:

- Front camera.
- Back camera.
- Front or back camera recording.
- Camera with microphone input.
- Screen recording.

Recordings are written to `output.mp4` in the current working directory. A later recording can replace an earlier file with the same name, so rename recordings you want to keep.

Camera and microphone options depend on the Android version, device permissions, and the bundled scrcpy version.

## Useful Authorized Commands

The command menu sends input through `adb shell`. Examples for your own test device:

```text
getprop ro.product.model
wm size
df -h
pm list packages
```

Avoid commands that delete data, change security settings, install unknown software, or modify a device unless you fully understand their effect and have permission.

## Troubleshooting

### `adb.exe` cannot be found

Confirm that `adb.exe` is in the same folder as `main.py` or the built executable.

### Device is unauthorized

Unlock the device, accept the USB debugging prompt, then run the connection option again.

### No device is listed

Try another USB cable or port, confirm USB debugging is enabled, and check the output of:

```powershell
.\adb.exe devices
```

### scrcpy does not start

Confirm that `scrcpy.exe`, `scrcpy-server`, and all required scrcpy DLL files are present beside the program. Also check that the connected device is authorized.

### Camera or microphone fails

The device may not expose the requested camera/audio source to scrcpy. Check Android permissions and verify that the bundled scrcpy version supports the selected feature.

## Project Files

- `main.py`: ZaimDroid application source.
- `adb.exe`: Android Debug Bridge executable.
- `scrcpy.exe`: Android screen mirroring and control executable.
- `scrcpy-server`: scrcpy server used on the Android device.

## Support The Project

If ZaimDroid is useful to you, please star the repository and share it with other developers.

Made with love by **Zaim Sheali**.

## License

No license has been specified yet. Add a license before distributing ZaimDroid publicly.
