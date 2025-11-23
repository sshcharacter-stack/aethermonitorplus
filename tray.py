"""
System tray icon for Aether Monitor+.
Uses pystray for cross-platform system tray support.
"""
import threading
import os
import sys
from typing import Optional, Callable
try:
    from PIL import Image, ImageDraw
    import pystray
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False


class SystemTray:
    """System tray icon handler."""
    
    def __init__(self, on_show: Optional[Callable] = None, on_quit: Optional[Callable] = None):
        self.on_show = on_show
        self.on_quit = on_quit
        self.icon: Optional[pystray.Icon] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
        
    def _create_image(self):
        """Create a simple icon image."""
        # Try to load ICO first (better for system tray), then PNG
        icon_paths = []
        
        # Check if running from EXE (temporary folder)
        if getattr(sys, 'frozen', False):
            try:
                base_path = sys._MEIPASS
                icon_paths.extend([
                    os.path.join(base_path, 'assets', 'main_icon.ico'),
                    os.path.join(base_path, 'assets', 'icon.png'),
                ])
            except:
                pass
        
        # Add regular paths (also check current directory)
        current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
        icon_paths.extend([
            os.path.join('assets', 'main_icon.ico'),
            os.path.join('assets', 'icon.png'),
            os.path.join(current_dir, 'assets', 'main_icon.ico'),
            os.path.join(current_dir, 'assets', 'icon.png'),
        ])
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    img = Image.open(icon_path)
                    # Convert to RGBA for better quality
                    if img.mode not in ('RGBA', 'RGB'):
                        if img.mode == 'P' and 'transparency' in img.info:
                            img = img.convert('RGBA')
                        else:
                            img = img.convert('RGB')
                    # Resize to 64x64 if needed
                    if img.size != (64, 64):
                        img = img.resize((64, 64), Image.Resampling.LANCZOS)
                    # Convert to RGB if RGBA (pystray works better with RGB)
                    if img.mode == 'RGBA':
                        # Create dark background
                        background = Image.new('RGB', img.size, (26, 26, 26))  # #1a1a1a
                        if img.split()[3] if len(img.split()) == 4 else None:
                            background.paste(img, mask=img.split()[3])
                        else:
                            background.paste(img)
                        img = background
                    return img
                except Exception as e:
                    continue
        
        # Fallback: Create a simple icon image with better visibility
        # Use 16x16 for system tray (smaller is better)
        size = 16
        image = Image.new('RGB', (size, size), color=(0, 255, 136))  # Green background
        draw = ImageDraw.Draw(image)
        
        # Draw a simple lightning bolt shape with better contrast
        # White lightning bolt
        draw.polygon([(6, 2), (10, 2), (8, 6), (14, 6), (6, 14), (8, 10), (2, 10)], fill=(255, 255, 255))
        
        # Resize to 64x64 for pystray
        if size != 64:
            image = image.resize((64, 64), Image.Resampling.NEAREST)
        
        return image
    
    def _create_menu(self):
        """Create context menu for tray icon."""
        menu_items = []
        
        if self.on_show:
            menu_items.append(pystray.MenuItem("Show Window", self._on_show))
        
        menu_items.append(pystray.MenuItem("Exit", self._on_quit))
        
        return pystray.Menu(*menu_items)
    
    def _on_show(self, icon, item):
        """Handle show window menu item."""
        if self.on_show:
            self.on_show()
    
    def _on_quit(self, icon, item):
        """Handle quit menu item."""
        if self.on_quit:
            self.on_quit()
        self.stop()
    
    def start(self):
        """Start system tray icon."""
        if not TRAY_AVAILABLE:
            return False
        
        try:
            image = self._create_image()
            if image is None:
                return False
                
            menu = self._create_menu()
            
            # Create icon with proper name and title
            self.icon = pystray.Icon(
                "AetherMonitorPlus",
                image,
                "Aether Monitor+",
                menu
            )
            self._running = True
            
            # Run in separate thread (daemon=True to allow app to exit)
            self._thread = threading.Thread(target=self._run_icon, daemon=True, name="TrayIconThread")
            self._thread.start()
            
            # Small delay to ensure thread starts
            import time
            time.sleep(0.2)
            
            return True
        except Exception as e:
            # Silently fail - tray is optional
            return False
    
    def _run_icon(self):
        """Run icon in thread."""
        if self.icon:
            self.icon.run()
    
    def stop(self):
        """Stop system tray icon."""
        self._running = False
        if self.icon:
            try:
                self.icon.stop()
            except:
                pass
        self.icon = None
    
    def is_available(self):
        """Check if system tray is available."""
        return TRAY_AVAILABLE

