from __future__ import annotations

import random
import string
import subprocess
import time
from pathlib import Path

import qrcode
from zeroconf import ServiceBrowser, ServiceInfo, Zeroconf

PAIRING_SERVICE = "_adb-tls-pairing._tcp.local."
CONNECT_SERVICE = "_adb-tls-connect._tcp.local."


def pair_device(adb_path: str | Path, ip: str, port: int, password: str) -> bool:
    command = [str(adb_path), "pair", f"{ip}:{port}", password]
    print(f"Running: adb pair {ip}:{port} {password}")
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.stderr:
        print(f"Error: {result.stderr.strip()}")
    return result.returncode == 0


def connect_device(adb_path: str | Path, ip: str, port: int) -> bool:
    command = [str(adb_path), "connect", f"{ip}:{port}"]
    print(f"Running: adb connect {ip}:{port}")
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.stderr:
        print(f"Error: {result.stderr.strip()}")
    return result.returncode == 0


class AdbPairingListener:
    def __init__(self, target_service_name: str):
        self.target_service_name = target_service_name
        self.ip_address: str | None = None
        self.port: int | None = None

    def remove_service(self, zeroconf, service_type: str, name: str) -> None:
        return None

    def add_service(self, zeroconf, service_type: str, name: str) -> None:
        if self.target_service_name not in name:
            return
        info = zeroconf.get_service_info(service_type, name)
        if info:
            self.on_service_found(info)

    def update_service(self, zeroconf, service_type: str, name: str) -> None:
        self.add_service(zeroconf, service_type, name)

    def on_service_found(self, info: ServiceInfo) -> None:
        addresses = info.parsed_addresses()
        if addresses:
            self.ip_address = addresses[0]
            self.port = info.port


def discover_service(
    service_type: str,
    target_name: str,
    timeout: int = 120,
) -> tuple[str | None, int | None]:
    zeroconf = Zeroconf()
    listener = AdbPairingListener(target_name)
    browser = ServiceBrowser(zeroconf, service_type, listener)
    del browser

    try:
        start_time = time.monotonic()
        while listener.ip_address is None and time.monotonic() - start_time < timeout:
            time.sleep(0.5)
    finally:
        zeroconf.close()

    return listener.ip_address, listener.port


def generate_random_string(length: int) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def generate_pairing_string(service_name: str, password: str) -> str:
    return f"WIFI:T:ADB;S:{service_name};P:{password};;"


def print_qr_code(payload: str) -> None:
    qr = qrcode.QRCode(border=2)
    qr.add_data(payload)
    qr.print_ascii(invert=True)


def qr_pair(adb_path: str | Path = "adb", timeout: int = 120) -> bool:
    service_name = f"adb-cli-{generate_random_string(6)}"
    password = generate_random_string(6)
    payload = generate_pairing_string(service_name, password)

    print("Starting ADB QR Code Pairing...\n")
    print("Scan this QR code in Android > Developer Options > Wireless Debugging > Pair device with QR code\n")
    print(f"Service Name: {service_name}")
    print(f"Password: {password}\n")
    print_qr_code(payload)
    print(f"\nWaiting for device to scan QR code (timeout {timeout}s)...")

    pair_ip, pair_port = discover_service(PAIRING_SERVICE, service_name, timeout)
    if not pair_ip or pair_port is None:
        print("Timed out waiting for the pairing service.")
        return False

    print(f"Device found at {pair_ip}:{pair_port}. Initiating pairing...")
    if not pair_device(adb_path, pair_ip, pair_port, password):
        print("Pairing failed.")
        return False

    print("Pairing successful! Waiting for connection service...")
    connect_ip, connect_port = discover_service(CONNECT_SERVICE, service_name, timeout)
    if not connect_ip or connect_port is None:
        print("Timed out waiting for the connection service.")
        return False

    if not connect_device(adb_path, connect_ip, connect_port):
        print("Connection failed.")
        return False

    print("Successfully paired and connected!")
    return True
