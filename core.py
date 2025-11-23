"""
Ultra-lightweight core monitoring engine.
Optimized for minimal memory footprint - only primitive types cached.
"""
import psutil
import time
import os
import gc
from typing import Dict, Optional
from threading import Lock


class MonitorCore:
    """Ultra-lightweight monitoring core - only percentages cached."""
    
    def __init__(self):
        # Cache only primitive types (float) - minimal memory
        self._cpu_percent: float = 0.0
        self._ram_percent: float = 0.0
        self._disk_percent: float = 0.0
        self._temp_celsius: float = 0.0
        self._health: float = 100.0
        
        # Cache timestamps (float)
        self._last_cpu_time: float = 0.0
        self._last_ram_time: float = 0.0
        self._last_disk_time: float = 0.0
        self._last_temp_time: float = 0.0
        
        # Cache totals (rarely change) - for UI display only
        self._ram_total_gb: float = 0.0
        self._disk_total_gb: float = 0.0
        
        # Update intervals (can be adjusted for memory optimization)
        self._cpu_interval: float = 3.0
        self._ram_interval: float = 5.0
        self._disk_interval: float = 10.0
        
        self._lock = Lock()
        self._disk_path = 'C:\\' if os.name == 'nt' else '/'
        self._temp_available = False
        self._process = psutil.Process(os.getpid())
        
        # Initialize totals once
        self._init_totals()
        self._check_temp_availability()
    
    def _init_totals(self):
        """Initialize total values (rarely change)."""
        try:
            mem = psutil.virtual_memory()
            self._ram_total_gb = mem.total / (1024**3)
        except:
            self._ram_total_gb = 0.0
        
        try:
            disk = psutil.disk_usage(self._disk_path)
            self._disk_total_gb = disk.total / (1024**3)
        except:
            try:
                disk = psutil.disk_usage(os.path.expanduser('~'))
                self._disk_total_gb = disk.total / (1024**3)
            except:
                self._disk_total_gb = 0.0
    
    def _check_temp_availability(self):
        """Check if temperature sensors are available (no WMI)."""
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                self._temp_available = bool(temps)
            else:
                self._temp_available = False
        except:
            self._temp_available = False
    
    def get_app_memory_usage(self) -> float:
        """Get current application memory usage in MB."""
        try:
            return self._process.memory_info().rss / 1024 / 1024  # MB
        except:
            return 0.0
    
    def check_memory_limit(self) -> bool:
        """Check if memory usage exceeds limit and optimize if needed."""
        memory_mb = self.get_app_memory_usage()
        if memory_mb > 25:  # MB
            self.optimize_memory_usage()
            return True
        return False
    
    def optimize_memory_usage(self):
        """Optimize memory usage by adjusting intervals and clearing caches."""
        # Increase update intervals to reduce polling frequency
        self._cpu_interval = 10.0  # 10 seconds
        self._ram_interval = 15.0  # 15 seconds
        self._disk_interval = 20.0  # 20 seconds
        
        # Don't clear cached values - keep them visible
        # Only force garbage collection
        gc.collect()
    
    def clear_caches(self):
        """Clear all cached data (but preserve last known values)."""
        # Don't reset to 0 - keep last known values visible
        # Only force garbage collection
        gc.collect()
    
    def _calculate_health(self, cpu: float, ram: float, disk: float) -> float:
        """Calculate system health: 100 - weighted average."""
        health = 100.0 - ((cpu * 0.3) + (ram * 0.4) + (disk * 0.3))
        return max(0.0, min(100.0, health))  # Clamp 0-100
    
    def get_lightweight_metrics(self) -> Dict:
        """Get all metrics - optimized lightweight version."""
        current_time = time.time()
        
        # Check memory limit periodically
        if int(current_time) % 30 == 0:  # Check every 30 seconds
            self.check_memory_limit()
        
        # CPU (update based on interval)
        if current_time - self._last_cpu_time >= self._cpu_interval:
            with self._lock:
                if current_time - self._last_cpu_time >= self._cpu_interval:
                    self._cpu_percent = psutil.cpu_percent(interval=1)
                    self._last_cpu_time = current_time
        
        # RAM (update based on interval)
        if current_time - self._last_ram_time >= self._ram_interval:
            with self._lock:
                if current_time - self._last_ram_time >= self._ram_interval:
                    mem = psutil.virtual_memory()
                    self._ram_percent = mem.percent
                    self._last_ram_time = current_time
        
        # Disk (update based on interval)
        if current_time - self._last_disk_time >= self._disk_interval:
            with self._lock:
                if current_time - self._last_disk_time >= 10:
                    try:
                        disk = psutil.disk_usage(self._disk_path)
                        self._disk_percent = (disk.used / disk.total) * 100
                    except:
                        try:
                            disk = psutil.disk_usage(os.path.expanduser('~'))
                            self._disk_percent = (disk.used / disk.total) * 100
                        except:
                            self._disk_percent = 0.0
                    self._last_disk_time = current_time
        
        # Temperature (update every 10s, if available)
        if self._temp_available and (current_time - self._last_temp_time >= 10):
            with self._lock:
                if current_time - self._last_temp_time >= 10:
                    try:
                        temps = psutil.sensors_temperatures()
                        if temps:
                            # Get first available temperature
                            for name, entries in temps.items():
                                if entries:
                                    self._temp_celsius = entries[0].current
                                    break
                    except:
                        pass
                    self._last_temp_time = current_time
        
        # Calculate health
        self._health = self._calculate_health(
            self._cpu_percent,
            self._ram_percent,
            self._disk_percent
        )
        
        return {
            'cpu': self._cpu_percent,
            'ram': self._ram_percent,
            'disk': self._disk_percent,
            'temp': self._temp_celsius if self._temp_available else None,
            'health': self._health
        }
    
    def get_recommendations(self) -> list:
        """Get recommendations based on lightweight rules (lazy evaluation)."""
        # Check memory before computing recommendations
        if self.get_app_memory_usage() > 30:
            return []  # Skip recommendations if memory is high
        
        recs = []
        
        # Minimal recommendation rules (lambda functions)
        RECOMMENDATIONS = {
            'disk_critical': {
                'condition': lambda: self._disk_percent > 95,
                'text': '🔴 Low disk space',
                'action': 'Clean temporary files',
                'priority': 1
            },
            'disk_high': {
                'condition': lambda: self._disk_percent > 85,
                'text': '🟡 Low free space',
                'action': 'Free up disk space',
                'priority': 2
            },
            'ram_high': {
                'condition': lambda: self._ram_percent > 85,
                'text': '🟡 High memory usage',
                'action': 'Close unnecessary applications',
                'priority': 2
            },
            'cpu_high': {
                'condition': lambda: self._cpu_percent > 90,
                'text': '🟢 High CPU load',
                'action': 'Check background processes',
                'priority': 2
            },
            'ram_medium': {
                'condition': lambda: self._ram_percent > 75,
                'text': '🟡 High RAM usage',
                'action': 'Close background applications',
                'priority': 3
            }
        }
        
        # Evaluate conditions on-demand
        for key, rule in RECOMMENDATIONS.items():
            try:
                if rule['condition']():
                    recs.append((rule['text'], rule['action'], rule['priority']))
            except:
                pass
        
        # Sort by priority and return max 3
        recs.sort(key=lambda x: x[2])
        result = [(text, action) for text, action, _ in recs[:3]]
        
        # If no critical recommendations, add general optimization tips
        if not result:
            general_tips = [
                ('💡 System Optimization', 'Regularly clean temporary files'),
                ('💡 Performance', 'Close unused programs'),
                ('💡 Maintenance', 'Check disk for errors monthly')
            ]
            result = general_tips[:2]  # Show 2 general tips
        
        return result
    
    def get_detailed_for_ui(self, include_recommendations=False) -> Dict:
        """Get detailed metrics for UI (computes GB on-the-fly, not cached)."""
        metrics = self.get_lightweight_metrics()
        
        # Compute GB values on-the-fly (not cached to save memory)
        ram_used_gb = (self._ram_percent / 100.0) * self._ram_total_gb
        disk_used_gb = (self._disk_percent / 100.0) * self._disk_total_gb
        
        result = {
            'cpu': metrics['cpu'],
            'ram': {
                'used': ram_used_gb,
                'total': self._ram_total_gb,
                'percent': metrics['ram']
            },
            'disk': {
                'used': disk_used_gb,
                'total': self._disk_total_gb,
                'percent': metrics['disk']
            },
            'temp': metrics.get('temp'),
            'health': metrics['health']
        }
        
        # Recommendations computed lazily only when needed
        if include_recommendations:
            result['recommendations'] = self.get_recommendations()
        
        return result
    
    def get_all(self, include_recommendations=False) -> Dict:
        """Get all metrics (alias for compatibility)."""
        return self.get_detailed_for_ui(include_recommendations)

