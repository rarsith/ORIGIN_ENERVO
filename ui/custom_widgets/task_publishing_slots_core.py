import sys
from PySide2 import QtWidgets
from ui.custom_widgets.task_publishing_slots_UI import PublishSlotsWidgetUI
from database.entities.db_entities import DbProject, DbTasks, DbPubSlot

SLOTS_TYPES = ['abc', 'tex', 'vdb', 'bgeo', 'ptc', 'rend', 'exr', 'mat', 'pbr','img','scn', 'geo', 'csh', 'cfg']
SLOTS_SCOPE = ["build", "shots"]
SLOT_MODE = ["layer", "non_layer"]
SLOT_ARTISTS =["unassigned"]
SLOTS_METHODS = {'m1':'sf_csh',
                 'm2':'mf_csh',
                 'm3':'sf_geo',
                 'm4':'geo_bake',
                 'm5':'geo_sim',
                 'm6':'scn_exp',
                 'm7':'img_exp',
                 'm8':'anm_crv',
                 'm9':'scatter',
                 'm10':'p_exp',
                 'm11':'assign_exp',
                 'm12':'cfg_scn_exp',
                 'm13':'cfg_exp'}



class PublishSlotsWidgetCore(PublishSlotsWidgetUI):
    def __init__(self, parent=None):
        super(PublishSlotsWidgetCore, self).__init__(parent)

        self.create_connections()
        self.populate_main_widget()

    def create_connections(self):
        self.delete_list_item_btn.clicked.connect(self.remove_pub_slot)
        self.save_btn.clicked.connect(self.db_commit)
        self.refresh_btn.clicked.connect(self.populate_main_widget)
        self.add_pub_slot_btn.clicked.connect(self.add_to_pub_list)

