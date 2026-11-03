import os
import sys

APP_NAME = "ITDDesktop"


def _get_exec_command() -> str:
    if getattr(sys, 'frozen', False):
        return f'"{sys.executable}"'
    return f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'


def is_autostart_enabled() -> bool:
    if sys.platform.startswith("linux"):
        desktop_file = os.path.expanduser(f"~/.config/autostart/{APP_NAME}.desktop")
        return os.path.exists(desktop_file)
    elif sys.platform == "darwin":
        plist_file = os.path.expanduser(f"~/Library/LaunchAgents/com.xachapyri.{APP_NAME}.plist")
        return os.path.exists(plist_file)
    return False


def set_autostart(enable: bool):
    cmd = _get_exec_command()

    if sys.platform.startswith("linux"):
        autostart_dir = os.path.expanduser("~/.config/autostart")
        desktop_file = os.path.join(autostart_dir, f"{APP_NAME}.desktop")

        if enable:
            os.makedirs(autostart_dir, exist_ok=True)
            content = f"""[Desktop Entry]
Type=Application
Exec={cmd}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=ИТД Desktop
Comment=Клиент соцсети ИТД
"""
            with open(desktop_file, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            if os.path.exists(desktop_file):
                os.remove(desktop_file)

    elif sys.platform == "darwin":
        agents_dir = os.path.expanduser("~/Library/LaunchAgents")
        plist_file = os.path.join(agents_dir, f"com.xachapyri.{APP_NAME}.plist")

        if enable:
            os.makedirs(agents_dir, exist_ok=True)
            content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.xachapyri.{APP_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
            with open(plist_file, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            if os.path.exists(plist_file):
                os.remove(plist_file)