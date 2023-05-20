from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime
from itertools import islice
import re
import os
import json


dir_path = os.path.dirname(__file__)

with open(os.path.join(dir_path, "config.JSON")) as cfg:
    cfg_data = json.load(cfg)
    languages = True if cfg_data["Language"] == "eng" else False


class UserIO(ABC):
    
    @abstractmethod
    def user_output(self):
        pass
    
    @abstractmethod
    def user_input(self):
        pass

class Console(UserIO):

    def user_output(*output):
        print(*output)
        
    def user_input(*input_):
        return input(*input_)


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Note:
    def __init__(self, text, tag=None, done=False):
        self.day = datetime.today()
        self.done = done
        self.done_date = None
        self.text = text
        self.tag_list = [tag] if tag else []

    def add_tag(self, tag):
        if tag not in self.tag_list:
            self.tag_list.append(tag)
            self.tag_list.sort()

    def __repr__(self) -> str:
        return str(self.text)

    def __eq__(self, other):
        return self.text == other.text
    
    def to_dict(self) -> dict:
        data = {"day":datetime.strftime(self.day, "%d.%m.%Y"),
                "done":self.done,
                "done_date":(datetime.strftime(self.done_date, "%d.%m.%Y") if self.done_date else None),
                "text":self.text, 
                "tag_list":[str(tag) for tag in self.tag_list]}
        return data
    
    def from_dict(self, data):
        self.day = datetime.strptime(data["day"], "%d.%m.%Y")
        self.done = data["done"]
        if data["done_date"]:
            self.done_date = datetime.strptime(data["done_date"], "%d.%m.%Y"),
        self.text = data["text"]
        self.tag_list = [HashTag(tag) for tag in data["tag_list"]]

class HashTag:
    def __init__(self, tag) -> None:
        if "#" in tag:
            self.text = tag
        else:
            self.text = "#" + tag

    def __repr__(self) -> str:
        return self.text

    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text


class NotePad:
    def load_from_file(self, note_file):
        try:
            with open(note_file, "r") as db:
                notes = json.load(db)
        except EOFError:
            pass
        for rec in notes["notes"]:
            note = Note("")
            note.from_dict(rec)
            self.note_list.append(note)
                
    def save_to_file(self, note_file):
        data = []
        for note in self.note_list:
            data.append(note.to_dict())
        notebook = {"notes":data}
        with open(note_file, "w") as db:
            json.dump(notebook, db)

    note_list = []

    def add_note(self, note):
        i = 0
        for rec in self.note_list:
            if len(note.tag_list) <= len(rec.tag_list):
                i = self.note_list.index(rec) + 1
        self.note_list.insert(i, note)

    def change_note(self, note, new_note):
        for rec in self.note_list:
            if str(note) == str(rec):
                rec.text = new_note

    def change_status(self, note):
        for rec in self.note_list:
            if note == rec:
                rec.done = True
                rec.done_date = datetime.today().date()

    def delete(self, note):
        self.note_list.remove(note)

    def sorting(self):
        self.note_list.sort(key=lambda note: len(note.tag_list), reverse=True)


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not (value.isnumeric() or len(value) < 2):  # Name validation
            self.__value = value
        else:
            if languages:
                raise ValueError(
                    "The name cannot consist only of numbers and the minimum length of the name is 2 characters."
                )
            else:
                raise ValueError(
                    "Ім'я не може складатись тільки з цифр та мінімальна довжина імені 2 символа."
                )


class Birthday(Field):
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, "%d.%m.%Y")  # Date validaiton "."
        except ValueError:
            try:
                self._value = datetime.strptime(
                    value, "%d/%m/%Y"
                )  # Date validaiton "/"
            except ValueError:
                if languages:
                    raise ValueError("use the date format DD.MM.YYYY or DD/MM/YYYY")
                else:
                    raise ValueError(
                        "використовуйте формат дати ДД.ММ.РРРР або ДД/ММ/РРРР"
                    )

    def __str__(self) -> str:
        return datetime.strftime(self._value, "%d.%m.%Y")


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        pattern = (
            # Email validation
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )
        if re.match(pattern, value):
            self.__value = value
        else:
            if languages:
                raise ValueError("Invalid e-mail format")
            else:
                raise ValueError("Невірний формат e-mail")


