from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, \
    QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QInputDialog, QMessageBox
import json

app = QApplication([])

win = QWidget()
win.setWindowTitle("Розумні замітки")
win.resize(900, 600)

field_text = QTextEdit()
list_notes_label = QLabel('Список заміток')
list_notes = QListWidget()
button_note_create = QPushButton('Створити замітку')
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')
list_tags_label = QLabel('Список тегів')
list_tags = QListWidget()
field_tag = QLineEdit()
field_tag.setPlaceholderText('Введіть тег...')
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')

main_layout = QHBoxLayout()

col = QVBoxLayout()
col.addWidget(list_notes_label)
col.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
col.addLayout(row_1)

col.addWidget(button_note_save)
col.addWidget(list_tags_label)
col.addWidget(list_tags)
col.addWidget(field_tag)

row_2 = QHBoxLayout()
row_2.addWidget(button_tag_add)
row_2.addWidget(button_tag_del)
col.addLayout(row_2)

col.addWidget(button_tag_search)

main_layout.addWidget(field_text, stretch=2)
main_layout.addLayout(col, stretch=1)
win.setLayout(main_layout)

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def add_note():
    name, ok = QInputDialog.getText(win, "Додати замітку", "Уведіть назву замітки:")
    if ok and name != "":
        notes[name] = {"текст": "", "теги": []}
        list_notes.addItem(name)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
    else:
        QMessageBox(text="Замітка не обрана").exec_()

def del_note():
    if list_notes.selectedItems():
        box = QMessageBox(text="Ви дійсно хочете видалити замітку?")
        box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if box.exec() == QMessageBox.Ok:
            key = list_notes.selectedItems()[0].text()
            del notes[key]
            field_text.clear()
            list_notes.clear()
            list_notes.addItems(notes)
            list_tags.clear()
            with open("notes_data.json", "w") as file:
                json.dump(notes, file, sort_keys=True)
    else:
        QMessageBox(text="Замітка не обрана").exec_()

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag != "" and not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.clear()
            list_tags.addItems(notes[key]["теги"])
            field_tag.clear()
            with open("notes_data.json", "w") as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        QMessageBox(text="Замітка не обрана").exec_()

def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        QMessageBox(text="Замітка не обрана").exec_()

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Шукати замітки по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        list_notes.clear()
        list_notes.addItems(notes_filtered)
        list_tags.clear()
        button_tag_search.setText("Скинути пошук")
    elif button_tag_search.text() == "Скинути пошук":
        list_notes.clear()
        list_notes.addItems(notes)
        list_tags.clear()
        field_tag.clear()
        button_tag_search.setText("Шукати замітки по тегу")

list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

win.show()

with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec_()