"""adding ,changing ,changing status, deleting, searching notes
, adding tag, searching by tag"""
from ab_classes import Note, NotePad, HashTag, Console, dir_path
import json
import os


with open(os.path.join(dir_path, "config.JSON")) as cfg:
    cfg_data = json.load(cfg)
    languages = True if cfg_data["Language"] == "eng" else False
    PAGE = cfg_data["Page"]


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result

        except TypeError as err:
            return err

        except AttributeError:
            if languages:
                return "Check the correctness of data inputs."
            else:
                return "Перевірте правильність набору даних."

        except ValueError as err:
            return err

        except IndexError as err:
            return err

    return wrapper


@input_error
def add_note(notebook: NotePad, *args):
    text = f'{" ".join(args)}'
    if not text:
        if languages:
            raise ValueError("enter the note text")
        else:
            raise ValueError("введіть текст нотатки")
    record = Note(text)
    notebook.add_note(record)
    if languages:
        return "Note added"
    else:
        return "Нотатка добавлена"


@input_error
def add_tag(notebook: NotePad, note, tag):
    if not tag:
        if languages:
            raise ValueError("Enter  first_letters_of_the_note... #tag")
        else:
            raise ValueError("Введіть перші_літери_нотатки... #тег")
    rec = quick_note_list(notebook, note)
    rec.add_tag(HashTag(tag))
    notebook.sorting()
    if languages:
        return f'Tag "{tag}" added to record "{rec}"'
    else:
        return f'Тег "{tag}" додано до запису "{rec}"'


@input_error
def change_note(notebook: NotePad, *args):
    if not args:
        if languages:
            raise ValueError("enter part of the note text")
        else:
            raise ValueError("введіть частину тексту нотатки")      
    search_word = args[0]
    if search_word.startswith("#"):
        record = quick_tag(notebook, search_word)
        new_note = f'{" ".join(args)}'
        new_note = new_note.replace(f'{search_word} ', "")
        if record:
            notebook.change_note(record, new_note)
            if languages:
                return f'Note changed to "{new_note}"'
            else:
                return f'Запис змінено на "{new_note}"'
    text = f'{" ".join(args)}'
    old_note, new_note = text.split("... ")
    record = quick_note_list(notebook, old_note)
    if record in notebook.note_list:
        notebook.change_note(record, new_note)
        if languages:
            return f'Note changed to "{new_note}"'
        else:
            return f'Запис змінено на "{new_note}"'
    if languages:
        return f'Record "{record}" not found'
    else:
        return f'Запис "{record}" не знайдений'


@input_error
def change_note_stat(notebook: NotePad, *args):
    text = f'{" ".join(args)}'
    if text.startswith("#"):
        record = quick_tag(notebook, text)
        if record:
            notebook.change_status(record)
            if languages:
                return f'The status of {record} has been changed to "done"'
            else:
                return f'Статус нотатки {record} змінено на "виконано"'
    record = quick_note_list(notebook, text)
    if record in notebook.note_list:
        notebook.change_status(record)
        if languages:
            return f'The status of {record} has been changed to "done"'
        else:
            return f'Статус нотатки {record} змінено на "виконано"'
    if languages:
        return f'Record "{record}" not found'
    else:
        return f'Запис "{record}" не знайдений'


@input_error
def del_note(notebook: NotePad, *args):
    text = f'{" ".join(args)}'
    if not text:
        if languages:
            raise ValueError("enter part of note text or #tag")
        else:
            raise ValueError("введіть частину тексту нотатки або #тег")
    if text.startswith("#"):
        record = quick_tag(notebook, text)
        if record:
            notebook.delete(record)
            notebook.sorting()
            if languages:
                return f'"{record}" deleted successfully'
            else:
                return f'"{record}" видалений успішно'
    record = quick_note_list(notebook, text)
    if record in notebook.note_list:
        notebook.delete(record)
        notebook.sorting()
        if languages:
            return f'"{record}" deleted successfully'
        else:
            return f'"{record}" видалений успішно'
    if languages:
        return f'Record "{record}" not found'
    else:
        return f'Запис "{record}" не знайдений'


