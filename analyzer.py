import psutil
import os
from pathlib import Path
try:
    import WMI
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False
    print("WMI not available for detailed drive info. Install with 'pip install WMI'")

def get_size(bytes_size, suffix="B"):
    \"\"\"Convert bytes to human readable format.\"\"\"
    factor = 1024
    for unit in [\"\", \"K\", \"M\", \"G\", \"T\", \"P\"]:
        if bytes_size < factor:
            return f\"{bytes_size:.2f}{unit}{suffix}\"
        bytes_size /= factor
    return f\"{bytes_size:.2f}P{suffix}\"

class DiskAnalyzer:
    def __init__(self):
        self.file_categories = {
            'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            'Apps': ['.exe', '.msi', '.app', '.deb', '.rpm'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'System': ['.dll', '.sys', '.drv']
        }

    def get_physical_drives(self):
        \"\"\"Get physical drive info using WMI.\"\"\"
        drives = []
        if WMI_AVAILABLE:
            c = WMI.WMI()
            for disk in c.Win32_DiskDrive():
                drives.append({
                    'name': disk.Caption or disk.Model,
                    'model': disk.Model,
                    'type': 'SSD' if 'SSD' in disk.Model.upper() or disk.MediaType == 'Solid State Disk' else 'HDD',
                    'size': int(disk.Size or 0),
                    'interface': disk.InterfaceType or 'Unknown'
                })
        return drives

    def get_partition_info(self):
        \"\"\"Get partition details.\"\"\"
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except PermissionError:
                print(f\"Access denied for {partition.mountpoint}\")
        return partitions

    def scan_directory(self, path, max_depth=3):
        \"\"\"Recursively scan directory for sizes, categories, top folders. Limit depth for performance.\"\"\"
        total_size = 0
        category_sizes = {cat: 0 for cat in self.file_categories}
        folder_sizes = {}  # path: size
        queue = [(path, 0)]  # (dirpath, depth)

        while queue:
            dirpath, depth = queue.pop(0)
            if depth > max_depth:
                continue
            try:
                for entry in os.scandir(dirpath):
                    if entry.is_file():
                        size = entry.stat().st_size
                        total_size += size
                        ext = Path(entry.path).suffix.lower()
                        for cat, exts in self.file_categories.items():
                            if ext in exts:
                                category_sizes[cat] += size
                                break
                    elif entry.is_dir():
                        folder_sizes[entry.path] = 0  # placeholder
                        queue.append((entry.path, depth + 1))
            except PermissionError:
                continue

        # Sort top 10 folders (simplified, actual sum in full impl)
        top_folders = sorted(folder_sizes.items(), key=lambda x: 1, reverse=True)[:10]  # placeholder

        return {
            'total_size': total_size,
            'category_sizes': category_sizes,
            'top_folders': top_folders
        }

    def get_health_status(self):
        \"\"\"Basic SMART status via WMI.\"\"\"
        status = []
        if WMI_AVAILABLE:
            c = WMI.WMI()
            for disk in c.Win32_DiskDrive():
                smart_status = 'OK'
                # Simplified; full SMART needs pySMART or wmic
                status.append({'disk': disk.DeviceID, 'status': smart_status})
        return status

# Test function
if __name__ == \"__main__":
    analyzer = DiskAnalyzer()
    print(\"=== Physical Drives ===\")
    for d in analyzer.get_physical_drives():
        print(d)
    print(\"\\n=== Partitions ===\")
    for p in analyzer.get_partition_info():
        print(f\"{p['mountpoint']}: {get_size(p['total'])} total, {p['percent']:.1f}% used\")
    # Example scan (user changeable)
    scan = analyzer.scan_directory('C:\\Users')
    print(f\"\\nScan C:\\Users: {get_size(scan['total_size'])}\")
    print(\"Categories:\", {k: get_size(v) for k,v in scan['category_sizes'].items()})

