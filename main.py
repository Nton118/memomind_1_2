from ab_classes import (
    dir_path,
    Console,
    Name,
    Birthday,
    Email,
    Phone,
    Address,
    Record,
    AddressBook,
    NotePad,
)
from functools import wraps
import json
import os
from pathlib import Path
from notebook import (
    WITH_NOTES,
    add_note,
    add_tag,
    change_note,
    change_note_stat,
    show_notes,
    search_note,
    del_note,
)
import re
import sort_folder


def input_error(func):
    @wraps(func)
    def wrapper(*args):
        try:
            result = func(*args)
            return result

        except TypeError as err:
            if func.__name__ == "add_birthday":
                if languages:
                    return "enter name and birthday"
                else:
                    return "введіть ім'я та день народження"
            if func.__name__ == "add_email":
                if languages:
                    return "enter name and e-mail"
                else:
                    return "введіть ім'я та e-mail"
            return err

        except AttributeError:
            if languages:
                return "Check the correctness of data inputs and if contact was created"
            else:
                return "Перевірте правильність вводу даних та чи створений контакт"

        except ValueError as err:
            return err

        except IndexError as err:
            return err

    return wrapper


def greet(*args):
    if languages:
        return "Hello, I am your personal MemoMind bot assistant. How can I help?"
    else:
        return "Вітаю, я Ваш персональний бот-помічник MemoMind  Чим можу допомогти?"


def add_contact(book: AddressBook, contact: Name, *params):
    @input_error
    def inner_add_contact():
        contact_l = [
            contact,
        ]
        phone, email, address = None, None, []
        phone_regex = r"^(\+?\d{1,3})? ?(\d{2,3}) ?(\d{2,3}) ?(\d{2}) ?(\d{2})$"

        for i, param in enumerate(params):
            if "@" in param:
                email = Email(param) if "@" in param else "-"
            elif re.match(phone_regex, param):
                phone = Phone(param)
            else:
                if i > 1:  # name can be maximum 3 words
                    address.append(param)
                else:
                    contact_l.append(param)

        contact_str = " ".join(contact_l)
        contact_new = Name(contact_str)
        address_str = " ".join(address)
        address = Address(address_str) if address_str else "-"
        email_display = email.value if email else "-"
        rec_new = Record(contact_new, phone, email, address if address_str else None)

        if contact_new.value not in book.keys():
            book.add_record(rec_new)
            if languages:
                return f"Added contact '{contact}' with phone: {phone if phone else '-'}, email: {email_display} and address: {address}"
            else:
                return f"Додано контакт '{contact}' з телефоном: {phone if phone else '-'}, електронною поштою: {email_display} та адресою: {address}"
        else:
            rec = book.get(contact)
            if phone:
                rec.add_phone(phone)
            if email:
                rec.add_email(email)
            if address_str:
                rec.add_address(address)
            if languages:
                return f"Added phone number: {phone}, email: {email} and address: {address} for existing contact '{contact}'"
            else:
                return f"Для існуючого контакту '{contact}' додано номер телефону: {phone}, електронну пошту: {email} та адресу: {address}"

    return inner_add_contact()


@input_error
def add_address(book: AddressBook, contact: str, *address):
    x = " ".join(address)
    address_new = Address(x)
    rec = book.get(contact)
    rec.add_address(address_new)
    if languages:
        return f'Added address: {x} for existing contact "{contact}"'
    else:
        return f'Для існуючого контакту "{contact}" додано адресу: {x}'


@input_error
def add_email(book: AddressBook, contact: str, email: str):
    email_new = Email(email)
    rec = book.get(contact)
    rec.add_email(email_new)
    if languages:
        return f'Added e-mail for existing contact "{contact}": {email}'
    else:
        return f'Для існуючого контакту "{contact}" додано e-mail: {email}'


@input_error
def add_birthday(book: AddressBook, contact: str, birthday: str):
    b_day = Birthday(birthday)
    rec = book.get(contact)
    rec.add_birthday(b_day)
    if languages:
        return f'Birthday added for existing contact "{contact}": {b_day}'
    else:
        return f'Для існуючого контакту "{contact}" додано день народження: {b_day}'


