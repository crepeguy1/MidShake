# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['python/midshake_cli.py'],
    pathex=[],
    binaries=[],
    datas=[('stdlib', 'stdlib'), ('python', 'python')],
    hiddenimports=['midshake_tokenizer', 'midshake_parser', 'midshake_runtime', 'midshake_interpreter', 'midshake_compiler', 'midshake_semantic', 'midshake_ast', 'midshake_highlight'],
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
    name='midshake',
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
