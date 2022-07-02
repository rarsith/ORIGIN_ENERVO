import sys
from PySide2 import QtWidgets

from origin_data_base import xcg_db_actions as xac
from origin_config import xcg_validation as xval

class CreateAssetCategoryUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateAssetCategoryUI, self).__init__(parent)

        self.setWindowTitle("Create Asset Category")
        self.setMinimumSize(550, 650)
        self.setMaximumSize(550, 650)

        self.setMinimumHeight(900)
        self.setMaximumHeight(900)


        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.addItems(self.get_shows())

        categories_types = ['character', 'prop', 'environment']
        self.type_cb = QtWidgets.QComboBox()
        self.type_cb.addItems(categories_types)
        self.type_cb.setPlaceholderText('Select Type')

        self.seq_name_le = QtWidgets.QLineEdit()

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name: ", self.show_name_cb)
        form_layout.addRow("Asset Category Name:", self.seq_name_le)
        form_layout.addRow("Category Type:", self.type_cb)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.show_name_cb.activated.connect(self.comboBox_shows)

        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        xac.create_assets_category(self.show_name_cb.currentText(), self.seq_name_le.text(), self.type_cb.currentText())
        self.seq_name_le.clear()

    def get_shows(self):
        store_shows = []
        shows = xac.db_query("show", "show_name", show_type="vfx")
        print ('This are the shows:', shows)
        for show in shows:
            store_shows.append(show)
        return store_shows



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    try:
        create_shot.close()
        create_shot.deleteLater()
    except:
        pass
    create_shot = CreateAssetCategoryUI()
    create_shot.show()
    sys.exit(app.exec_())