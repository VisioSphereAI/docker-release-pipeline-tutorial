import psutil
import platform
from datetime import datetime


class SystemMonitor:
    """Monitor system performance and hardware details."""

    @staticmethod
    def get_system_info():
        """Get detailed system information."""
        try:
            uname = platform.uname()
            return {
                "system": uname.system,
                "node_name": uname.node,
                "release": uname.release,
                "version": uname.version,
                "machine": uname.machine,
                "processor": uname.processor,
                "python_version": platform.python_version(),
                "platform": platform.platform(),
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_cpu_info():
        """Get CPU information and usage."""
        try:
            cpu_count_physical = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_percent_per_cpu = psutil.cpu_percent(interval=1, percpu=True)

            return {
                "physical_cores": cpu_count_physical,
                "logical_cores": cpu_count_logical,
                "max_frequency": cpu_freq.max if cpu_freq else 0,
                "min_frequency": cpu_freq.min if cpu_freq else 0,
                "current_frequency": cpu_freq.current if cpu_freq else 0,
                "total_usage": cpu_percent,
                "usage_per_core": cpu_percent_per_cpu,
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_memory_info():
        """Get RAM memory information."""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "free": memory.free,
                "percent": memory.percent,
                "swap_total": swap.total,
                "swap_used": swap.used,
                "swap_free": swap.free,
                "swap_percent": swap.percent,
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_disk_info():
        """Get disk usage information."""
        try:
            disks = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        "device": partition.device,
                        "mount_point": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent,
                    })
                except PermissionError:
                    continue

            return disks
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_network_info():
        """Get network interface information."""
        try:
            net_interfaces = {}
            stats = psutil.net_if_stats()
            addrs = psutil.net_if_addrs()

            for interface_name, interface_addrs in addrs.items():
                net_interfaces[interface_name] = {
                    "addresses": [],
                    "stats": None,
                }

                for addr in interface_addrs:
                    net_interfaces[interface_name]["addresses"].append({
                        "family": addr.family.name if hasattr(addr.family, "name") else str(addr.family),
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast,
                    })

                if interface_name in stats:
                    interface_stats = stats[interface_name]
                    net_interfaces[interface_name]["stats"] = {
                        "is_up": interface_stats.isup,
                        "speed": interface_stats.speed,
                        "mtu": interface_stats.mtu,
                    }

            return net_interfaces
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_network_io():
        """Get network I/O statistics."""
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout,
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_battery_info():
        """Get battery information."""
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return {"has_battery": False}

            return {
                "has_battery": True,
                "percent": battery.percent,
                "secsleft": battery.secsleft,
                "power_plugged": battery.power_plugged,
                "time_left": SystemMonitor._format_time(battery.secsleft),
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_processes():
        """Get top processes by CPU and memory usage."""
        try:
            processes = []
            for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
                try:
                    pinfo = proc.as_dict(attrs=["pid", "name", "cpu_percent", "memory_percent"])
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Sort by CPU usage and get top 10
            top_cpu = sorted(processes, key=lambda x: x.get("cpu_percent", 0), reverse=True)[:10]

            # Sort by memory and get top 10
            top_memory = sorted(processes, key=lambda x: x.get("memory_percent", 0), reverse=True)[:10]

            return {
                "top_cpu": top_cpu,
                "top_memory": top_memory,
                "total_processes": len(processes),
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_boot_time():
        """Get system boot time."""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            return {
                "boot_time": boot_time.isoformat(),
                "uptime_seconds": uptime.total_seconds(),
                "uptime_hours": uptime.total_seconds() / 3600,
                "uptime_formatted": SystemMonitor._format_uptime(uptime),
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_all_info():
        """Get all system information."""
        return {
            "timestamp": datetime.now().isoformat(),
            "system": SystemMonitor.get_system_info(),
            "cpu": SystemMonitor.get_cpu_info(),
            "memory": SystemMonitor.get_memory_info(),
            "disk": SystemMonitor.get_disk_info(),
            "network": SystemMonitor.get_network_info(),
            "network_io": SystemMonitor.get_network_io(),
            "battery": SystemMonitor.get_battery_info(),
            "boot_time": SystemMonitor.get_boot_time(),
            "processes": SystemMonitor.get_processes(),
        }

    @staticmethod
    def _format_time(seconds):
        """Format seconds to human-readable time."""
        if seconds is None or seconds == psutil.POWER_TIME_UNKNOWN:
            return "Unknown"

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    @staticmethod
    def _format_uptime(td):
        """Format timedelta to human-readable uptime."""
        total_seconds = int(td.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60

        return f"{days}d {hours}h {minutes}m"

    @staticmethod
    def format_bytes(bytes_val):
        """Convert bytes to human-readable format."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"