@input_error
def search_note(notebook: NotePad, *args):
    text = f'{" ".join(args)}'
    text = text.replace("...", "")
    list_of_notes = []
    if languages:
        error = "Record not found"
    else:
        error = "Запис не знайдений"
    if text.startswith("#"):
        tag = text.replace("#", "")
        for note in notebook.note_list:
            for hashtag in note.tag_list:
                list_of_notes.append(note) if tag in str(hashtag) else None
        if languages:
            output = (
                f"Found notes for {text}"
                + "\n"
                + f'{", ".join(str(note) for note in list_of_notes)}'
            )
        else:
            output = (
                f"Знайдені нотатки за {text}"
                + "\n"
                + f'{", ".join(str(note) for note in list_of_notes)}'
            )
        return output if len(list_of_notes) != 0 else error
    for note in notebook.note_list:
        if text in str(note):
            list_of_notes.append(note)
    if languages:
        output = (
            f"Found notes for {text}"
            + "\n"
            + f'{ ", ".join(str(note) for note in list_of_notes)}'
        )
    else:
        output = (
            f"Знайдені нотатки за {text}"
            + "\n"
            + f'{ ", ".join(str(note) for note in list_of_notes)}'
        )
    return output if len(list_of_notes) != 0 else error


def show_notes(notebook: NotePad, *args):
    line = ""
    for note in notebook.note_list:
        tags = ", ".join(str(tag) for tag in note.tag_list)
        if languages:
            line += (
                f'{tags} creation date: {note.day.strftime("%d-%m-%Y")}. Content:{str(note)}. Status:{f"done. Date done {note.done_date}"if note.done else "not done"}'
                + "\n"
            )
        else:
            line += (
                f'{tags} дата створення: {note.day.strftime("%d-%m-%Y")}. Зміст:{str(note)}. Статус:{f"виконано. Дата виконання {note.done_date}"if note.done else "не виконано"}'
                + "\n"
            )
    if languages:
        return "list of notes\n" + line + "end of list of notes"
    else:
        return "список нотатків\n" + line + "кінець списку нотаток"


def quick_tag(notebook: NotePad, text: str):
    note_list = []
    for note in notebook.note_list:
        for tag in note.tag_list:
            if str(text) in str(tag):
                note_list.append(note)
    note = quick_choice(note_list)
    return note

def quick_note_list(notebook: NotePad, text: str):
    content = text.replace("...", "")
    note_list = []
    for note in notebook.note_list:
        if content in str(note):
            note_list.append(note)
    note = quick_choice(note_list)
    return note


def quick_choice(note_list):
    note_count = len(note_list)
    notes_per_iteration = PAGE
    current_index = 0
    result = None
    while current_index < note_count:
        next_index = current_index + notes_per_iteration
        notes = note_list[current_index:next_index]
        if languages:
            notes_ = "Notes"
            options = "Options"
            exit = "Exit"
            next = "for continue"
            enter = "Enter your choice"
            not_found = "Not found"
        else:
            notes_ = "Нотатки"
            options = "Опції"
            exit = "Вихід"
            next = "для продовження"
            enter = "Введіть ваш вибір"
            not_found = "Не знайдено"


        Console.user_output(f"{notes_} {current_index}-{next_index}:")
        for i, note in enumerate(notes, start=1):
            Console.user_output(f"{i}. {note}")

        Console.user_outputt(f'{options}: ')
        if next_index < note_count:
            Console.user_output(f'"next" {next}')
        Console.user_output(f'0. {exit}')

        choice = Console.user_input(f'{enter} ')

        if choice == "next" and next_index < note_count:
            current_index = next_index
            continue
        if int(choice) == 0:
            break
        elif int(choice) >= 1:
            i = int(choice) - 1
            result = notes[i]
            break
    return result if result else f'{not_found}'


WITH_NOTES = [
    add_note,
    add_tag,
    change_note,
    change_note_stat,
    show_notes,
    search_note,
    del_note,
]