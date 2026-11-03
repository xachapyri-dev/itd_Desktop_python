import os
import sys
import json
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QUrl, QStandardPaths, QSettings, pyqtSlot, QObject
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEnginePage,
    QWebEngineDownloadRequest,
    QWebEngineScript,
)
from PyQt6.QtWebChannel import QWebChannel
from UI.ИТДDesktopRoot import Ui_MainWindow
from Theme.themes import ThemeManager
from settings_window import SettingsDialog
from updater import UpdateCheckerThread
import autostart

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --no-sandbox"


def resource_path(relative_path: str) -> str:
    if getattr(sys, "frozen", False):
        base_path = os.path.join(sys._MEIPASS, "app")
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class WebBridge(QObject):
    message_received = QtCore.pyqtSignal(str)

    @pyqtSlot(str)
    def postMessage(self, json_str: str):
        self.message_received.emit(json_str)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.settings = QSettings("ITD_Client_Community", "ITDDesktop")
        self.really_exit = False

        self.init_profile()
        self.init_webchannel()
        self.init_tray()

        layout = QtWidgets.QVBoxLayout(self.ui.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.webEngineView)

        self.ui.webEngineView.urlChanged.connect(self.on_url_changed)
        self.ui.webEngineView.loadFinished.connect(self.on_page_load_finished)
        self.bind_menu_actions()

        is_dark = self.settings.value("dark_theme", False, type=bool)
        ThemeManager.apply_app_theme(self, is_dark)
        QtCore.QTimer.singleShot(1500, self.start_update_check)

        icon_path = resource_path("favicon.ico")
        if os.path.exists(icon_path):
            app_icon = QtGui.QIcon(icon_path)
            self.setWindowIcon(app_icon)
            self.tray_icon.setIcon(app_icon)

    def init_profile(self):
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

        self.profile.downloadRequested.connect(self.on_download_requested)

        page = QWebEnginePage(self.profile, self.ui.webEngineView)
        self.ui.webEngineView.setPage(page)
        self.ui.webEngineView.setUrl(QUrl("https://xn--d1ah4a.com/"))

    def init_webchannel(self):
        self.channel = QWebChannel(self)
        self.bridge = WebBridge()
        self.bridge.message_received.connect(self.handle_web_message)
        self.channel.registerObject("pyBridge", self.bridge)
        self.ui.webEngineView.page().setWebChannel(self.channel)

        inject_code = """
        (() => {
            function setupChannel() {
                if (window.qt && window.qt.webChannelTransport) {
                    new QWebChannel(qt.webChannelTransport, function (channel) {
                        window.pyBridge = channel.objects.pyBridge;
                    });
                }
            }

            if (typeof QWebChannel === 'undefined') {
                const script = document.createElement('script');
                script.src = 'qrc:///qtwebchannel/qwebchannel.js';
                script.onload = setupChannel;
                document.head.appendChild(script);
            } else {
                setupChannel();
            }

            // Перехват стрима входящих уведомлений
            const origGetReader = ReadableStream.prototype.getReader;
            ReadableStream.prototype.getReader = function(...args) {
                const reader = origGetReader.apply(this, args);
                const origRead = reader.read;
                let isNotificationStream = false;
                let buffer = '';
                const decoder = new TextDecoder();

                reader.read = async function() {
                    const result = await origRead.apply(this, arguments);
                    const { done, value } = result;

                    if (!done && value) {
                        const chunk = decoder.decode(value, { stream: true });
                        if (!isNotificationStream && (chunk.includes('data:') || chunk.includes('notifications'))) {
                            isNotificationStream = true;
                        }

                        if (isNotificationStream) {
                            buffer += chunk;
                            const lines = buffer.split('\\n');
                            buffer = lines.pop();

                            for (const line of lines) {
                                const trimmed = line.trim();
                                if (trimmed.startsWith('data:')) {
                                    const raw = trimmed.replace(/^data:\\s*/, '');
                                    try {
                                        if (window.pyBridge) {
                                            window.pyBridge.postMessage(raw);
                                        }
                                    } catch (e) {}
                                }
                            }
                        }
                    }
                    return result;
                };
                return reader;
            };
        })();
        """

        script = QWebEngineScript()
        script.setSourceCode(inject_code)
        script.setName("ITDBridge")
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        self.profile.scripts().insert(script)

    def init_tray(self):
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())
        self.tray_icon.setToolTip("ИТД Desktop")

        tray_menu = QtWidgets.QMenu()
        open_action = tray_menu.addAction("Открыть клиент")
        open_action.triggered.connect(self.restore_window)

        settings_action = tray_menu.addAction("Настройки")
        settings_action.triggered.connect(self.open_settings)

        tray_menu.addSeparator()

        exit_action = tray_menu.addAction("Выход")
        exit_action.triggered.connect(self.force_exit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def on_tray_activated(self, reason):
        if reason in (
            QtWidgets.QSystemTrayIcon.ActivationReason.Trigger,
            QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.restore_window()

    def restore_window(self):
        self.showNormal()
        self.activateWindow()

    def force_exit(self):
        self.really_exit = True
        self.tray_icon.hide()
        QtWidgets.QApplication.quit()

    def closeEvent(self, event: QtGui.QCloseEvent):
        if not self.really_exit:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "ИТД Desktop",
                "Клиент свернут в трей и продолжит присылать уведомления.",
                QtWidgets.QSystemTrayIcon.MessageIcon.Information,
                2500,
            )
        else:
            event.accept()

    def handle_web_message(self, json_str: str):
        try:
            data = json.loads(json_str)

            action = data.get("itdAction")
            if action:
                if action == "enable_autostart":
                    autostart.set_autostart(True)
                    self.tray_icon.showMessage(
                        "ИТД Desktop",
                        "Автозагрузка успешно включена!",
                        QtWidgets.QSystemTrayIcon.MessageIcon.Information,
                        3000,
                    )
                self.settings.setValue("first_run_done", True)
                return

            type_ = data.get("type")
            if not type_:
                return

            actor = data.get("actor", {})
            author = actor.get("displayName") or actor.get("username") or "Пользователь"
            preview = data.get("preview", "")

            title = "ИТД Desktop"
            msg = ""

            if type_ == "like":
                title = "Новая реакция"
                msg = f"{author} оценил(а) ваш пост: \"{preview}\"" if preview else f"{author} оценил(а) ваш пост"
            elif type_ == "comment":
                title = "Новый комментарий"
                msg = f"{author}: \"{preview}\"" if preview else f"{author} оставил(а) комментарий"
            elif type_ == "comment_like":
                title = "Реакция на комментарий"
                msg = f"{author} оценил(а) комментарий: \"{preview}\"" if preview else f"{author} оценил(а) ваш комментарий"
            elif type_ == "reply":
                title = "Ответ на комментарий"
                msg = f"{author} ответил(а): \"{preview}\"" if preview else f"{author} ответил(а) на ваш комментарий"
            elif type_ == "mention":
                title = "Новое упоминание"
                msg = f"{author} упомянул(а) вас: \"{preview}\"" if preview else f"{author} упомянул(а) вас"
            elif type_ == "follow":
                title = "Новый подписчик"
                msg = f"{author} подписался(-ась) на вас"
            elif type_ == "repost":
                title = "Репост"
                msg = f"{author} сделал(а) репост вашей записи"
            elif type_ == "wall_post":
                title = "Запись на стене"
                msg = f"{author} на стене: \"{preview}\"" if preview else f"{author} опубликовал(а) запись на вашей стене"
            else:
                return

            if len(msg) > 120:
                msg = msg[:117] + "..."

            self.tray_icon.showMessage(title, msg, QtWidgets.QSystemTrayIcon.MessageIcon.Information, 4000)

        except Exception as ex:
            print(f"[Bridge] Ошибка обработки WebMessage: {ex}")

    def on_page_load_finished(self, ok: bool):
        if ok:
            is_dark = self.settings.value("dark_theme", False, type=bool)
            self.ui.webEngineView.page().runJavaScript(ThemeManager.get_theme_script(is_dark))

            if not self.settings.value("first_run_done", False, type=bool):
                self.show_welcome_modal()

    def show_welcome_modal(self):
        modal_js = """
        (() => {
            if (document.getElementById('itd-welcome-popup')) return;

            const overlay = document.createElement('div');
            overlay.id = 'itd-welcome-popup';
            overlay.style.cssText = `
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background: rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(6px);
                -webkit-backdrop-filter: blur(6px);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000000;
                padding: 16px;
                box-sizing: border-box;
            `;

            const modal = document.createElement('div');
            modal.style.cssText = `
                background: var(--modal-bg, #111111);
                color: var(--text-primary, #f5f5f5);
                border: 1px solid var(--border-color, rgba(255, 255, 255, 0.15));
                border-radius: var(--radius-md, 12px);
                box-shadow: var(--shadow-elevated, 0 8px 32px rgba(0, 0, 0, 0.4));
                width: 100%;
                max-width: 480px;
                padding: 24px;
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                gap: 16px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            `;

            modal.innerHTML = `
                <div style='display: flex; flex-direction: column; gap: 8px;'>
                    <h2 style='margin: 0; font-size: 20px; font-weight: 700; color: var(--text-primary);'>
                        Приветствуем в ИТД Desktop! 👋
                    </h2>
                    <p style='margin: 0; font-size: 14px; line-height: 1.5; color: var(--text-secondary);'>
                        Спасибо, что скачали наш клиент!
                    </p>
                </div>

                <div style='background: var(--block-bg-secondary, rgba(255,255,255,0.05)); border: 1px solid var(--border-subtle); padding: 14px; border-radius: 8px; font-size: 14px; line-height: 1.5;'>
                    В приложении работает мгновенная доставка системных уведомлений. Чтобы не пропускать реакции и комментарии, клиенту требуется запуск вместе с системой.
                </div>

                <div style='display: flex; gap: 10px; margin-top: 4px;'>
                    <button id='itd-btn-yes' style='
                        flex: 1;
                        background: var(--btn-primary-bg, #ffffff);
                        color: var(--btn-primary-text, #000000);
                        border: none;
                        padding: 10px 14px;
                        border-radius: 6px;
                        font-size: 14px;
                        font-weight: 600;
                        cursor: pointer;
                    '>Да, включить автозагрузку</button>

                    <button id='itd-btn-no' style='
                        flex: 1;
                        background: transparent;
                        color: var(--text-primary, #ffffff);
                        border: 1px solid var(--border-color, rgba(255, 255, 255, 0.2));
                        padding: 10px 14px;
                        border-radius: 6px;
                        font-size: 14px;
                        font-weight: 500;
                        cursor: pointer;
                    '>Нет, не надо</button>
                </div>

                <div style='display: flex; flex-direction: column; gap: 8px; border-top: 1px solid var(--border-subtle); padding-top: 12px;'>
                    <div style='font-size: 11px; line-height: 1.4; color: var(--text-secondary); text-align: center;'>
                        Данное клиентское приложение "ИТД Desktop" является неофициальным клиентом для социальной сети ИТД. Официальная поддержка от ООО «НОУКИ» не предоставляется.
                    </div>
                    <div style='font-size: 11px; line-height: 1.4; color: var(--text-secondary); text-align: center;'>
                        Приложение не включает автозагрузку без вашего ведома. При подозрениях можно 
                        <a href='https://github.com/xachapyri-dev/itd_Desktop_python' target='_blank' style='color: var(--link-color, #6a9fd4); text-decoration: underline;'>посмотреть открытый исходный код</a>.
                    </div>
                </div>
            `;

            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            document.getElementById('itd-btn-yes').onclick = () => {
                overlay.remove();
                if (window.pyBridge) {
                    window.pyBridge.postMessage(JSON.stringify({ itdAction: 'enable_autostart' }));
                }
            };

            document.getElementById('itd-btn-no').onclick = () => {
                overlay.remove();
                if (window.pyBridge) {
                    window.pyBridge.postMessage(JSON.stringify({ itdAction: 'dismiss_welcome' }));
                }
            };
        })();
        """
        self.ui.webEngineView.page().runJavaScript(modal_js)

    def on_download_requested(self, download: QWebEngineDownloadRequest):
        default_dl = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
        target_dir = self.settings.value("download_path", default_dl, type=str)
        download.setDownloadDirectory(target_dir)
        download.accept()

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
        print("[Main] Проверка обновлений...")
        self.updater_thread = UpdateCheckerThread(self)
        self.updater_thread.update_available.connect(self.show_update_dialog)
        self.updater_thread.start()

    def show_update_dialog(self, new_version: str):
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
                QUrl("https://github.com/xachapyri-dev/itd_Desktop_python/releases/latest")
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())