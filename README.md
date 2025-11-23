# ⚡ Aether Monitor+

<div align="center">

**Ultra-lightweight system monitoring application for Windows**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Memory](https://img.shields.io/badge/Memory-<30MB-orange.svg)]()

*Minimal resource consumption • Real-time monitoring • Smart recommendations*

</div>

---

## ✨ Features

### 🎯 Core Functionality
- **Real-time System Monitoring** - Track CPU, RAM, Disk usage, and Temperature
- **System Health Score** - Intelligent calculation based on resource utilization
- **Smart Recommendations** - Context-aware optimization tips for system performance
- **Overlay Widget** - Always-on-top draggable widget for quick metric glances
- **System Tray Integration** - Minimize to tray with right-click context menu
- **Windows Autostart** - Optional automatic launch on system boot

### 🚀 Performance
- **Ultra-Lightweight** - Strict memory limit: <30MB under load
- **Optimized Polling** - Dynamic intervals (CPU: 3s, RAM: 5s, Disk: 10s)
- **Lazy Loading** - Components load only when needed
- **Aggressive GC** - Automatic memory optimization hooks

### 💡 User Experience
- **Minimalist UI** - Clean, focused interface with essential metrics
- **Draggable Widget** - Customizable overlay position
- **Color-Coded Metrics** - Visual indicators for system status
- **One-Click Access** - Quick widget toggle from main window

---

## 📋 Requirements

- **Python**: 3.8 or higher
- **OS**: Windows 10/11 (primary support)
- **Dependencies**: 
  - `psutil==5.9.5` - System monitoring
  - `pystray>=0.19.4` - System tray integration
  - `Pillow>=9.0.0` - Image processing

---

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sshcharacter-stack/aetherMonitorplus.git
   cd aetherMonitor+
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### Building Executable

Build a standalone Windows executable:

```bash
python build.py
```

The executable will be created in `dist/AetherMonitorPlus.exe`.

**Note**: For icon support, place your application icons in the `assets/` folder:
- `main_icon.ico` - 256x256 ICO file (multiple sizes recommended)
- `icon.png` - PNG file for widget and UI logo

---

## 📁 Project Structure

```
aetherMonitor+
├── main.py              # Application entry point & orchestration
├── core.py              # Core monitoring logic & recommendations
├── ui.py                # Main application UI components
├── widget.py            # Overlay widget implementation
├── tray.py              # System tray integration
├── autostart.py         # Windows autostart management
├── build.py             # PyInstaller build script
├── config.json          # Application configuration
├── requirements.txt      # Python dependencies
├── LICENSE              # MIT License
└── README.md           # This file
```

---

## ⚙️ Configuration

Edit `config.json` to customize application behavior:

```json
{
  "poll_intervals": {
    "cpu": 3,
    "ram": 5,
    "disk": 10
  },
  "window": {
    "width": 320,
    "height": 520,
    "resizable": false
  },
  "cache_ttl": 1
}
```

---

## 🎯 Memory Optimization

The application is designed with strict memory constraints in mind:

### Optimization Strategies
- **Lazy Loading** - Components created only when needed
- **Aggressive Garbage Collection** - Automatic cleanup on window hide
- **Dynamic Polling Intervals** - Adjusts based on memory usage
- **Minimal Caching** - Only essential data cached

### Target Memory Usage
- **Startup**: 15-18MB
- **With Widget**: 20-25MB
- **Under Load**: <30MB

### Memory Monitoring
Built-in memory monitoring automatically optimizes resource usage:
- Increases polling intervals when memory exceeds 25MB
- Clears caches on window hide
- Forces garbage collection periodically

---

## 🎨 Usage

### Main Window
- Displays real-time metrics (CPU, RAM, Disk, Temperature)
- Shows system health score
- Provides smart recommendations
- Widget toggle button

### Overlay Widget
- **Left-click**: Open main window
- **Right-click**: Context menu (disable widget)
- **Drag**: Reposition anywhere on screen
- Auto-updates every 5 seconds

### System Tray
- **Left-click**: Show main window
- **Right-click**: Context menu (Show/Quit)

---

## 🔧 Autostart (Windows)

Enable or disable autostart:

```powershell
# Enable autostart
python autostart.py --enable

# Disable autostart
python autostart.py --disable
```

---

## 📊 System Health Formula

The system health score is calculated as:

```
Health = 100 - ((CPU_usage × 0.3) + (RAM_usage × 0.4) + (DISK_usage × 0.3))
```

This provides a balanced assessment of overall system performance.

---

## 🛠️ Development

### Building from Source

1. Ensure all dependencies are installed
2. Place icons in `assets/` folder (optional)
3. Run `python build.py`
4. Executable will be in `dist/` folder

### Running Tests

```bash
python main.py
```

Monitor memory usage with Task Manager to verify optimization targets.

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Shio Software

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Share feedback and suggestions

---

## 👨‍💻 Author

Developed with focus on **minimal resource consumption** and **user experience**.

---

<div align="center">

**Made with ⚡ for efficient system monitoring**

</div>