class Address(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) > 5:
            self.__value = value
        else:
            if languages:
                raise ValueError("Address string must be at least 5 symbols long")
            else:
                raise ValueError("Адреса повинна бцти не меньше 5 символів довжиною")


class Phone(Field):
    min_len = 9
    max_len = 13

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, number):
        number = re.sub("\D+", "", number)
        if len(number) == 12:
            number = "+" + number
        elif len(number) == 10:
            number = "+38" + number
        elif len(number) == 9:
            number = "+380" + number
        else:
            if languages:
                raise ValueError(
                    f"\nYou entered the wrong phone number format.\n Try again!\n Minimum number of characters: {Phone.min_len}.\n Maximum: {Phone.max_len}."
                )
            else:
                raise ValueError(
                    f"\nВи ввели невірний формат номера.\n Спробуйте знову!\n Мінімальна к-сть символів:{Phone.min_len}.\n Максимальна:{Phone.max_len}."
                )

        self.__value = number


class Record:
    def __init__(
        self,
        name: Name,
        phone: Phone = None,
        email: Email = None,
        address: Address = None,
        birthday: Birthday = None,
    ):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
        self.email = email
        self.address = address

    def __str__(self):
        if languages:
            line = "{}: Phones: {}; E-mail: {}; Date of birth: {}; Address: {} \n"
        else:
            line = "{}: Телефони: {}; E-mail: {}; Дата народження: {}; Адреса: {} \n"
        address = self.address if self.address else "-"
        email = self.email if self.email else "-"
        birthday = self.birthday if self.birthday else "-"
        return line.format(
            self.name,
            ", ".join([str(phone) for phone in self.phones]),
            email,
            birthday,
            address,
        )

    def __repr__(self):
        if languages:
            line = "{}: Phones: {}; E-mail: {}; Date of birth: {}; Address: {} \n"
        else:
            line = "{}: Телефони: {}; E-mail: {}; Дата народження: {}; Адреса: {} \n"
        email = self.email if self.email else "-"
        address = self.address if self.address else "-"
        birthday = self.birthday if self.birthday else "-"
        return line.format(
            self.name,
            ", ".join([str(phone) for phone in self.phones]),
            email,
            birthday,
            address,
        )

    def days_to_birthday(self) -> int:
        if not self.birthday:
            return 1000000
        today = datetime.today()
        compare = self.birthday.value.replace(year=today.year)
        days = int((compare - today).days)
        if days >= 0:
            return days
        else:
            days = int((compare.replace(year=today.year + 1) - today).days)
            return days

    def add_email(self, email: Email):
        if not self.email:
            self.email = email
        else:
            if languages:
                raise IndexError("E-mail is already entered")
            else:
                raise IndexError("E-mail вже введений")

    def add_phone(self, phone: Phone):
        if phone in self.phones:
            if languages:
                raise IndexError("This phone number already exists")
            else:
                raise IndexError("Цей номер телефону вже існує")
        self.phones.append(phone)

    def add_address(self, adres: Address):
        if not self.address:
            self.address = adres
        else:
            if languages:
                raise IndexError("Address is already entered")
            else:
                raise IndexError("Адреса вже введена")

    def add_birthday(self, birthday: Birthday):
        if not self.birthday:
            self.birthday = birthday
        else:
            if languages:
                raise IndexError("Birthday is already entered")
            else:
                raise IndexError("День народження вже введений")

    def show_phones(self):
        if not self.phones:
            if languages:
                return "This contact has no phone numbers"
            else:
                return "В цього контакта немає номерів телефону"
        elif len(self.phones) == 1:
            if languages:
                return f"Current phone number {self.phones[0]}"
            else:
                return f"Поточний номер телефону {self.phones[0]}"
        else:
            if languages:
                output = "This contact has several phone numbers:\n"
            else:
                output = "В цього контакта декілька номерів телефону:\n"
            for i, phone in enumerate(self.phones, 1):
                output += f"{i}: {phone} "
            return output

    def change_email(self, email: str):
        self.email = Email(email)

    def show_email(self):
        if not self.email:
            if languages:
                return "This contact has no e-mail"
            else:
                return "В цього контакта немає e-mail"
        else:
            if languages:
                return f"Current e-mail {self.email}"
            else:
                return f"Поточний e-mail {self.email}"

    def change_birthday(self, new_birthday: Birthday):
        if not self.birthday:
            if languages:
                raise IndexError("The date of birth is not entered yet")
            else:
                raise IndexError("Дата народження ще не введена")
        self.birthday = new_birthday

    def change_address(self, new_address: Address):
        if not self.address:
            self.address = new_address
            if languages:
                return f"Added {new_address}"
            else:
                return f"Додано адресу {new_address}"
        else:
            old_address = self.address
            self.address = new_address
            if languages:
                return f"Address is changed from {old_address} to {new_address}"
            else:
                return f"Змінено адресу з {old_address} на {new_address}"

    def del_phone(self, num=1):
        if not self.phones:
            if languages:
                raise IndexError("This contact has no phone numbers saved")
            else:
                raise IndexError("В цього контакта немає збережених номерів телефону")
        else:
            return self.phones.pop(num - 1)

    def edit_phone(self, phone_new: Phone, num=1):
        if not self.phones:
            if languages:
                raise IndexError("This contact has no phone numbers saved")
            else:
                raise IndexError("В цього контакта немає збережених номерів телефону")
        else:
            self.phones.pop(num - 1)
            self.phones.insert(num - 1, phone_new)