@input_error
def congrat(book: AddressBook, days: int):
    if days == "":
        if languages:
            raise ValueError("Enter number of days")
        else:
            raise ValueError("Введіть число днів")
    output = ""
    for contact in book.values():
        if contact.days_to_birthday() <= int(days):
            output += str(contact)
    if languages:
        text = (
            f"the following contacts haave birthdays:\n{output}"
            if output
            else "none of the contacts has a birthday"
        )
    else:
        text = (
            f"день народження в наступних контактів:\n{output}"
            if output
            else "ні в кого з контактів не має дня народження"
        )
    if languages:
        return f"During the next {days} days {text}"
    else:
        return f"В період наступних {days} днів {text}"


@input_error
def change(
    book: AddressBook,
    contact: str,
    phone: str = None,
):
    rec = book.get(contact)

    Console.user_output(rec.show_phones())

    if not rec.phones:
        if not phone:
            if languages:
                phone_new = Phone(
                    Console.user_input("If you want to add a phone number, enter the number:")
                )

            else:
                phone_new = Phone(
                    Console.user_input("Якщо хочете додати телефон введіть номер:")
                )
        else:
            phone_new = Phone(phone)
        rec.add_phone(phone_new)
        if languages:
            return f'Changed phone number to {phone_new} for contact "{contact}"'
        else:
            return f'Змінено номер телефону на {phone_new} для контакту "{contact}"'

    else:
        if len(rec.phones) == 1:
            num = 1
        if len(rec.phones) > 1:
            if languages:
                num = int(
                    Console.user_input(
                        "Which one do you want to change (enter index):"
                    )
                )
            else:
                num = int(
                    Console.user_input("Який ви хочете змінити (введіть індекс):")
                )
        if not phone:
            if languages:
                phone_new = Phone(
                    Console.user_input("Please enter a new number:")
                )
            else:
                phone_new = Phone(Console.user_input("Будь ласка введіть новий номер:"))
        else:
            phone_new = Phone(phone)
        old_phone = rec.phones[num - 1]
        rec.edit_phone(phone_new, num)
        if languages:
            return f'Changed phone number {old_phone} to {phone_new} for contact "{contact}"'
        else:
            return f'Змінено номер телефону {old_phone} на {phone_new} для контакту "{contact}"'


@input_error
def change_email(
    book: AddressBook,
    contact: str,
    email: str = None,
):
    if contact not in book:
        if languages:
            return f'The contact "{contact}" is not in the address book'
        else:
            return f'Контакт "{contact}" відсутній в адресній книзі'

    rec = book.get(contact)

    if not email:
        if languages:
            email_new = Console.user_input(
                "If you want to change the e-mail, enter a new address: "
            )
        else:
            email_new = Console.user_input(
                "Якщо хочете змінити e-mail введіть нову адресу: "
            )
    else:
        email_new = email

    rec.change_email(email_new)
    if languages:
        return f'Changed e-mail of contact "{contact}" to {email_new}'
    else:
        return f'Змінено e-mail контакту "{contact}" на {email_new}'


@input_error
def change_birthday(book: AddressBook, contact: str, birthday: str):
    rec = book.get(contact)
    new_birthday = Birthday(birthday)
    rec.change_birthday(new_birthday)
    if languages:
        return f'Changed birthday to {new_birthday} for contact "{contact}"'
    else:
        return f'Змінено дату народження на {new_birthday} для контакту "{contact}"'


@input_error
def change_address(book: AddressBook, contact: str, *address):
    x = " ".join(address)
    address_new = Address(x)
    rec = book.get(contact)

    if not rec.address:
        if not x:
            if languages:
                address_new = Address(
                    Console.user_input(
                       "If you want to add an address, enter it:"
                    )
                )
            else:
                address_new = Address(
                    Console.user_input("Якщо хочете додати адресу, введіть її:")
                )
        else:
            address_new = Address(x)
        rec.add_address(address_new)
        if languages:
            return f'Added {address_new} for contact "{contact}"'
        else:
            return f'Додано адресу {address_new} для контакту "{contact}"'
    else:
        if not x:
            if languages:
                address_new = Address(
                    Console.user_input("Please enter a new address:")
                )
            else:
                address_new = Address(
                    Console.user_input("Будь ласка, введіть нову адресу:")
                )
        else:
            address_new = Address(x)
        old_address = rec.address
        rec.change_address(address_new)
        if languages:
            return f'Changed address {old_address} to {address_new} for contact "{contact}"'
        else:
            return f'Змінено адресу {old_address} на {address_new} для контакту "{contact}"'


