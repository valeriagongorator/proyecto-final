from src.main_qt import WordHuntApp

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = WordHuntApp()
    window.show()
    sys.exit(app.exec_())
