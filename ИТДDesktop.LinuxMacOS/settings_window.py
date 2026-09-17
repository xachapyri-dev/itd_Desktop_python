import os
import shutil
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QUrl, QSettings, QStandardPaths
from Theme.themes import ThemeManager
from UI.ИТДDesktopSetings import Ui_MainWindow as Ui_SettingsWindow


class SettingsDialog(QtWidgets.QMainWindow):
    theme_changed = QtCore.pyqtSignal(bool)
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_win = main_window
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        self.settings = QSettings("ITD_Client_Community", "ITDDesktop")
        self.load_settings()
        self.bind_events()
    def load_settings(self):
        default_dl = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
        download_path = self.settings.value("download_path", default_dl, type=str)
        self.ui.lineEdit.setText(download_path)
        is_dark = self.settings.value("dark_theme", False, type=bool)
        self.ui.checkBox.setChecked(is_dark)
    def bind_events(self):
        self.ui.pushButton.clicked.connect(self.choose_download_dir)
        self.ui.pushButton_2.clicked.connect(self.clear_browser_data)
        self.ui.checkBox.toggled.connect(self.toggle_theme)
        self.ui.commandLinkButton.clicked.connect(
            lambda: QtGui.QDesktopServices.openUrl(QUrl("https://github.com/xachapyri-dev/itd_Desktop_python"))
        )
        self.ui.commandLinkButton_2.clicked.connect(
            lambda: QtGui.QDesktopServices.openUrl(QUrl("https://github.com/xachapyri-dev"))
        )
        self.ui.commandLinkButton_3.clicked.connect(
            lambda: QtGui.QDesktopServices.openUrl(QUrl("https://t.me/nowkies"))
        )
        self.ui.commandLinkButton_4.clicked.connect(
            lambda: QtGui.QDesktopServices.openUrl(QUrl("https://t.me/kroshidanielYouTube"))
        )
        self.ui.commandLinkButton_5.clicked.connect(
            lambda: QtGui.QDesktopServices.openUrl(QUrl("https://github.com/xachapyri-dev/itd_Desktop_python/issues"))
        )
    def choose_download_dir(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Выбрать папку для загрузок", self.ui.lineEdit.text()
        )
        if folder:
            self.ui.lineEdit.setText(folder)
            self.settings.setValue("download_path", folder)
    def clear_browser_data(self):
        box = QtWidgets.QMessageBox(self)
        box.setWindowTitle("Подтверждение сброса")
        box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        box.setText("Вы действительно хотите удалить все данные браузера?")
        box.setInformativeText(
            "Будет выполнен сброс профиля: удалятся все сохранённые сессии, аккаунты, куки и кэш.\n\n"
            "Это действие необратимо! После сброса приложение закроется."
        )
        box.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        if box.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            self.main_win.profile.clearHttpCache()
            self.main_win.profile.cookieStore().deleteAllCookies()
            storage_path = self.main_win.profile.persistentStoragePath()
            cache_path = self.main_win.profile.cachePath()
            try:
                if os.path.exists(storage_path):
                    shutil.rmtree(storage_path, ignore_errors=True)
                if os.path.exists(cache_path):
                    shutil.rmtree(cache_path, ignore_errors=True)
            except Exception as ex:
                print(f"Ошибка удаления файлов: {ex}")
            QtWidgets.QMessageBox.information(self, "Успешно", "Данные очищены. Приложение сейчас закроется.")
            QtWidgets.QApplication.quit()
    def toggle_theme(self, checked: bool):
        self.settings.setValue("dark_theme", checked)
        ThemeManager.apply_app_theme(self, checked)
        self.theme_changed.emit(checked)