class AddressBook(UserDict):
    def load_from_file(self, filename) -> None:
        try:
            with open(filename, "r") as db:
                data = json.load(db)
        except EOFError:
            pass
        for rec in data:
            name = Name(data[rec]['name'])
            email = None if not data[rec]['email'] else Email(data[rec]['email'])
            address = None if not data[rec]['address'] else Address(data[rec]['address'])
            birthday = None if not data[rec]['birthday'] else Birthday(data[rec]['birthday'])
            record  = Record(name, email, address, birthday)
            for phone in data[rec]['phones']:
                record.add_phone(phone)
            self.data.update({record.name.value: record})  
            
            
    def save_to_file(self, filename) -> None:
        data = {}
        for rec in self.data.values():
            phones = [str(phone) for phone in rec.phones]
            email = rec.email.value if rec.email is not None else None 
            address = rec.address.value if rec.address is not None else None
            birthday = str(rec.birthday.value) if rec.birthday is not None else None
            data_value = {rec.name.value:{"name":rec.name.value, 
                                          "phones":phones, 
                                          "email":email,
                                          "address":address,
                                          "birthday":birthday}}
            data.update(data_value)
        with open(filename, "w") as db:
            json.dump(data, db)

    def add_record(self, record: Record) -> None:
        self.data.update({record.name.value: record})

    def remove_record(self, contact: str) -> None:
        return self.data.pop(contact)

    def lening(self) -> int:
        return len(self.data)

    def iterator(self, page) -> str:
        start = 0
        while True:
            output = ""
            for i in islice(self.data.values(), start, start + page):
                output += str(i)
            if not output:
                break
            yield output
            start += page

    def show_all(self) -> str:
        output = ""
        for contact in self.data.values():
            output += str(contact)
        if languages:
            output += f"Total: {len(self.data)} contacts."
        else:
            output += f"Всього: {len(self.data)} контактів."
        return output

    def search(self, pattern: str) -> list:
        found_recs = []
        for contact in self.data.values():
            if pattern in str(contact):
                found_recs.append(contact)
        return found_recs
