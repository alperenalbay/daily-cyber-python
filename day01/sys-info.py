#!/usr/bin/env python3
import os
import platform
import subprocess
import json
import socket
from datetime import datetime

def get_system_info():
    """
    Sistem hakkinda temel bilgileri toplar.
    """
    info = {
        "timestamp": datetime.now().isoformat(),
        "os_type": os.name,
        "os_release": platform.release(),
        "os_version": platform.version(),
        "platform": platform.system(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "python_version": platform.python_version(),
    }
    
    # Kullanici bilgisi
    try:
        info["current_user"] = os.getlogin()
    except Exception:
        # Bazi ortamlarda (cron vb.) getlogin calismayabilir
        info["current_user"] = os.environ.get('USER', 'unknown')

    return info

def get_linux_distro():
    """
    Linux dagitim detaylarini alir.
    """
    try:
        # /etc/os-release dosyasindan bilgileri okumaya calisir
        with open("/etc/os-release") as f:
            lines = f.readlines()
            distro_info = {}
            for line in lines:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    distro_info[k] = v.strip('"')
            return distro_info.get("PRETTY_NAME", "Unknown Linux Distro")
    except FileNotFoundError:
        return "Not available (Not Linux or /etc/os-release missing)"

def get_uptime():
    """
    Sistem acik kalma suresini (uptime) alir.
    """
    try:
        uptime_seconds = float(subprocess.check_output(['cat', '/proc/uptime']).split()[0])
        uptime_hours = uptime_seconds / 3600
        return f"{uptime_hours:.2f} hours"
    except Exception as e:
        return f"Could not determine uptime: {e}"

def main():
    print("[-] Sistem bilgisi toplaniyor...")
    
    data = get_system_info()
    
    if data["platform"] == "Linux":
        data["distro"] = get_linux_distro()
        data["uptime"] = get_uptime()
    
    print("[-] Bilgiler derlendi.")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    # Istenirse dosyaya da kaydedebiliriz
    filename = f"sys_info_{data['hostname']}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[-] Rapor kaydedildi: {filename}")

if __name__ == "__main__":
    main()
