# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('adb.exe', '.'), ('AdbWinApi.dll', '.'), ('AdbWinUsbApi.dll', '.'), ('scrcpy.exe', '.'), ('SDL3.dll', '.'), ('avcodec-62.dll', '.'), ('avformat-62.dll', '.'), ('avutil-60.dll', '.'), ('swresample-6.dll', '.'), ('libusb-1.0.dll', '.')],
    datas=[('scrcpy-server', '.'), ('scrcpy.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    icon='icon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
