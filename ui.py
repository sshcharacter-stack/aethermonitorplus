"""
Ultra-lightweight minimalist UI.
Only essential components: 4 progressbars, 1 text, 2 buttons, 1 label.
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict
import json
import os


class MonitorUI:
    """Minimalist UI - only essential widgets."""
    
    def __init__(self, root: tk.Tk, core=None, config_path: str = "config.json"):
        self.root = root
        self.core = core
        self.config = self._load_config(config_path)
        self._recommendations_cached = None
        self._setup_window()
        self._create_widgets()
        
    def _load_config(self, path: str) -> Dict:
        """Load configuration."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {
                "window": {"width": 320, "height": 520, "resizable": False},
                "poll_intervals": {"cpu": 3, "ram": 5, "disk": 10}
            }
    
    def _setup_window(self):
        """Configure main window - no resize."""
        self.root.title("AETHER MONITOR+")
        self.root.geometry(f"{self.config['window']['width']}x{self.config['window']['height']}")
        self.root.resizable(False, False)
        
        # Try to set icon - support both development and PyInstaller builds
        try:
            import sys
            icon_paths = []
            
            # Check if running from EXE (PyInstaller)
            if getattr(sys, 'frozen', False):
                try:
                    base_path = sys._MEIPASS
                    icon_paths.append(os.path.join(base_path, 'assets', 'main_icon.ico'))
                    icon_paths.append(os.path.join(base_path, 'main_icon.ico'))  # Also check root
                except:
                    pass
            
            # Regular paths
            current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
            icon_paths.extend([
                os.path.join('assets', 'main_icon.ico'),
                os.path.join(current_dir, 'assets', 'main_icon.ico'),
                os.path.abspath(os.path.join('assets', 'main_icon.ico')),
            ])
            
            icon_set = False
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    try:
                        # Use absolute path
                        abs_path = os.path.abspath(icon_path)
                        self.root.iconbitmap(abs_path)
                        icon_set = True
                        break
                    except Exception as e:
                        continue
            
            # If iconbitmap failed, try alternative method
            if not icon_set:
                try:
                    from PIL import Image, ImageTk
                    for icon_path in icon_paths:
                        if os.path.exists(icon_path):
                            try:
                                img = Image.open(icon_path)
                                photo = ImageTk.PhotoImage(img)
                                self.root.iconphoto(False, photo)
                                self.root._icon_photo = photo  # Keep reference
                                break
                            except:
                                continue
                except:
                    pass
        except Exception as e:
            pass
        
        self.font = ('Segoe UI', 9)
        self.root.configure(bg='#1a1a1a')
        
    def _create_widgets(self):
        """Create only essential widgets."""
        # Main container - minimal
        main = tk.Frame(self.root, bg='#1a1a1a', padx=10, pady=8)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Header with logo and title
        header = tk.Frame(main, bg='#1a1a1a')
        header.pack(fill=tk.X, pady=(0, 8))
        
        # Logo/Icon - try to load PNG, fallback to emoji
        import sys
        icon_paths = [os.path.join('assets', 'icon.png')]
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            icon_paths.insert(0, os.path.join(base_path, 'assets', 'icon.png'))
        
        icon_loaded = False
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    from tkinter import PhotoImage
                    logo_img = PhotoImage(file=icon_path)
                    # Resize if needed (max 24x24)
                    logo_label = tk.Label(
                        header,
                        image=logo_img,
                        bg='#1a1a1a'
                    )
                    logo_label.image = logo_img  # Keep a reference
                    logo_label.pack(side=tk.LEFT, padx=(0, 8))
                    icon_loaded = True
                    break
                except Exception:
                    continue
        
        if not icon_loaded:
            # Use emoji as fallback
            logo_label = tk.Label(
                header,
                text="⚡",
                font=('Segoe UI', 20),
                bg='#1a1a1a',
                fg='#00ff88'
            )
            logo_label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Title
        title = tk.Label(header, text="AETHER MONITOR+", font=self.font, bg='#1a1a1a', fg='#00ff88')
        title.pack(side=tk.LEFT)
        
        # CPU Progressbar with label
        cpu_frame = tk.Frame(main, bg='#1a1a1a')
        cpu_frame.pack(fill=tk.X, pady=2)
        cpu_label = tk.Label(cpu_frame, text="CPU:", font=self.font, bg='#1a1a1a', fg='#888888', width=8, anchor='w')
        cpu_label.pack(side=tk.LEFT)
        self.cpu_bar = ttk.Progressbar(cpu_frame, length=220, mode='determinate', maximum=100)
        self.cpu_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # RAM Progressbar with label
        ram_frame = tk.Frame(main, bg='#1a1a1a')
        ram_frame.pack(fill=tk.X, pady=2)
        ram_label = tk.Label(ram_frame, text="RAM:", font=self.font, bg='#1a1a1a', fg='#888888', width=8, anchor='w')
        ram_label.pack(side=tk.LEFT)
        self.ram_bar = ttk.Progressbar(ram_frame, length=220, mode='determinate', maximum=100)
        self.ram_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # DISK Progressbar with label
        disk_frame = tk.Frame(main, bg='#1a1a1a')
        disk_frame.pack(fill=tk.X, pady=2)
        disk_label = tk.Label(disk_frame, text="DISK:", font=self.font, bg='#1a1a1a', fg='#888888', width=8, anchor='w')
        disk_label.pack(side=tk.LEFT)
        self.disk_bar = ttk.Progressbar(disk_frame, length=220, mode='determinate', maximum=100)
        self.disk_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Health Progressbar with label
        health_frame = tk.Frame(main, bg='#1a1a1a')
        health_frame.pack(fill=tk.X, pady=2)
        health_label = tk.Label(health_frame, text="HEALTH:", font=self.font, bg='#1a1a1a', fg='#888888', width=8, anchor='w')
        health_label.pack(side=tk.LEFT)
        self.health_bar = ttk.Progressbar(health_frame, length=220, mode='determinate', maximum=100)
        self.health_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Health percentage label
        self.health_label = tk.Label(main, text="HEALTH: 0%", font=self.font, bg='#1a1a1a', fg='#00ff88', anchor='w')
        self.health_label.pack(fill=tk.X, pady=(2, 4))
        
        # Recommendations frame with better visibility
        rec_frame = tk.Frame(main, bg='#1a1a1a')
        rec_frame.pack(fill=tk.BOTH, expand=True, pady=(4, 2))
        
        rec_label = tk.Label(rec_frame, text="Recommendations:", font=('Segoe UI', 9, 'bold'), bg='#1a1a1a', fg='#00ff88', anchor='w')
        rec_label.pack(fill=tk.X, pady=(0, 4))
        
        # Text for recommendations with better styling - larger and more visible
        rec_font = ('Segoe UI', 10)  # Slightly larger font
        self.rec_text = tk.Text(rec_frame, height=4, width=35, font=rec_font, bg='#2a2a2a', fg='#ffffff',
                               relief=tk.FLAT, wrap=tk.WORD, padx=8, pady=6, bd=0, highlightthickness=0,
                               selectbackground='#00ff88', selectforeground='#1a1a1a', insertwidth=0)
        self.rec_text.pack(fill=tk.BOTH, expand=True)
        # Make it look more like a label but keep text selectable
        self.rec_text.config(state=tk.DISABLED, cursor='arrow')  # Read-only
        
        # Buttons for widget control - ensure it's visible
        btn_frame = tk.Frame(main, bg='#1a1a1a')
        btn_frame.pack(fill=tk.X, pady=(4, 4))
        
        self.widget_btn = tk.Button(btn_frame, text="ENABLE WIDGET", font=self.font, bg='#2a2a2a', fg='#ffffff',
                                    relief=tk.FLAT, padx=8, pady=2, command=self._on_widget)
        self.widget_btn.pack(side=tk.LEFT, padx=(0, 5))
    
    def _on_widget(self):
        """Widget button handler - toggle widget visibility."""
        if hasattr(self, 'on_widget_toggle'):
            self.on_widget_toggle()
    
    def set_widget_toggle_callback(self, callback):
        """Set callback for widget toggle button."""
        self.on_widget_toggle = callback
    
    def update_widget_button(self, widget_visible: bool):
        """Update widget button text based on visibility."""
        if widget_visible:
            self.widget_btn.config(text="DISABLE WIDGET")
        else:
            self.widget_btn.config(text="ENABLE WIDGET")
    
    def update_all(self, data: Dict):
        """Update all displays."""
        try:
            # Update progressbars with values
            cpu_val = data.get('cpu', 0.0)
            self.cpu_bar['value'] = cpu_val
            
            ram_data = data.get('ram', {})
            ram_val = ram_data.get('percent', 0.0) if isinstance(ram_data, dict) else ram_data
            self.ram_bar['value'] = ram_val
            
            disk_data = data.get('disk', {})
            disk_val = disk_data.get('percent', 0.0) if isinstance(disk_data, dict) else disk_data
            self.disk_bar['value'] = disk_val
            
            health_val = data.get('health', 0.0)
            self.health_bar['value'] = health_val
            
            # Update health label
            self.health_label.config(text=f"HEALTH: {health_val:.0f}%")
            
            # Color health
            if health_val >= 70:
                self.health_label.config(fg='#00ff88')
            elif health_val >= 40:
                self.health_label.config(fg='#ffaa00')
            else:
                self.health_label.config(fg='#ff4444')
            
            # Lazy evaluation of recommendations (only when window is visible)
            try:
                self.rec_text.config(state=tk.NORMAL)
                self.rec_text.delete('1.0', tk.END)
                
                # Compute recommendations only when needed (lazy)
                if self.core:
                    recs = self.core.get_recommendations()
                else:
                    recs = data.get('recommendations', [])
                
                # Clear and populate recommendations
                if recs and len(recs) > 0:
                    lines = []
                    for text, action in recs:
                        lines.append(f"{text}\n   → {action}")
                    content = '\n\n'.join(lines)
                else:
                    # Always show general tips if no specific recommendations
                    general_tips = [
                        '💡 System Optimization\n   → Regularly clean temporary files',
                        '💡 Performance\n   → Close unused programs',
                        '💡 Maintenance\n   → Check disk for errors monthly'
                    ]
                    content = '\n\n'.join(general_tips[:2])
                
                # Insert content
                if content:
                    self.rec_text.insert('1.0', content)
                
                self.rec_text.config(state=tk.DISABLED)
                
                # Force update to ensure visibility
                self.rec_text.update_idletasks()
            except Exception as e:
                # Fallback: show at least something
                try:
                    self.rec_text.config(state=tk.NORMAL)
                    self.rec_text.delete('1.0', tk.END)
                    self.rec_text.insert('1.0', '💡 System is running normally\n   → Regularly check system status')
                    self.rec_text.config(state=tk.DISABLED)
                except:
                    pass
        except Exception as e:
            # Error handling - ensure UI doesn't break
            pass
