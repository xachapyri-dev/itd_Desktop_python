class ThemeManager:
    LIGHT_STYLE = """
        QMainWindow, QWidget { background-color: #FFFFFF; color: #000000; }
        QMenuBar { background-color: #F0F0F0; color: #000000; }
        QMenuBar::item:selected { background-color: #E0E0E0; }
        QTabWidget::pane { border: 1px solid #D0D0D0; }
        QPushButton { background-color: #E1E1E1; color: #000000; border: 1px solid #ADADAD; padding: 4px; border-radius: 2px; }
        QPushButton:hover { background-color: #E5F1FB; border-color: #0078D7; }
        QLineEdit { background-color: #FFFFFF; color: #000000; border: 1px solid #7A7A7A; padding: 2px; }
    """

    DARK_STYLE = """
        QMainWindow, QWidget { background-color: #1E1E1E; color: #FFFFFF; }
        QMenuBar { background-color: #2D2D30; color: #FFFFFF; }
        QMenuBar::item:selected { background-color: #3E3E40; }
        QTabWidget::pane { border: 1px solid #3F3F46; }
        QTabBar::tab { background-color: #2D2D30; color: #DCDCDC; padding: 6px 12px; }
        QTabBar::tab:selected { background-color: #1E1E1E; color: #FFFFFF; }
        QPushButton { background-color: #333337; color: #FFFFFF; border: 1px solid #434346; padding: 4px; border-radius: 2px; }
        QPushButton:hover { background-color: #3E3E40; border-color: #007ACC; }
        QLineEdit { background-color: #2D2D30; color: #FFFFFF; border: 1px solid #3F3F46; padding: 2px; }
        QCheckBox { color: #FFFFFF; }
    """

    @staticmethod
    def get_theme_script(is_dark: bool) -> str:
        mode = "dark" if is_dark else "light"
        return f"""
            document.documentElement.setAttribute('data-theme', '{mode}');
            localStorage.setItem('nowkie_theme', '{mode}');
        """

    @classmethod
    def apply_app_theme(cls, app_or_window, is_dark: bool):
        app_or_window.setStyleSheet(cls.DARK_STYLE if is_dark else cls.LIGHT_STYLE)