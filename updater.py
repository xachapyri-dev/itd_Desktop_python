import json
import urllib.request
from PyQt6 import QtCore
try:
    from Data.config import version as CURRENT_VERSION
except ImportError:
    CURRENT_VERSION = "1.5.0"


class UpdateCheckerThread(QtCore.QThread):
    update_available = QtCore.pyqtSignal(str)
    API_URL = "http://k90052gj.beget.tech/API/versions.json"
    def run(self):
        print(f"[Updater] Поток запущен! Локальная версия: {CURRENT_VERSION}")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Connection": "close"
            }
            print(f"[Updater] Отправка запроса на {self.API_URL}...")
            req = urllib.request.Request(self.API_URL, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.status
                print(f"[Updater] Ответ сервера получен, статус: {status}")
                if status != 200:
                    print(f"[Updater] Ошибка: код ответа {status}")
                    return
                raw_data = response.read().decode("utf-8")
                data = json.loads(raw_data)
                itd_data = data.get("ITDdes", {})
                remote_version = str(itd_data.get("version", "")).strip()
                print(f"[Updater] Распарсенная версия на сервере: '{remote_version}'")
                if not remote_version:
                    print("[Updater] Версия не найдена в JSON файле!")
                    return
                if remote_version != CURRENT_VERSION.strip():
                    print(f"[Updater] Версия не совпадает (на сервере: v{remote_version}, у клиента: v{CURRENT_VERSION})! Шлём сигнал в UI.")
                    self.update_available.emit(remote_version)
                else:
                    print("[Updater] Версия полностью совпадает с сервером.")
        except Exception as ex:
            print(f"[Updater] Исключение при выполнении запроса: {ex}")
    @staticmethod
    def is_newer(remote_v: str, local_v: str) -> bool:
        try:
            r_parts = [int(p) for p in remote_v.strip().lstrip('v').split('.')]
            l_parts = [int(p) for p in local_v.strip().lstrip('v').split('.')]
            return r_parts > l_parts
        except Exception:
            return remote_v != local_v