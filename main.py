import os
import subprocess
import sys
import time
from pathlib import Path
import re

import colorama
from colorama import Fore, Style


colorama.init(autoreset=True)

BASE_DIR = Path(__file__).resolve().parent
ADB = BASE_DIR / "adb.exe"
SCRCPY = BASE_DIR / "scrcpy.exe"


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def display_banner() -> None:
    banner = r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ███████╗ █████╗ ██╗███╗   ███╗    ████████╗███████╗ ██████╗██╗  ██╗      ║
║     ╚══███╔╝██╔══██╗██║████╗ ████║    ╚══██╔══╝██╔════╝██╔════╝██║  ██║      ║
║       ███╔╝ ███████║██║██╔████╔██║       ██║   █████╗  ██║     ███████║      ║
║      ███╔╝  ██╔══██║██║██║╚██╔╝██║       ██║   ██╔══╝  ██║     ██╔══██║      ║
║     ███████╗██║  ██║██║██║ ╚═╝ ██║       ██║   ███████╗╚██████╗██║  ██║      ║
║                                                                              ║
║                                   Z A I M   T E C H                          ║
║                          Ethical Hacking & Cyber Security                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  DISCLAIMER: For educational purposes only.                                  ║
║  Use only on systems you own or are authorized to test.                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                               Made by Zaim Sheali       KE                   ║
║                     Follow me on Instagram: @king_zaim001                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(Fore.CYAN + banner)


def loading_dots(text: str, cycles: int = 4, delay: float = 0.3) -> None:
    for _ in range(cycles):
        for dots in range(4):
            sys.stdout.write(f"\r{text}{'.' * dots}   ")
            sys.stdout.flush()
            time.sleep(delay)
    sys.stdout.write("\r" + " " * (len(text) + 6) + "\r")
    sys.stdout.flush()


def run_adb(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ADB), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def run_scrcpy(*args: str) -> bool:
    try:
        process = subprocess.Popen(
            [str(SCRCPY), *args],
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if process.stdout is not None:
            for line in process.stdout:
                print(Fore.GREEN + line.rstrip())

        return_code = process.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, process.args)
        return True

    except FileNotFoundError:
        print(Fore.RED + "\nFailed to start scrcpy. Please ensure it is installed and try again.")
        return False
    except subprocess.CalledProcessError as error:
        print(Fore.RED + "\nFailed to start scrcpy. Please ensure it is installed and try again.")
        print(Fore.RED + f"scrcpy exited with code {error.returncode}.")
        return False


def get_connected_devices() -> list[str]:
    result = run_adb("devices")
    lines = result.stdout.strip().splitlines()
    return [line.strip() for line in lines[1:] if line.strip()]


def show_devices() -> list[str]:
    devices = get_connected_devices()
    if not devices:
        print(Fore.RED + "No devices found. Please connect a device and try again.")
        return []

    print(Fore.GREEN + "Connected devices:")
    for device in devices:
        print(Fore.GREEN + device)
    return devices