@input_error
def del_phone(book: AddressBook, contact: str, phone=None):
    rec = book.get(contact)
    rec.del_phone()
    if languages:
        return f"Contact {contact}, phone number deleted"
    else:
        return f"Контакт {contact}, телефон видалено"


@input_error
def del_email(book: AddressBook, *args):
    contact = " ".join(args)
    rec = book.get(contact)
    rec.email = None
    if languages:
        return f"Contact {contact}, e-mail deleted"
    else:
        return f"Контакт {contact}, e-mail видалено"


@input_error
def del_contact(book: AddressBook, *args):
    contact = " ".join(args)
    rec = book.get(contact)
    if not rec:
        raise AttributeError
    ans = None
    while ans != "y":
        if languages:
            ans = Console.user_input(
                f"Are you sure you want to delete {contact}? (Y/N)"
            ).lower()
        else:
            ans = Console.user_input(
                f"Ви впевнені що хочете видалити контакт {contact}? (Y/N)"
            ).lower()
    if languages:
        return f"Contact {book.remove_record(contact)} Removed!"
    else:
        return f"Контакт {book.remove_record(contact)} Видалено!"


@input_error
def del_birthday(book: AddressBook, *args):
    contact = " ".join(args)
    rec = book.get(contact)
    rec.birthday = None
    if languages:
        return f"Contact {contact}, birthday deleted"
    else:
        return f"Контакт {contact}, день народження видалений"


@input_error
def del_address(book: AddressBook, *args):
    contact = " ".join(args)
    rec = book.get(contact)
    rec.address = None
    if languages:
        return f"Contact {contact}, address deleted"
    else:
        return f"Контакт {contact}, адреса видалена"


def load_data(book1: AddressBook, notebook: NotePad):
    global db_file_name, note_file_name, PAGE, languages
    with open(os.path.join(dir_path, "config.JSON")) as cfg:
        cfg_data = json.load(cfg)
        db_file_name = os.path.join(dir_path, cfg_data["PhoneBookFile"])
        note_file_name = os.path.join(dir_path, cfg_data["NoteBookFile"])
        PAGE = cfg_data["Page"]
        languages = True if cfg_data["Language"] == "eng" else False


    if Path(db_file_name).exists():
        book1.load_from_file(db_file_name)
    if Path(note_file_name).exists():
        notebook.load_from_file(note_file_name)
    pass


@input_error
def phone(book: AddressBook, *args):
    contact = " ".join(args)
    rec = book.get(contact)
    if languages:
        return f'Contact "{contact}". {rec.show_phones()}'
    else:
        return f'Контакт "{contact}". {rec.show_phones()}'


def save_data(book: AddressBook, notebook: NotePad):
    book.save_to_file(db_file_name)
    notebook.save_to_file(note_file_name)


def show_all(book: AddressBook, *args):
    if len(book) <= PAGE:
        return book.show_all()
    else:
        gen_obj = book.iterator(PAGE)
        for i in gen_obj:
            if languages:
                Console.user_output(i)
                Console.user_output("*" * 50)
                Console.user_input("Press any key")
            else:
                Console.user_output(i)
                Console.user_output("*" * 50)
                Console.user_input("Нажміть будь-яку клавішу")
        x = book.lening()
        if languages:
            return f"Total: {x} contacts."
        else:
            return f"Всього: {x} контактів."


@input_error
def search(book: AddressBook, *args):
    pattern = " ".join(args)
    if len(pattern) < 3:
        if languages:
            return "search string length >= 3"
        else:
            return "довжина рядка для пошуку >= 3"
    result = book.search(pattern)
    if not result:
        if languages:
            return "not found"
        else:
            return "не знайдено"
    matches = ""
    for i in result:
        matches += str(i)
    frags = matches.split(pattern)
    highlighted = ""
    for i, fragment in enumerate(frags):
        highlighted += fragment
        if i < len(frags) - 1:
            highlighted += "\033[42m" + pattern + "\033[0m"
    if languages:
        return f"Found {len(result)} matches:\n" + highlighted
    else:
        return f"Знайдено {len(result)} збігів:\n" + highlighted


