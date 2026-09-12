# ZaimDroid

![Security Tool](https://img.shields.io/badge/Focus-Android%20Security-111827?logo=android&logoColor=3DDC84)
![Authorized Testing](https://img.shields.io/badge/Use-Authorized%20Testing-dc2626?logo=shield&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)

> **ZAIM TECH // ANDROID SECURITY LAB**

ZaimDroid is a Windows command-line utility for Android security testing, mobile awareness demonstrations, and authorized device administration through **ADB** and **scrcpy**.

It helps students, developers, and security testers inspect their own Android devices, understand debugging exposure, and document controlled security-lab exercises.

## Rules Of Engagement

Only use ZaimDroid in a legal, controlled environment:

- Test devices you own or have written permission to assess.
- Get consent before mirroring screens, opening cameras, recording, or running commands.
- Use a private lab network for wireless debugging.
- Do not use the tool to access, monitor, record, or control another person's device.
- Remove test recordings and sensitive device data after an exercise.

You are responsible for following all applicable laws, policies, and organizational rules.

## Security And Awareness Uses

ZaimDroid can support safe demonstrations and defensive work such as:

- Showing why USB debugging should be disabled when it is not needed.
- Demonstrating the difference between an authorized and unauthorized ADB state.
- Inspecting device properties and installed packages on a test phone.
- Reviewing the risks of wireless debugging on an untrusted network.
- Recording a consented test scenario for training or incident documentation.
- Practicing mobile-device assessment workflows in a personal lab.

ZaimDroid is not an exploit framework, credential-stealing tool, or permission-bypass utility.

## Capabilities

- Connect to an Android device over USB.
- Connect to an authorized device using its serial number.
- Connect over a TCP/IP address.
- Pair and connect through Android Wireless Debugging QR code.
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
- The built `ZaimDroid.exe` Windows executable, or Python 3.10+ for development.
- An Android device with USB debugging enabled.
- For QR pairing, Android Wireless Debugging and a shared Wi-Fi network.

The one-file executable contains the required Python application, ADB, scrcpy, DLL files, `scrcpy-server`, `scrcpy.png`, and `disconnected.png`. You do not need to install Python, ADB, scrcpy, or separate DLL files when using the executable.

## Installation

[![Download for Windows](https://img.shields.io/badge/Download-Windows-0078D6?logo=windows&logoColor=white)](https://github.com/zaim-tech/ZaimDroid/releases/download/0.1/main.exe)

1. Download the [ZaimDroid Windows executable](https://github.com/zaim-tech/ZaimDroid/releases/download/0.1/main.exe).
2. Place it in a folder of your choice.
3. Connect your authorized Android device and unlock it.
4. Run the executable.
5. Accept the USB debugging authorization prompt on the device.

The main menu contains these options:

| Option | Action |
| --- | --- |
| 1 | Open device connection options |
| 2 | Open camera and recording options |
| 3 | Disconnect ADB connections |
| 4 | Display device information |
| 5 | List installed apps/packages |
| 6 | Send a command through `adb shell` |
| 7 | Send a message to the device browser |
| 8 | Mirror the device with scrcpy |
| 9 | Exit the program |

## USB Connection

1. Enable **Developer options** and **USB debugging** on the Android device.
2. Connect the device with a USB cable.
3. Run the ZaimDroid `.exe` file.
4. Choose `1`, then choose `3. Connect via USB`.

If the device is not shown, restart ZaimDroid, reconnect the device, and make sure the device is authorized.

## Wireless Connection

Use wireless debugging only on a network you trust and only for devices you are authorized to manage.

1. Enable wireless debugging on the Android device.
2. Find the device IP address and ADB port.
3. Start ZaimDroid and choose `1`, then `2. By IP address`.
4. Enter an address such as `192.168.1.100:5555`.

The device and computer must normally be connected to the same network. If Android displays a pairing code or pairing port, complete that pairing using the Android platform-tools workflow first.

### Wireless Menu Options

- **By IP address:** enter the complete address in the format `device-ip:5555`, for example `192.168.1.100:5555`.
- **Pair using QR code:** choose option `4`, then scan the terminal QR code from Android **Developer options > Wireless debugging > Pair device with QR code**. The tool discovers the phone's pairing service, runs `adb pair`, discovers the connection service, and runs `adb connect` automatically.
- **Enable wireless connection:** connect by USB first, choose this option, then disconnect the USB cable and run `adb connect <device-ip>:5555` from an authorized terminal.

The computer and phone must be on the same Wi-Fi network. QR pairing requires Android platform-tools with mDNS support; the bundled ADB executable is used by the Windows build.

## Build From Source

Install the Python dependencies from `requirements.txt`, then build the one-file Windows executable:

```powershell
pip install -r requirements.txt
pyinstaller --clean --noconfirm ZaimDroid.spec
```

The finished executable is written to `dist\ZaimDroid.exe`. The spec file embeds ADB, scrcpy, their DLL files, `scrcpy-server`, and both PNG assets.

## Camera and Recording

Choose `2. Access camera` from the main menu. Available actions include:

- Front camera.
- Back camera.
- Front or back camera recording.
- Camera with microphone input.
- Screen recording.

Recordings are written to `output.mp4` in the current working directory. A later recording can replace an earlier file with the same name, so rename recordings you want to keep.

Camera and microphone options depend on the Android version, device permissions, and the bundled scrcpy version.

## Authorized Security Checks

The command menu sends input through `adb shell`. Examples for your own test device:

```text
getprop ro.product.model
wm size
df -h
pm list packages
```

These read-only examples are suitable for a personal test device:

```text
getprop ro.product.model
getprop ro.build.version.release
settings get global adb_enabled
wm size
df -h
pm list packages
```

Review the output as test evidence, and avoid commands that delete data, change security settings, install unknown software, or modify a device unless you fully understand their effect and have permission.

## Safe Testing Workflow

1. Define the device, purpose, and test window.
2. Confirm written authorization and user consent.
3. Prefer USB debugging on a private test setup.
4. Record only the evidence needed for the exercise.
5. Disconnect the device and disable debugging when finished.
6. Delete sensitive recordings and document the findings.

## Troubleshooting

### Required files cannot be found

Download the complete ZaimDroid Windows release again. The ADB and scrcpy files are bundled with the executable package.

### Device is unauthorized

Unlock the device, accept the USB debugging prompt, then run the connection option again.

### No device is listed

Try another USB cable or port, confirm USB debugging is enabled, and restart ZaimDroid.

### scrcpy does not start

Download the complete ZaimDroid Windows release again and check that the connected device is authorized.

### Camera or microphone fails

The device may not expose the requested camera/audio source to scrcpy. Check Android permissions and verify that the bundled scrcpy version supports the selected feature.

## Support The Project

If ZaimDroid is useful to you, please star the repository and share it with others.

Made with love by **Zaim Sheali**.

## License

No license has been specified yet. Add a license before distributing ZaimDroid publicly.
