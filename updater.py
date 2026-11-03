import json
import urllib.request
from PyQt6 import QtCore

try:
    from Data.config import version as CURRENT_VERSION
except ImportError:
    CURRENT_VERSION = "1.5.0"


class UpdateCheckerThread(QtCore.QThread):
    update_available = QtCore.pyqtSignal(str)

    PRIMARY_URL = "http://k90052gj.beget.tech/API/versions.json"
    FALLBACK_URL = "https://raw.githubusercontent.com/xachapyri-dev/VersionProgramCheck/refs/heads/main/versions.json"

    def run(self):
        print(f"[Updater] Поток запущен. Текущая версия: {CURRENT_VERSION}")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

        raw_data = None
        for url in [self.PRIMARY_URL, self.FALLBACK_URL]:
            try:
                print(f"[Updater] Проверка обновлений через: {url}")
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        raw_data = response.read().decode("utf-8")
                        break
            except Exception as ex:
                print(f"[Updater] Ошибка источника {url}: {ex}")

        if not raw_data:
            print("[Updater] Все серверы проверки обновлений недоступны.")
            return

        try:
            data = json.loads(raw_data)
            remote_version = str(data.get("ITDdes", {}).get("version", "")).strip()
            print(f"[Updater] Версия на сервере: '{remote_version}'")

            if remote_version and remote_version != CURRENT_VERSION.strip():
                self.update_available.emit(remote_version)
        except Exception as ex:
            print(f"[Updater] Ошибка разбора JSON: {ex}")