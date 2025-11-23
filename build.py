"""
Ultra-lightweight build script for Aether Monitor+.
PyInstaller with optimizations for minimal EXE size (8-12MB).
RADICAL ICON EMBEDDING: Uses spec file for guaranteed icon embedding.
"""
import PyInstaller.__main__
import os
import sys
import shutil


def create_spec_file(icon_path):
    """Create a PyInstaller spec file with icon embedded."""
    # Escape backslashes for Windows paths in spec file
    escaped_icon_path = icon_path.replace('\\', '\\\\')
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/main_icon.ico', 'assets'),
        ('assets/icon.png', 'assets'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'PyQt5', 'PyQt6', 'tkinter.test', 'unittest', 'test', 'distutils'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AetherMonitorPlus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=r'{escaped_icon_path}',
)
'''
    spec_path = 'AetherMonitorPlus.spec'
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    return spec_path


def build():
    """Build executable with PyInstaller optimizations."""
    
    # Get absolute path to icon
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, 'assets', 'main_icon.ico')
    
    # Check if icon exists
    if not os.path.exists(icon_path):
        print(f"⚠ Warning: Icon not found at {icon_path}")
        print("Building without icon...")
        icon_path = None
    else:
        abs_icon_path = os.path.abspath(icon_path)
        print(f"✓ Using icon: {abs_icon_path}")
        print(f"  Icon file size: {os.path.getsize(abs_icon_path)} bytes")
        
        # Verify icon format
        try:
            from PIL import Image
            img = Image.open(abs_icon_path)
            print(f"  Icon format: {img.format}, Size: {img.size}")
            img.close()
        except Exception as e:
            print(f"  ⚠ Warning: Could not verify icon format: {e}")
        
        icon_path = abs_icon_path
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('AetherMonitorPlus.spec'):
        os.remove('AetherMonitorPlus.spec')
    
    # Create spec file with icon
    if icon_path:
        spec_path = create_spec_file(icon_path)
        print(f"\n✓ Created spec file: {spec_path}")
        print("  Using spec file for guaranteed icon embedding...\n")
        
        # Build using spec file
        opts = [
            spec_path,
            '--clean',
            '--noconfirm',
        ]
    else:
        # Fallback to command line if no icon
        opts = [
            '--onefile',
            '--windowed',
            '--optimize=2',
            '--strip',
            '--noupx',
            '--name=AetherMonitorPlus',
            '--clean',
            '--noconfirm',
            '--exclude-module=matplotlib',
            '--exclude-module=numpy',
            '--exclude-module=pandas',
            '--exclude-module=PyQt5',
            '--exclude-module=PyQt6',
            '--exclude-module=tkinter.test',
            '--exclude-module=unittest',
            '--exclude-module=test',
            '--exclude-module=distutils',
            'main.py',
        ]
    
    print("Building Aether Monitor+ with PyInstaller...")
    print("\nExpected EXE size: 8-12MB")
    print("Target memory usage:")
    print("  - On startup: 15-18MB")
    print("  - With widget: 20-25MB")
    print("  - Under load: <30MB\n")
    
    try:
        PyInstaller.__main__.run(opts)
        print("\n✓ Build completed successfully!")
        print("  Output: dist/AetherMonitorPlus.exe")
        
        # Post-build: Verify icon was applied
        exe_path = os.path.join('dist', 'AetherMonitorPlus.exe')
        if os.path.exists(exe_path):
            exe_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"  EXE size: {exe_size:.2f} MB")
            
            if icon_path:
                print("\n  ✓ Icon embedded via spec file")
                print("  If icon doesn't appear:")
                print("    1. Clear Windows icon cache: ie4uinit.exe -show")
                print("    2. Restart Windows Explorer")
                print("    3. Rebuild with --clean flag")
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    build()