def get_android_ip() -> str | None:
    try:
        # Run adb command to get wlan0 IP info
        output = subprocess.check_output(
            ["adb", "shell", "ip", "-f", "inet", "addr", "show", "wlan0"],
            text=True,
            stderr=subprocess.STDOUT,
        )

        # Extract IP address matching pattern (e.g., 192.168.1.50)
        match = re.search(r"inet\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output)
        if match:
            return match.group(1)
        return None

    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def connection_menu() -> None:
    while True:
        clear_screen()
        display_banner()
        print(Fore.YELLOW + "1. By serial number\n")
        print(Fore.YELLOW + "2. By IP address (wireless connection)\n")
        print(Fore.YELLOW + "3. Connect via USB\n")
        print(Fore.YELLOW + "4. Enable wireless connection")
        print(Fore.YELLOW + "   Use this after connecting by USB so you can switch to wireless\n")
        print(Fore.YELLOW + "5. Back to main menu\n")

        try:
            choice = input(Fore.GREEN + "Enter your choice (1-5): " + Style.RESET_ALL).strip()
        except KeyboardInterrupt:
            print(Fore.RED + "\nConnection menu interrupted by user.")
            return

        if choice == "1":
            try:
                devices = show_devices()
                if not devices:
                    return

                serial_number = input(
                    Fore.GREEN + "Enter the device serial number: " + Style.RESET_ALL
                ).strip()
                if not serial_number:
                    print(Fore.RED + "No serial number entered.")
                    return

                print(Fore.YELLOW + f"Starting connection to {serial_number}...")
                loading_dots("Connecting")
                run_scrcpy(f"--serial={serial_number}")
                return

            except FileNotFoundError:
                print(Fore.RED + "Failed to run adb. Please ensure it is installed and try again.")
                return
            except subprocess.CalledProcessError as error:
                print(Fore.RED + "Failed to list connected devices.")
                if error.stderr:
                    print(Fore.RED + error.stderr.strip())
                return

        if choice == "2":
            try:
                ip_address = input(
                    Fore.GREEN
                    + "Enter the target IP address (example: 192.168.1.100:5555): "
                    + Style.RESET_ALL
                ).strip()
                if not ip_address:
                    print(Fore.RED + "No IP address entered.")
                    return

                print(Fore.YELLOW + "Starting connection to the target...")
                loading_dots("Connecting")
                result = run_adb("connect", ip_address)
                print(Fore.GREEN + f"\n{result.stdout.strip()}")

                print(Fore.GREEN + f"Successfully connected to {ip_address}!")
                print(Fore.GREEN + "Starting scrcpy...")
                loading_dots("Processing")
                run_scrcpy(f"--tcpip={ip_address}")
                return

            except FileNotFoundError:
                print(Fore.RED + "Failed to run adb. Please ensure it is installed and try again.")
                return
            except subprocess.CalledProcessError as error:
                print(
                    Fore.RED
                    + f"\nFailed to connect to {ip_address}. Please check the IP address and try again."
                )
                if error.stderr:
                    print(Fore.RED + error.stderr.strip())
                return

        if choice == "3":
            try:
                devices = show_devices()
                if not devices:
                    return

                print(Fore.YELLOW + "Starting connection to the device via USB...")
                loading_dots("Processing")
                print(Fore.GREEN + "Starting scrcpy...")
                loading_dots("Processing")
                run_scrcpy("-d")
                return

            except FileNotFoundError:
                print(Fore.RED + "Failed to run adb. Please ensure it is installed and try again.")
                return
            except subprocess.CalledProcessError as error:
                print(Fore.RED + "Failed to list connected devices.")
                if error.stderr:
                    print(Fore.RED + error.stderr.strip())
                return

        if choice == "4":
            try:
                devices = show_devices()
                if not devices:
                    return

                print(Fore.YELLOW + "Enabling wireless ADB on the connected device...")
                loading_dots("Processing")
                ip = get_android_ip()
                if not ip:
                    print(Fore.RED + "Failed to get device IP address.")
                    return
                result = run_adb("tcpip", "5555")
                run_adb("connect", f"{ip}:5555")
                print(Fore.GREEN + f"\n{result.stdout.strip()}")
                print(Fore.GREEN + "Wireless ADB is now enabled on port 5555.")
                print(Fore.GREEN + "Disconnect USB, then connect using: adb connect <device-ip>:5555")
                input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
                return

            except FileNotFoundError:
                print(Fore.RED + "Failed to run adb. Please ensure it is installed and try again.")
                return
            except subprocess.CalledProcessError as error:
                print(Fore.RED + "\nFailed to enable wireless ADB.")
                if error.stderr:
                    print(Fore.RED + error.stderr.strip())
                return

        if choice == "5":
            return

        print(Fore.RED + "Invalid choice. Please enter 1, 2, 3, 4, or 5.")
        time.sleep(1)


def camera_menu() -> None:
    options = {
        "1": ("Front Camera", "--video-source=camera", "--camera-facing=front", "--no-audio"),
        "2": ("Back Camera", "--video-source=camera", "--camera-facing=back", "--no-audio"),
        "3": (
            "Front Camera and Recording",
            "--video-source=camera",
            "--camera-facing=front",
            "--record=output.mp4",
        ),
        "4": (
            "Back Camera and Recording",
            "--video-source=camera",
            "--camera-facing=back",
            "--record=output.mp4",
        ),
        "5": (
            "Mic and Front Camera",
            "--video-source=camera",
            "--camera-facing=front",
            "--audio-source=mic",
        ),
        "6": (
            "Mic and Back Camera",
            "--video-source=camera",
            "--camera-facing=back",
            "--audio-source=mic",
        ),
        "7": ("Screen Recording", "--record=output.mp4"),
    }

    while True:
        clear_screen()
        display_banner()
        print(Fore.YELLOW + "1. Front Camera                         5. Mic and Front Camera\n")
        print(Fore.YELLOW + "2. Back Camera                          6. Mic and Back Camera\n")
        print(Fore.YELLOW + "3. Front camera and recording mp4       7. Screen recording\n")
        print(Fore.YELLOW + "4. Back camera and recording mp4        8. Back to main menu\n")

        try:
            choice = input(Fore.GREEN + "\nEnter your choice (1-8): " + Style.RESET_ALL).strip()
        except KeyboardInterrupt:
            print(Fore.RED + "\nCamera menu interrupted by user.")
            return

        if choice == "8":
            return

        if choice not in options:
            print(Fore.RED + "Invalid choice. Please enter a number from 1 to 8.")
            time.sleep(1)
            continue

        label, *scrcpy_args = options[choice]
        print(Fore.GREEN + f"Starting {label.lower()}...")
        loading_dots("Processing")
        run_scrcpy(*scrcpy_args)
        return


def disconnect() -> None:
    try:
        print(Fore.YELLOW + "Disconnecting from the device...")
        loading_dots("Disconnecting")
        result = run_adb("disconnect")
        print(Fore.GREEN + f"\n{result.stdout.strip()}")
    except FileNotFoundError:
        print(Fore.RED + "Failed to disconnect. Please ensure adb is installed and try again.")
    except subprocess.CalledProcessError as error:
        print(Fore.RED + "\nFailed to disconnect. Please ensure adb is installed and try again.")
        if error.stderr:
            print(Fore.RED + error.stderr.strip())


def get_apps() -> None:
    while True:
        clear_screen()
        display_banner()
        print(Fore.YELLOW + "1. Get installed apps\n")
        print(Fore.YELLOW + "2. Back to main menu\n")

        try:
            choice = input(Fore.GREEN + "\nChoose an option (1-2): " + Style.RESET_ALL).strip()
        except KeyboardInterrupt:
            print(Fore.RED + "\nApp menu interrupted by user.")
            return

        if choice == "1":
            try:
                result = run_adb("shell", "pm", "list", "packages")
                packages = [line.strip() for line in result.stdout.splitlines() if line.strip()]
                print(Fore.GREEN + "Installed apps:")
                for package in packages:
                    print(Fore.GREEN + package)
                input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
                return
            except FileNotFoundError:
                print(
                    Fore.RED
                    + "Failed to retrieve installed apps. Please ensure adb is installed and try again."
                )
                return
            except subprocess.CalledProcessError as error:
                print(
                    Fore.RED
                    + "\nFailed to retrieve installed apps. Please ensure adb is installed and try again."
                )
                if error.stderr:
                    print(Fore.RED + error.stderr.strip())
                return

        if choice == "2":
            return

        print(Fore.RED + "Invalid choice. Please enter 1 or 2.")
        time.sleep(1)


def send_command() -> None:
    while True:
        try:
            command = input(
                Fore.GREEN
                + "\nEnter the command to send to the device (or type 'exit' to return): "
                + Style.RESET_ALL
            ).strip()
        except KeyboardInterrupt:
            print(Fore.RED + "\nCommand entry interrupted by user.")
            return

        if command.lower() == "exit":
            return

        try:
            result = run_adb("shell", command)
            print(Fore.GREEN + f"\nCommand output:\n{result.stdout.strip()}")
            input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
            return
        except FileNotFoundError:
            print(Fore.RED + "Failed to execute command. Please ensure adb is installed and try again.")
            time.sleep(1)
            return
        except subprocess.CalledProcessError as error:
            print(Fore.RED + "\nFailed to execute command. Please ensure adb is installed and try again.")
            if error.stderr:
                print(Fore.RED + error.stderr.strip())
            time.sleep(1)    
            return


def get_device_info() -> None:
    try:
        result = run_adb("shell", "getprop")
        print(Fore.GREEN + "Device information:")
        print(Fore.GREEN + result.stdout.strip())
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + "Failed to retrieve device information. Please ensure adb is installed and try again.")
    except subprocess.CalledProcessError as error:
        print(Fore.RED + "\nFailed to retrieve device information. Please ensure adb is installed and try again.")
        if error.stderr:
            print(Fore.RED + error.stderr.strip())

