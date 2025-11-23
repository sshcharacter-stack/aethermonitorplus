"""
Setup autostart for Aether Monitor+ on Windows.
Creates a startup shortcut in Windows Startup folder.
"""
import os
import sys
import win32api
import win32con
from pathlib import Path


def setup_autostart():
    """Add application to Windows startup."""
    try:
        # Get current script directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            app_path = sys.executable
        else:
            # Running as script
            app_path = os.path.abspath(__file__)
            # If this is setup script, use main.py instead
            if 'setup_autostart' in app_path:
                app_path = os.path.join(os.path.dirname(app_path), 'main.py')
                app_path = f'"{sys.executable}" "{app_path}"'
        
        # Get Windows Startup folder
        startup_folder = os.path.join(
            os.environ.get('APPDATA', ''),
            'Microsoft',
            'Windows',
            'Start Menu',
            'Programs',
            'Startup'
        )
        
        # Create shortcut
        shortcut_path = os.path.join(startup_folder, 'AetherMonitorPlus.lnk')
        
        # Create shortcut using Windows API
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = app_path if not isinstance(app_path, str) or not app_path.startswith('"') else app_path.split('"')[1]
        if isinstance(app_path, str) and app_path.startswith('"'):
            shortcut.Arguments = app_path.split('"')[2].strip()
        shortcut.WorkingDirectory = os.path.dirname(app_path) if not isinstance(app_path, str) or not app_path.startswith('"') else os.path.dirname(app_path.split('"')[1])
        shortcut.IconLocation = os.path.join(os.path.dirname(app_path) if not isinstance(app_path, str) or not app_path.startswith('"') else os.path.dirname(app_path.split('"')[1]), 'assets', 'main_icon.ico')
        shortcut.save()
        
        print(f"✓ Autostart configured successfully!")
        print(f"  Shortcut created: {shortcut_path}")
        return True
        
    except ImportError:
        print("Error: pywin32 is required for autostart setup.")
        print("Install it with: pip install pywin32")
        return False
    except Exception as e:
        print(f"Error setting up autostart: {e}")
        return False


def remove_autostart():
    """Remove application from Windows startup."""
    try:
        startup_folder = os.path.join(
            os.environ.get('APPDATA', ''),
            'Microsoft',
            'Windows',
            'Start Menu',
            'Programs',
            'Startup'
        )
        shortcut_path = os.path.join(startup_folder, 'AetherMonitorPlus.lnk')
        
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
            print("✓ Autostart removed successfully!")
            return True
        else:
            print("Autostart was not configured.")
            return False
    except Exception as e:
        print(f"Error removing autostart: {e}")
        return False


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'remove':
        remove_autostart()
    else:
        setup_autostart()