# PublishSlotsWidget -- START
    def get_properties(self):
        pub_slots = DbPubSlot().get_pub_slots()
        return pub_slots

    def populate_main_widget(self):
        properties = self.get_properties()
        if not properties is None:
            rows_cnt = len(properties)
            self.publish_slots_wdg.setRowCount(rows_cnt)
            cnt = 0
            for name in properties:
                self.create_pub_slots(name, cnt)
                cnt += 1
        return properties

    def create_pub_slots(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)
        self.publish_slots_wdg.setItem(row, 0, item)

        self.set_type_cb = QtWidgets.QComboBox()
        self.set_type_cb.addItems(SLOTS_TYPES)

        self.set_method_cb = QtWidgets.QComboBox()
        self.set_method_cb.addItems(list(SLOTS_METHODS.values()))

        self.set_source_cb = QtWidgets.QComboBox()
        self.set_source_cb.addItems(self.get_current_pub_slots())

        self.set_scope_cb = QtWidgets.QComboBox()
        self.set_scope_cb.addItems(SLOTS_SCOPE)

        self.set_mode_cb = QtWidgets.QComboBox()
        self.set_mode_cb.addItems(SLOT_MODE)

        self.set_used_by_lw = QtWidgets.QListWidget()
        curr_used_by = self.get_db_pub_attr(name, 'used_by')
        for task in curr_used_by:
            QtWidgets.QListWidgetItem(task, self.set_used_by_lw)

        self.set_artists_lw = QtWidgets.QListWidget()
        curr_artists = self.get_db_pub_attr(name, 'artists')
        for artist in curr_artists:
            QtWidgets.QListWidgetItem(artist, self.set_artists_lw)

        self.set_reviewable_ckb = QtWidgets.QCheckBox()
        self.set_active_ckb = QtWidgets.QCheckBox()

        try:
            self.set_type_cb.setCurrentText(str(self.get_db_pub_attr(name, "type")))
            self.set_method_cb.setCurrentText(str(self.get_db_pub_attr(name, 'method')))
            self.set_source_cb.setCurrentText(str(self.get_db_pub_attr(name, 'source')))
            self.set_scope_cb.setCurrentText(str(self.get_db_pub_attr(name, 'scope')))
            self.set_mode_cb.setCurrentText(str(self.get_db_pub_attr(name, 'mode')))
            self.set_artists_lw.setCurrentText(str(self.get_db_pub_attr(name, 'artists')))
            self.set_reviewable_ckb.setChecked(bool(self.get_db_pub_attr(name, 'reviewable')))
            self.set_active_ckb.setChecked(bool(self.get_db_pub_attr(name, 'active')))

        except:
            pass

        self.publish_slots_wdg.setCellWidget(row, 1, self.set_type_cb)
        self.publish_slots_wdg.setCellWidget(row, 2, self.set_method_cb)
        self.publish_slots_wdg.setCellWidget(row, 3, self.set_source_cb)
        self.publish_slots_wdg.setCellWidget(row, 4, self.set_scope_cb)
        self.publish_slots_wdg.setCellWidget(row, 5, self.set_mode_cb)
        self.publish_slots_wdg.setCellWidget(row, 6, self.set_used_by_lw)
        self.publish_slots_wdg.setCellWidget(row, 7, self.set_artists_lw)
        self.publish_slots_wdg.setCellWidget(row, 8, self.set_reviewable_ckb)
        self.publish_slots_wdg.setCellWidget(row, 9, self.set_active_ckb)

    def get_db_pub_attr(self, slot, attr):
        properties = self.get_properties()
        to_attr = properties[slot]
        if attr not in to_attr.keys():
            return ["--NA--"]

        pub_attr = properties[slot][attr]
        return pub_attr

    def get_slot_name(self, row, column):
        slot_name = self.publish_slots_wdg.item(row, column)
        return slot_name.text()

    def get_slot_type(self, row, column):
        slot_type = self.publish_slots_wdg.cellWidget(row, column)
        return slot_type.currentText()

    def get_pub_method(self, row, column):
        slot_method = self.publish_slots_wdg.cellWidget(row, column)
        return slot_method.currentText()

    def get_pub_source(self, row, column):
        slot_source = self.publish_slots_wdg.cellWidget(row, column)
        return slot_source.currentText()

    def get_pub_scope(self, row, column):
        slot_scope = self.publish_slots_wdg.cellWidget(row, column)
        return slot_scope.currentText()

    def get_pub_mode(self, row, column):
        slot_mode = self.publish_slots_wdg.cellWidget(row, column)
        return slot_mode.currentText()

    def get_pub_artists(self, row, column):
        slot_artists = self.publish_slots_wdg.cellWidget(row, column)
        return slot_artists.currentText()

    def reviewable_is_checked(self, row, column):
        rev_checked = self.publish_slots_wdg.cellWidget(row, column)
        return rev_checked.isChecked()

    def active_is_checked(self, row, column):
        act_is_checked = self.publish_slots_wdg.cellWidget(row, column)
        return act_is_checked.isChecked()

    def get_pub_buffer_content(self):
        items = []
        rows = self.publish_slots_wdg.rowCount()

        for r in range(rows):
            get_slot_name = self.get_slot_name(r, 0)
            get_existing_properties = self.get_properties()
            if get_slot_name in get_existing_properties:
                get_used_by = self.get_db_slot_used_by(get_slot_name)
            else:
                get_used_by = []

            dictionary_build = {self.get_slot_name(r, 0) : {'type':self.get_slot_type(r, 1),
                                                            'method':self.get_pub_method(r, 2),
                                                            'used_by':get_used_by,
                                                            'source':self.get_pub_source(r, 3),
                                                            'scope':self.get_pub_scope(r, 4),
                                                            'mode':self.get_pub_mode(r, 5),
                                                            'artists':self.get_pub_artists(r, 7),
                                                            'reviewable':self.reviewable_is_checked(r, 8),
                                                            'active':self.active_is_checked(r, 9)}}

            items.append(dictionary_build)



        return items

    def get_db_slot_used_by(self, slot):
        properties = self.get_properties()
        pub_is_used_by = properties[slot]['used_by']
        return pub_is_used_by

    def get_first_cell(self):
        clickme = QtWidgets.QApplication.focusWidget()
        index = self.publish_slots_wdg.indexAt(clickme.pos())
        if index.isValid():
            get_name_cell = (index.column()-3)
            slot_name = self.publish_slots_wdg.item(index.row(), get_name_cell)
            print ('Open Menu for {0}'.format (slot_name.text()))
            return slot_name.text()

    def get_current_pub_slots(self):
        complete_list = list()
        pub_slots = DbPubSlot().get_pub_slots()
        if pub_slots:
            complete_list.append('root')
            for each in list(pub_slots.keys()):
                complete_list.append(each)

        return complete_list

    def insert_pub_slot_row(self, name):
        self.publish_slots_wdg.insertRow(0)
        self.create_pub_slots(name, 0)

    def remove_pub_slot(self):
        listItems = self.publish_slots_wdg.currentItem()
        selected_index = self.publish_slots_wdg.indexFromItem(listItems)
        self.publish_slots_wdg.removeRow(selected_index.row())

    def db_commit(self):
        get_wdg_content = self.get_pub_buffer_content()
        print (get_wdg_content)
        DbPubSlot().remove_all()
        DbPubSlot().add_dict(pub_slot=get_wdg_content)

# PublishSlotsWidget -- END

    def add_to_pub_list(self):
        if self.add_pub_slot_le.text():
            self.insert_pub_slot_row(self.add_pub_slot_le.text())
            self.add_pub_slot_le.clear()
        else:
            return

if __name__ == "__main__":
    from envars.envars import Envars

    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "red_hulk"
    Envars.task_name = "modeling"



    app = QtWidgets.QApplication(sys.argv)

    test_dialog = PublishSlotsWidgetCore()

    test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())