def show_message(title:str, msg:str):
    try:
        run_adb("shell", f"am start -n com.android.chrome/com.google.android.apps.chrome.Main -a android.intent.action.VIEW -d \"data:text/html,%3C%21DOCTYPE%20html%3E%3Chtml%3E%3Cbody%20style%3D%27background%3Ablack%3Bcolor%3Awhite%3Btext-align%3Acenter%3Bpadding-top%3A100px%3Bfont-family%3Asans-serif%3B%27%3E%3Ch1%20style%3D%27color%3Ared%3Bfont-size%3A40px%3B%27%3E{title}%3C%2Fh1%3E%3Ch2%3E{msg}%3C%2Fh2%3E%3C%2Fbody%3E%3C%2Fhtml%3E\" -f 0x00080000")
    except FileNotFoundError:
        print(Fore.RED + "Failed to show message. Please ensure adb is installed and try again.")
    except subprocess.CalledProcessError as error:
        print(Fore.RED + "\nFailed to show message. Please ensure adb is installed and try again.")
        if error.stderr:
            print(Fore.RED + error.stderr.strip())

def main() -> None:
    while True:
        clear_screen()
        display_banner()
        print(Fore.YELLOW + "\n1. Connect to a device               5. Get installed apps\n")
        print(Fore.YELLOW + "\n2. Access camera                     6. Send command to device\n")
        print(Fore.YELLOW + "\n3. Disconnect from device            7. Send message to device\n")
        print(Fore.YELLOW + "\n4. Get device information            8. Mirror\n")
        print(Fore.RED + "\n9. Exit\n")


        try:
            choice = input(Fore.GREEN + "Choose an option (1-9): " + Style.RESET_ALL).strip()
        except KeyboardInterrupt:
            print(Fore.RED + "\nOperation interrupted by user.")
            return

        if choice == "1":
            connection_menu()
            continue
        if choice == "2":
            camera_menu()
            continue
        if choice == "3":
            disconnect()
            continue
        if choice == "4":
            get_device_info()
            continue
        if choice == "5":
            get_apps()
            continue
        if choice == "6":
            send_command()
            continue
        if choice == "7":
            title = input(Fore.GREEN + "Enter the title of the message: " + Style.RESET_ALL).strip()
            msg = input(Fore.GREEN + "Enter the message content: " + Style.RESET_ALL).strip()
            if title and msg:
                loading_dots("Sending message")
                show_message(title, msg)
                print(Fore.GREEN + "Message sent successfully!")
                time.sleep(2)
            else:
                print(Fore.RED + "Title and message cannot be empty.")
            continue
        if choice == "8":
            try:
                run_scrcpy()
            except Exception as error:
                print(Fore.RED + f"Failed to run scrcpy. Error: {error}")
            continue
        if choice == "9":
            print(Fore.YELLOW + "Exiting the program.")
            return

        print(Fore.RED + "Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, 8, or 9.")
        time.sleep(1)


if __name__ == "__main__":
    main()
