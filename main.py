"""
Aether Monitor+ - Ultra-lightweight system monitor.
Entry point with optimized initialization.
"""
import tkinter as tk
import threading
import time
import gc
from core import MonitorCore
from ui import MonitorUI
from widget import OverlayWidget
from tray import SystemTray
from typing import Optional


class AetherMonitor:
    """Main application controller."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.core = MonitorCore()
        self.ui = MonitorUI(self.root, core=self.core)
        self.widget: Optional[OverlayWidget] = None
        self.tray: Optional[SystemTray] = None
        self.running = False
        self._update_thread = None
        self._window_visible = False
        self._quitting = False
        self._widget_visible = True
        
        # Set widget toggle callback
        self.ui.set_widget_toggle_callback(self._toggle_widget)
        
        # Hide main window initially
        self.root.withdraw()
        
        # Track window visibility
        self.root.bind('<Map>', lambda e: self._on_window_show())
        self.root.bind('<Unmap>', lambda e: self._on_window_hide())
        
        # Override close button to minimize to tray
        self.root.protocol('WM_DELETE_WINDOW', self._on_close_window)
        
    def _on_window_show(self):
        """Handle window show event."""
        self._window_visible = True
        # Force GC when window is shown
        gc.collect()
        
    def _on_window_hide(self):
        """Handle window hide event - aggressive GC."""
        self._window_visible = False
        # Aggressive garbage collection when window is hidden
        self.core.clear_caches()
        gc.collect()
    
    def _on_close_window(self):
        """Handle window close - minimize to tray instead of quitting."""
        if not self._quitting:
            # Hide window instead of closing
            self.root.withdraw()
        else:
            # Actually quit
            self._quit_application()
    
    def _show_main_window(self):
        """Show main window."""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.attributes('-topmost', True)
        self.root.after_idle(lambda: self.root.attributes('-topmost', False))
        self._window_visible = True
    
    def _quit_application(self):
        """Quit application completely."""
        self._quitting = True
        self.running = False
        
        # Stop tray
        if self.tray:
            self.tray.stop()
        
        # Destroy widget
        if self.widget:
            self.widget.destroy()
        
        # Destroy root window
        try:
            if self.root.winfo_exists():
                self.root.quit()
                self.root.destroy()
        except:
            pass
        
    def _update_loop(self):
        """Background update loop with optimized polling."""
        last_data = None  # Keep last data to prevent flickering
        while self.running:
            try:
                # Always update data, but only refresh UI if visible
                data = self.core.get_all(include_recommendations=self._window_visible)
                
                # Use last data if current is invalid (prevents flickering)
                if data and all(key in data for key in ['cpu', 'ram', 'disk', 'health']):
                    last_data = data
                
                # Schedule UI update on main thread (non-blocking)
                if self._window_visible and self.root.winfo_exists() and last_data:
                    self.root.after(0, self.ui.update_all, last_data)
                # Sleep for minimum interval (3s for CPU)
                time.sleep(3)
            except (tk.TclError, RuntimeError):
                break
            except Exception:
                # On error, still try to update with last known data
                if last_data and self._window_visible and self.root.winfo_exists():
                    try:
                        self.root.after(0, self.ui.update_all, last_data)
                    except:
                        pass
                time.sleep(3)
    
    def start(self):
        """Start monitoring."""
        self.running = True
        
        # Initialize system tray (optional - won't break if unavailable)
        try:
            self.tray = SystemTray(
                on_show=self._show_main_window,
                on_quit=self._quit_application
            )
            if self.tray.is_available():
                self.tray.start()
        except Exception:
            # Tray is optional, continue without it
            self.tray = None
        
        # Start update thread
        self._update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self._update_thread.start()
        
        # Initial update to populate data
        data = self.core.get_all(include_recommendations=False)
        if self.root.winfo_exists():
            self.root.after(0, self.ui.update_all, data)
        
        # Create overlay widget
        self.widget = OverlayWidget(
            self.core,
            on_click=self._show_main_window,
            on_disable=self._disable_widget
        )
        self.widget.create()
        self._widget_visible = True
        # Update button state
        self.ui.update_widget_button(True)
        
        # Start main loop
        try:
            self.root.mainloop()
        except:
            pass
        finally:
            self.running = False
            # Cleanup
            if self.widget:
                self.widget.destroy()
            if self.tray:
                self.tray.stop()
    
    def _disable_widget(self):
        """Handle widget disable request."""
        if self.widget:
            self.widget.hide()
            self._widget_visible = False
            # Update button in UI if window is visible
            if self._window_visible:
                self.root.after(0, lambda: self.ui.update_widget_button(False))
    
    def _toggle_widget(self):
        """Toggle widget visibility."""
        if not self.widget:
            # Create widget if it doesn't exist
            self.widget = OverlayWidget(
                self.core,
                on_click=self._show_main_window,
                on_disable=self._disable_widget
            )
            self.widget.create()
            self._widget_visible = True
        elif self._widget_visible:
            # Hide widget
            self.widget.hide()
            self._widget_visible = False
        else:
            # Show widget
            self.widget.show()
            self._widget_visible = True
        
        # Update button text
        self.ui.update_widget_button(self._widget_visible)


def main():
    """Application entry point."""
    app = AetherMonitor()
    app.start()


if __name__ == "__main__":
    main()

