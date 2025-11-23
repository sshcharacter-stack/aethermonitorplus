"""
Simple autostart setup for Aether Monitor+ on Windows.
Uses registry instead of shortcuts (no pywin32 required).
"""
import os
import sys
import winreg


def setup_autostart():
    """Add application to Windows startup via registry."""
    try:
        # Get current script directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            app_path = sys.executable
        else:
            # Running as script
            app_path = os.path.abspath(__file__)
            if 'setup_autostart' in app_path:
                app_path = os.path.join(os.path.dirname(app_path), 'main.py')
                app_path = f'"{sys.executable}" "{app_path}"'
        
        # Registry key for current user startup
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        # Set registry value
        if isinstance(app_path, str) and app_path.startswith('"'):
            # Already quoted
            winreg.SetValueEx(key, "AetherMonitorPlus", 0, winreg.REG_SZ, app_path)
        else:
            # Need to quote
            winreg.SetValueEx(key, "AetherMonitorPlus", 0, winreg.REG_SZ, f'"{app_path}"')
        
        winreg.CloseKey(key)
        
        print("✓ Autostart configured successfully!")
        print(f"  Application: {app_path}")
        return True
        
    except Exception as e:
        print(f"Error setting up autostart: {e}")
        return False


def remove_autostart():
    """Remove application from Windows startup."""
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        try:
            winreg.DeleteValue(key, "AetherMonitorPlus")
            print("✓ Autostart removed successfully!")
            return True
        except FileNotFoundError:
            print("Autostart was not configured.")
            return False
        finally:
            winreg.CloseKey(key)
            
    except Exception as e:
        print(f"Error removing autostart: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'remove':
        remove_autostart()
    else:
        setup_autostart()