@input_error
def sort_targ_folder(book: AddressBook, *args):
    target_path = " ".join(args)
    return sort_folder.sort(target_path)


def help(*args):
    if languages:
        with open(os.path.join(dir_path, "README.md"), "rb") as help_file:
            output = help_file.read().decode("utf-8")
            return output
    else:
        with open(os.path.join(dir_path, "README.ua.md"), "rb") as help_file:
            output = help_file.read().decode("utf-8")
            return output


def exit(book: AddressBook, notebook: NotePad, *args):
    global is_ended
    is_ended = True
    save_data(book, notebook)
    if languages:
        return "Good bye"
    else:
        return "До побачення"


def no_command(*args):
    if languages:
        return "There is no such command"
    else:
        return "Такої команди немає"







@input_error
def language(book, *args):
    global languages
    with open(os.path.join(dir_path, "config.JSON"), "r") as cfg:
        cfg_data = json.load(cfg)
    if languages:
        x = input("Choose language: English or Ukrainian?(eng/ukr)>>> ")
    else:
        x = input("Виберіть мову: англійська або українська?(eng/ukr)>>> ")
    if "e" in x or "E" in x:
        with open(os.path.join(dir_path, "config.JSON"), "w") as cfg:
            cfg_data["Language"] = "eng"
            json.dump(cfg_data, cfg)
            return (
                "The language was successfully selected. To apply please restart the bot"
                if languages
                else "Мова виводу на екран була успішно вибрана. Зміниться після перезапуску боту"
            )
    else:
        with open(os.path.join(dir_path, "config.JSON"), "w") as cfg:
            cfg_data["Language"] = "ukr"
            json.dump(cfg_data, cfg)
            return (
                "The language was successfully selected. To apply please restart the bot"
                if languages
                else "Мова виводу на екран була успішно вибрана. Зміниться після перезапуску боту"
            )


COMMANDS = {
    "hello": greet,
    "add email": add_email,
    "add bday": add_birthday,
    "add address": add_address,
    "add contact": add_contact,
    "add note": add_note,
    "add tag": add_tag,
    "congrat": congrat,
    "change note": change_note,
    "change status": change_note_stat,
    "change address": change_address,
    "change bday": change_birthday,
    "change email": change_email,
    "change phone": change,
    "phone": phone,
    "show contacts": show_all,
    "show notes": show_notes,
    "search note": search_note,
    "search": search,
    "del note": del_note,
    "del address": del_address,
    "del phone": del_phone,
    "del bday": del_birthday,
    "del email": del_email,
    "del contact": del_contact,
    "sort folder": sort_targ_folder,
    "lang": language,
    "close": exit,
    "good bye": exit,
    "exit": exit,
    "help": help,
}


def command_parser(line: str):
    line_prep = " ".join(line.split())
    for k, v in COMMANDS.items():
        if line_prep.lower().startswith(k + " ") or line_prep.lower() == k:
            return v, re.sub(k, "", line_prep, flags=re.IGNORECASE).strip().rsplit(" ")
    return no_command, []


is_ended = False
languages = True  # True=En, False=Ukraine


def main():
    book1 = AddressBook()
    notebook = NotePad()
    load_data(book1, notebook)
    if languages:
        Console.user_output(
            "MemoMind \n",
            f"Available commands: {', '.join(k for k in COMMANDS.keys())}",
        )
    else:
        Console.user_output(
            "MemoMind \n",
            f"Доступні команди: {', '.join(k for k in COMMANDS.keys())}",
        )

    while not is_ended:
        s = Console.user_input(">>>")
        command, args = command_parser(s)
        if languages:
            if command == exit:
                Console.user_output(command(book1, notebook), *args)
            else:
                Console.user_output(
                    command((notebook if command in WITH_NOTES else book1), *args)
                )
        else:
            if command == exit:
                Console.user_output(command(book1, notebook), *args)
            else:
                Console.user_output(
                    command((notebook if command in WITH_NOTES else book1), *args)
                )


if __name__ == "__main__":
    main()
