import os
import sys
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QUrl, QStandardPaths, QSettings
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineDownloadRequest
from UI.ИТДDesktopRoot import Ui_MainWindow
from Theme.themes import ThemeManager
from settings_window import SettingsDialog
from updater import UpdateCheckerThread

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --no-sandbox"

def resource_path(relative_path: str) -> str:
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.settings = QSettings("ITD_Client_Community", "ITDDesktop")
        app_data = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        base_dir = os.path.join(app_data, "ITDDesktopClient")
        storage_path = os.path.join(base_dir, "UserData")
        cache_path = os.path.join(base_dir, "Cache")
        os.makedirs(storage_path, exist_ok=True)
        os.makedirs(cache_path, exist_ok=True)
        self.profile = QWebEngineProfile("ITD_Persistent_Profile", self)
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        self.profile.setCachePath(cache_path)
        base_ua = self.profile.httpUserAgent()
        self.profile.setHttpUserAgent(f"{base_ua} ИТД Desktop Client")
        self.profile.downloadRequested.connect(self.on_download_requested)
        page = QWebEnginePage(self.profile, self.ui.webEngineView)
        self.ui.webEngineView.setPage(page)
        self.ui.webEngineView.setUrl(QUrl("https://xn--d1ah4a.com/"))
        layout = QtWidgets.QVBoxLayout(self.ui.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.webEngineView)
        self.ui.webEngineView.urlChanged.connect(self.on_url_changed)
        self.ui.webEngineView.loadFinished.connect(self.on_page_load_finished)
        self.bind_menu_actions()
        is_dark = self.settings.value("dark_theme", False, type=bool)
        ThemeManager.apply_app_theme(self, is_dark)
        QtCore.QTimer.singleShot(1000, self.start_update_check)
        icon_path = resource_path("favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))
    def on_download_requested(self, download: QWebEngineDownloadRequest):
        default_dl = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
        target_dir = self.settings.value("download_path", default_dl, type=str)
        file_path = os.path.join(target_dir, download.downloadFileName())
        download.setDownloadDirectory(target_dir)
        download.setDownloadFileName(file_path)
        download.accept()
    def on_page_load_finished(self, ok: bool):
        if ok:
            is_dark = self.settings.value("dark_theme", False, type=bool)
            self.ui.webEngineView.page().runJavaScript(ThemeManager.get_theme_script(is_dark))
    def on_theme_updated(self, is_dark: bool):
        ThemeManager.apply_app_theme(self, is_dark)
        self.ui.webEngineView.page().runJavaScript(ThemeManager.get_theme_script(is_dark))
    def bind_menu_actions(self):
        self.ui.menubar.installEventFilter(self)
    def eventFilter(self, source, event):
        if source == self.ui.menubar and event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                action = self.ui.menubar.actionAt(event.pos())
                if action:
                    self.handle_menu_click(action)
                    return True
        return super().eventFilter(source, event)
    def handle_menu_click(self, action):
        if action == self.ui.menu.menuAction():
            self.ui.webEngineView.back()
        elif action == self.ui.menu_2.menuAction():
            self.ui.webEngineView.forward()
        elif action == self.ui.menuR.menuAction():
            self.ui.webEngineView.reload()
        elif action == self.ui.menu_3.menuAction():
            self.ui.webEngineView.setUrl(QUrl("https://xn--d1ah4a.com/"))
        elif action == self.ui.menu_4.menuAction():
            self.ui.webEngineView.setUrl(QUrl("https://xn--d1ah4a.com/shop"))
        elif action == self.ui.menu_5.menuAction():
            self.ui.webEngineView.setUrl(QUrl("https://xn--d1ah4a.com/search"))
        elif action == self.ui.menu_6.menuAction():
            self.ui.webEngineView.setUrl(QUrl("https://xn--d1ah4a.com/event"))
        elif action == self.ui.menu_7.menuAction():
            self.ui.webEngineView.setUrl(QUrl("https://xn--d1ah4a.com/notifications"))
        elif action == self.ui.menu_8.menuAction():
            self.ui.webEngineView.setUrl(QUrl("https://xn--d1ah4a.com/@me"))
        elif action == self.ui.menu_9.menuAction():
            self.open_settings()
    def on_url_changed(self, url: QUrl):
        self.setWindowTitle(f"ИТД Desktop | {url.toString()}")
    def open_settings(self):
        self.settings_dlg = SettingsDialog(self)
        self.settings_dlg.theme_changed.connect(self.on_theme_updated)
        is_dark = self.settings.value("dark_theme", False, type=bool)
        ThemeManager.apply_app_theme(self.settings_dlg, is_dark)
        self.settings_dlg.show()
    def start_update_check(self):
        print("[Main] Инициализация потока обновления...")
        self.updater_thread = UpdateCheckerThread(self)
        self.updater_thread.update_available.connect(self.show_update_dialog)
        self.updater_thread.start()
    def show_update_dialog(self, new_version: str):
        print(f"[Main] Открываем диалог обновления до v{new_version}")
        box = QtWidgets.QMessageBox(self)
        box.setWindowTitle("Обновление клиента")
        box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        box.setText(f"Доступна новая версия клиента: <b>v{new_version}</b>")
        box.setInformativeText("Хотите открыть страницу загрузки репозитория?")
        btn_open = box.addButton("Открыть", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        box.addButton("Позже", QtWidgets.QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(btn_open)
        box.exec()

        if box.clickedButton() == btn_open:
            QtGui.QDesktopServices.openUrl(
                QUrl("https://github.com/xachapyri-dev/itd_Desktop/releases/latest")
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())