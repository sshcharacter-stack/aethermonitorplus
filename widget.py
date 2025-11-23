"""
Ultra-lightweight overlay widget.
Minimal footprint: +2-3MB, single thread, 5s updates.
"""
import tkinter as tk
from tkinter import PhotoImage
import os
import sys
from typing import Optional, Callable


class OverlayWidget:
    """Minimalist overlay widget - 80x60px, draggable."""
    
    def __init__(self, core, on_click: Optional[Callable] = None, on_disable: Optional[Callable] = None):
        self.core = core
        self.on_click = on_click
        self.on_disable = on_disable
        self.window: Optional[tk.Toplevel] = None
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._update_timer = None
        self._context_menu: Optional[tk.Menu] = None
        
    def create(self):
        """Create overlay widget window."""
        self.window = tk.Toplevel()
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.attributes('-topmost', True)  # Always on top
        self.window.geometry('280x35+100+100')  # Fixed size for better readability
        self.window.configure(bg='#1a1a1a')
        
        # Disable window resizing
        self.window.resizable(False, False)
        
        # Create minimal content
        self._create_content()
        
        # Setup drag
        self._setup_drag()
        
        # Start updates
        self._schedule_update()
        
    def _create_content(self):
        """Create minimal widget content - single line with icon."""
        # Main frame with border
        frame = tk.Frame(self.window, bg='#2a2a2a', padx=6, pady=4)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Inner frame for content
        content = tk.Frame(frame, bg='#1a1a1a')
        content.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Font
        font = ('Segoe UI', 9, 'bold')
        
        # Icon - try to load PNG, fallback to emoji
        # Check if running from EXE (temporary folder)
        icon_paths = [os.path.join('assets', 'icon.png')]
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            icon_paths.insert(0, os.path.join(base_path, 'assets', 'icon.png'))
        
        icon_loaded = False
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    icon_img = PhotoImage(file=icon_path)
                    # Resize if needed (max 20x20)
                    self.icon_label = tk.Label(
                        content,
                        image=icon_img,
                        bg='#1a1a1a'
                    )
                    self.icon_label.image = icon_img  # Keep a reference
                    self.icon_label.pack(side=tk.LEFT, padx=(0, 6))
                    icon_loaded = True
                    break
                except Exception:
                    continue
        
        if not icon_loaded:
            # Use emoji as fallback
            self.icon_label = tk.Label(
                content,
                text="⚡",
                font=('Segoe UI', 14),
                bg='#1a1a1a',
                fg='#00ff88',
                width=2
            )
            self.icon_label.pack(side=tk.LEFT, padx=(0, 6))
        
        # Metrics container
        metrics_frame = tk.Frame(content, bg='#1a1a1a')
        metrics_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # CPU
        cpu_frame = tk.Frame(metrics_frame, bg='#1a1a1a')
        cpu_frame.pack(side=tk.LEFT, padx=2)
        cpu_label = tk.Label(cpu_frame, text="CPU:", font=('Segoe UI', 7), bg='#1a1a1a', fg='#888888')
        cpu_label.pack(side=tk.LEFT)
        self.cpu_value = tk.Label(cpu_frame, text="--%", font=font, bg='#1a1a1a', fg='#ffffff', width=4)
        self.cpu_value.pack(side=tk.LEFT, padx=(2, 0))
        
        # RAM
        ram_frame = tk.Frame(metrics_frame, bg='#1a1a1a')
        ram_frame.pack(side=tk.LEFT, padx=2)
        ram_label = tk.Label(ram_frame, text="RAM:", font=('Segoe UI', 7), bg='#1a1a1a', fg='#888888')
        ram_label.pack(side=tk.LEFT)
        self.ram_value = tk.Label(ram_frame, text="--%", font=font, bg='#1a1a1a', fg='#ffffff', width=4)
        self.ram_value.pack(side=tk.LEFT, padx=(2, 0))
        
        # DISK
        disk_frame = tk.Frame(metrics_frame, bg='#1a1a1a')
        disk_frame.pack(side=tk.LEFT, padx=2)
        disk_label = tk.Label(disk_frame, text="DISK:", font=('Segoe UI', 7), bg='#1a1a1a', fg='#888888')
        disk_label.pack(side=tk.LEFT)
        self.disk_value = tk.Label(disk_frame, text="--%", font=font, bg='#1a1a1a', fg='#ffffff', width=4)
        self.disk_value.pack(side=tk.LEFT, padx=(2, 0))
        
        # TEMP
        temp_frame = tk.Frame(metrics_frame, bg='#1a1a1a')
        temp_frame.pack(side=tk.LEFT, padx=2)
        self.temp_value = tk.Label(temp_frame, text="--°", font=font, bg='#1a1a1a', fg='#00ff88', width=4)
        self.temp_value.pack(side=tk.LEFT)
        
    def _show_context_menu(self, event):
        """Show context menu on right click."""
        if not self._context_menu:
            self._context_menu = tk.Menu(self.window, tearoff=0, bg='#2a2a2a', fg='#ffffff',
                                         activebackground='#3a3a3a', activeforeground='#ffffff')
            self._context_menu.add_command(label="Disable Widget", command=self._on_disable)
        
        try:
            self._context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self._context_menu.grab_release()
    
    def _on_disable(self):
        """Handle disable widget action."""
        if self.on_disable:
            self.on_disable()
        else:
            self.hide()
    
    def hide(self):
        """Hide widget without destroying."""
        if self.window:
            try:
                self.window.withdraw()
            except:
                pass
    
    def show(self):
        """Show hidden widget."""
        if self.window:
            try:
                self.window.deiconify()
            except:
                pass
    
    def _setup_drag(self):
        """Setup drag functionality."""
        if not self.window:
            return
            
        def on_drag_start(event):
            self._drag_start_x = event.x
            self._drag_start_y = event.y
        
        def on_drag_motion(event):
            if self.window:
                x = self.window.winfo_x() + event.x - self._drag_start_x
                y = self.window.winfo_y() + event.y - self._drag_start_y
                self.window.geometry(f'+{x}+{y}')
        
        def on_click_handler(event):
            if self.on_click:
                self.on_click()
        
        def on_right_click(event):
            self._show_context_menu(event)
        
        # Bind events to window
        self.window.bind('<Button-1>', on_drag_start)
        self.window.bind('<B1-Motion>', on_drag_motion)
        self.window.bind('<ButtonRelease-1>', on_click_handler)
        self.window.bind('<Button-3>', on_right_click)  # Right mouse button
        
        # Bind to all child widgets
        for widget in self.window.winfo_children():
            widget.bind('<Button-1>', on_drag_start)
            widget.bind('<B1-Motion>', on_drag_motion)
            widget.bind('<ButtonRelease-1>', on_click_handler)
            widget.bind('<Button-3>', on_right_click)  # Right mouse button
            # Recursive bind for nested widgets
            for child in widget.winfo_children():
                child.bind('<Button-1>', on_drag_start)
                child.bind('<B1-Motion>', on_drag_motion)
                child.bind('<ButtonRelease-1>', on_click_handler)
                child.bind('<Button-3>', on_right_click)  # Right mouse button
    
    def _schedule_update(self):
        """Schedule next update (5000ms interval)."""
        if self.window and self.window.winfo_exists():
            self._update()
            self._update_timer = self.window.after(5000, self._schedule_update)
    
    def _update(self):
        """Update widget metrics."""
        if not self.window or not self.window.winfo_exists():
            return
            
        try:
            metrics = self.core.get_lightweight_metrics()
            
            # Update individual labels with color coding
            cpu_val = metrics['cpu']
            self.cpu_value.config(text=f"{cpu_val:.0f}%", fg='#ff6b6b' if cpu_val > 80 else '#ffffff')
            
            ram_val = metrics['ram']
            self.ram_value.config(text=f"{ram_val:.0f}%", fg='#ffaa00' if ram_val > 80 else '#ffffff')
            
            disk_val = metrics['disk']
            self.disk_value.config(text=f"{disk_val:.0f}%", fg='#ff4444' if disk_val > 85 else '#ffffff')
            
            temp = metrics.get('temp')
            if temp is not None:
                self.temp_value.config(text=f"{temp:.0f}°", fg='#ff6b6b' if temp > 70 else '#00ff88')
            else:
                self.temp_value.config(text="--°", fg='#888888')
        except Exception as e:
            # Fallback display
            self.cpu_value.config(text="--%")
            self.ram_value.config(text="--%")
            self.disk_value.config(text="--%")
            self.temp_value.config(text="--°")
    
    def destroy(self):
        """Destroy widget."""
        try:
            if self._update_timer and self.window:
                try:
                    self.window.after_cancel(self._update_timer)
                except:
                    pass
            if self.window:
                try:
                    if self.window.winfo_exists():
                        self.window.destroy()
                except:
                    pass
        except:
            pass
        finally:
            self.window = None

