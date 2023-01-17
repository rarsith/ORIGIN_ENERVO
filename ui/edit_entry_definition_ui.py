
import sys
from PySide2 import QtWidgets, QtCore

from database.entities.db_entities import DbAsset
from envars.envars import Envars
from database.entities.db_structures import DbProjectBranch, DbAssetCategories

class EditEntryDefinitionsUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(EditEntryDefinitionsUI, self).__init__(parent)

        self.setWindowTitle("Edit Entry Definitions")
        self.setMinimumSize(550, 650)
        self.setMaximumSize(550, 650)

        self.setMinimumHeight(900)
        self.setMaximumHeight(900)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.populate_shot_definitions()

    def create_widgets(self):
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.addItem(Envars().show_name)
        self.show_branch_cb = QtWidgets.QComboBox()
        self.show_branch_cb.addItem(Envars().branch_name)
        self.category_cb = QtWidgets.QComboBox()
        self.category_cb.addItem(Envars().category)
        self.entry_name_cb = QtWidgets.QComboBox()
        self.entry_name_cb.addItem(Envars().entry_name)

        # Building the Stack menu
        # Build the Shot Definition menu
        self.shots_definition_properties_stack = QtWidgets.QWidget()
        self.shot_type_cb = QtWidgets.QComboBox()
        # self.shot_type_cb.addItems(xval.VALID_SHOTS_TYPES)
        self.preroll_le = QtWidgets.QLineEdit("0")
        self.frame_in_le = QtWidgets.QLineEdit("0")
        self.frame_out_le = QtWidgets.QLineEdit("0")
        self.full_range_in_lb = QtWidgets.QLabel("0")
        self.full_range_out_lb = QtWidgets.QLabel("0")
        self.handles_head_le = QtWidgets.QLineEdit("0")
        self.handles_tail_le = QtWidgets.QLineEdit("0")
        self.edit_cut_in_lb = QtWidgets.QLabel("0")
        self.edit_cut_out_lb = QtWidgets.QLabel("0")
        self.frame_rate_le = QtWidgets.QLineEdit("0")
        self.motion_blur_high_le = QtWidgets.QLineEdit()
        self.motion_blur_low_le = QtWidgets.QLineEdit()
        self.render_resolution_x_le = QtWidgets.QLineEdit()
        self.render_resolution_y_le = QtWidgets.QLineEdit()

        self.stacked_properties_wdg = QtWidgets.QStackedWidget()
        # self.stacked_properties_wdg.addWidget(self.assets_definition_properties_stack)
        self.stacked_properties_wdg.addWidget(self.shots_definition_properties_stack)

        self.separator_top_lb = QtWidgets.QLabel("")
        self.entry_definition_lb =  QtWidgets.QLabel("-- Definition --")
        self.separator_bottom_lb = QtWidgets.QLabel("")

        self.stacked_properties_wdg.
        self.populate_shot_definitions()
        # self.populate_asset_definitions()

        self.shot_commit_btn = QtWidgets.QPushButton("Commit")
        self.shot_commit_and_close_btn = QtWidgets.QPushButton("Commit and Close")

        self.asset_commit_btn = QtWidgets.QPushButton("Commit")
        self.asset_commit_and_close_btn = QtWidgets.QPushButton("Commit and Close")

        self.cancel_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name ", self.show_name_cb)
        form_layout.addRow("Show Branch", self.show_branch_cb)
        form_layout.addRow("Category", self.category_cb)
        form_layout.addRow("Entry Name", self.entry_name_cb)
        form_layout.setSpacing(5)
        form_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)

        separators_layout = QtWidgets.QFormLayout()
        separators_layout.addWidget(self.separator_top_lb)
        separators_layout.addWidget(self.entry_definition_lb)
        separators_layout.addWidget(self.separator_bottom_lb)

        definition_stack_layout = QtWidgets.QHBoxLayout()
        definition_stack_layout.addWidget(self.shots_definition_properties_stack)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(separators_layout)
        main_layout.addLayout(definition_stack_layout)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.frame_in_le.textChanged[str].connect(self.compute_cut_in_le)
        self.handles_head_le.textChanged[str].connect(self.compute_cut_in_le)

        self.frame_out_le.textChanged[str].connect(self.compute_cut_out_le)
        self.handles_tail_le.textChanged[str].connect(self.compute_cut_out_le)

        self.shot_commit_btn.clicked.connect(self.db_commit)
        self.shot_commit_and_close_btn.clicked.connect(self.db_commit_close)

        self.asset_commit_btn.clicked.connect(self.db_asset_commit)
        self.asset_commit_and_close_btn.clicked.connect(self.db_asset_commit_close)

        self.cancel_btn.clicked.connect(self.close)

    def populate_shot_definitions(self):
        self.shot_type_cb.setCurrentText(DbAsset().get_definition_element(definition_element="shot_type"))
        self.preroll_le.setText(DbAsset().get_definition_element(definition_element="preroll"))
        self.frame_in_le.setText(DbAsset().get_definition_element(definition_element="frame_in"))
        self.frame_out_le.setText(DbAsset().get_definition_element(definition_element="frame_out"))
        self.handles_head_le.setText(DbAsset().get_definition_element(definition_element="handles_head"))
        self.handles_tail_le.setText(DbAsset().get_definition_element(definition_element="handles_tail"))
        self.full_range_in_lb.setText(DbAsset().get_definition_element(definition_element="full_range_in"))
        self.full_range_out_lb.setText(DbAsset().get_definition_element(definition_element="full_range_out"))
        self.edit_cut_in_lb.setText(DbAsset().get_definition_element(definition_element="cut_in"))
        self.edit_cut_out_lb.setText(DbAsset().get_definition_element(definition_element="cut_out"))
        self.frame_rate_le.setText(DbAsset().get_definition_element(definition_element="frame_rate"))
        self.motion_blur_high_le.setText(str(DbAsset().get_definition_element(definition_element="motion_blur_high")))
        self.motion_blur_low_le.setText(str(DbAsset().get_definition_element(definition_element="motion_blur_low")))
        self.render_resolution_x_le.setText(DbAsset().get_definition_element(definition_element="res_x"))
        self.render_resolution_y_le.setText(DbAsset().get_definition_element(definition_element="res_y"))

    def compute_cut_in_le(self):
        try:
            get_frame_in = self.frame_in_le.text()
            get_handles_head = self.handles_head_le.text()
            calculate_cut_in = int(get_frame_in) + int(get_handles_head)
            self.edit_cut_in_lb.setText(str(calculate_cut_in))
        except:
            pass

    def compute_cut_out_le(self):
        try:
            get_frame_out = self.frame_out_le.text()
            get_handles_tail = self.handles_tail_le.text()
            calculate_cut_out = int(get_frame_out) - int(get_handles_tail)
            self.edit_cut_out_lb.setText(str(calculate_cut_out))
        except:
            pass

    def compute_shot_definition(self):
        shot_definition = { 'full_range_in':self.full_range_in_lb.text(),
                            'full_range_out':self.full_range_out_lb.text(),
                            'frame_in': self.frame_in_le.text(),
                            'frame_out': self.frame_out_le.text(),
                            'handles_head': self.handles_head_le.text(),
                            'handles_tail': self.handles_tail_le.text(),
                            'preroll': self.preroll_le.text(),
                            'shot_type': self.shot_type_cb.currentText(),
                            'cut_in':self.edit_cut_in_lb.text(),
                            'cut_out':self.edit_cut_out_lb.text(),
                            'frame_rate': self.frame_rate_le.text(),
                            'motion_blur_high': self.motion_blur_high_le.text(),
                            'motion_blur_low': self.motion_blur_low_le.text(),
                            'res_x': self.render_resolution_x_le.text(),
                            'res_y': self.render_resolution_y_le.text()}

        return shot_definition

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        DbAsset().set_definition(data=self.compute_shot_definition())

    def db_asset_commit_close(self):
        self.db_asset_commit()
        self.close()

    def db_asset_commit(self):
        DbAsset().set_definition(data=self.compute_asset_definition())

    def shot_definition_UI(self):
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.shot_commit_btn)
        buttons_layout.addWidget(self.shot_commit_and_close_btn)

        render_resolution_layout = QtWidgets.QHBoxLayout()
        render_resolution_layout.addWidget(self.render_resolution_x_le)
        render_resolution_layout.addWidget(self.render_resolution_y_le)

        labels_layout = QtWidgets.QFormLayout()
        labels_layout.addRow("Shot Type ", self.shot_type_cb)
        labels_layout.addRow("Preroll", self.preroll_le)
        labels_layout.addRow("Frame In ", self.frame_in_le)
        labels_layout.addRow("Frame Out ", self.frame_out_le)
        labels_layout.addRow("Handles Head ", self.handles_head_le)
        labels_layout.addRow("Handles Tail ", self.handles_tail_le)
        labels_layout.addRow("Full Range In ", self.full_range_in_lb)
        labels_layout.addRow("Full Range Out ", self.full_range_out_lb)
        labels_layout.addRow("Edit Cut In ", self.edit_cut_in_lb)
        labels_layout.addRow("Edit Cut Out ", self.edit_cut_out_lb)
        labels_layout.addRow("Frame rate ", self.frame_rate_le)
        labels_layout.addRow("Motion Blur High ", self.motion_blur_high_le)
        labels_layout.addRow("Motion Blur Low ", self.motion_blur_low_le)
        labels_layout.addRow("Render Resolution ", render_resolution_layout)

        labels_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        labels_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        labels_layout.setSpacing(5)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(labels_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.setSpacing(20)

        self.shots_definition_properties_stack.setLayout(main_layout)


if __name__ == "__main__":
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "gold_hulk"
    Envars.task_name = "groom"

    app = QtWidgets.QApplication(sys.argv)

    create_shot = EditEntryDefinitionsUI()
    create_shot.show()
    sys.exit(app.exec_())