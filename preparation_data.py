def get_text_from_edit_w(edit):
    text = edit.text()
    if len(text) > 0:
        return text
    else:
        raise ValueError


def get_text_from_box_w(box):
    text = box.currentText()
    if len(text) > 0:
        return text
    else:
        raise ValueError


def get_text_from_edit(edit):
    text = edit.text()
    if len(text) > 0:
        return text
    else:
        return 'NULL'


def get_text_from_box(box):
    text = box.currentText()
    if len(text) > 0:
        return text
    else:
        return 'NULL'


def remove_spaces(string):
    split_string = string.split(' ')
    split_string_without_spaces = [x for x in split_string if x != '']
    return ' '.join(split_string_without_spaces)

