Bot "MemoMind 1.2.0".
This bot is used to store important information such as a phone book, as well as a list of notes/tasks with hashtags and some other useful functions. Basic commands (all commands are case-insensitive):

- HELLO: welcomes the user
- LANG: selects the output language of the application. Language applies after restart. Frmat: lang  
- ADD CONTACT: adds a contact and its data to the phone book. Format: add contact name (mandatory parameter) phone e-mail address (optional parameters). User names cannot consist of only numbers and be shorter than 2 characters. If the contatct already exists new data is added.
- ADD NOTE: adds a note (with the current date and status "not completed") to the list of notes. Format: add note text with spaces between words
- ADD TAG: adds a tag to the note. Format: add tag first_letters_of_note... #tag
- ADD ADDRESS: adds the contact's address. Format: add address name address
- ADD EMAIL: adds the contact's e-mail address. Format: add email name e-mail
- ADD BDAY: adds the contact's date of birth. Format: add bday name date

- CHANGE PHONE: changes the contact's phone number(s). Format: change phone name phone (optional parameter). If the contact does not have a phone number, it will be added immediately. If the contact has 1 number, it will be replaced by a new one. If the contact has more than one phone number in the record, you need to select which one you'd like to change
- CHANGE EMAIL: changes the contact's e-mail address. Format: change email name (mandatory parameter) e-mail
- CHANGE BDAY: changes the contact's date of birth. Format: change bday name date
- CHANGE ADDRESS: changes the contact's address. Format: change address name address
- CHANGE NOTE: changes the content of the note. Format: change note (first_letters_of_note... or #tag) new_content
- CHANGE STATUS: changes the status of the note to "done" and saves the date of change. Format: change status (first_letters_of_note... or #tag)

- PHONE: displays the contact's phone(s) on the screen. Format: phone name
- DEL PHONE: deletes the contact's phone number. Format: del phone name phone (optional parameter). If a certain phone number was entered, it will be deleted, if not, then you need to select which number to delete
- DEL CONTACT: deletes the contact from the phone book. Format: del contact name
- DEL ADDRESS: deletes the contact's address. Format: del address name
- DEL NOTE: deletes the note. Format: del note (first_letters_of_note... or #tag)
- DEL EMAIL: deletes the contact's e-mail. Format: del email name
- DEL BDAY: deletes the contact's date of birth. Format: del bday name

- CONGRAT: displays a list of contacts who will have a birthday during the specified period. Format: congrat number_of_days
- SHOW CONTACTS: displays the phonebook. Format: show contacts
- SHOW NOTES: displays all notes, dates of creation, execution statuses and execution dates. Format: show notes
- SEARCH: executes the search in the contact book. Finds all matches in numbers, names or e-mails. The search string must contain at least 3 characters. Format: search string
- SEARCH NOTE: matches notes by at least 1 character or by tag. Format: search note (first_letters_of_note... or #tag)
- SORT FOLDER: sorts files by type in the folder at the specified path. Unpacks archives, deletes empty folders. Translates the names of files and folders with translit from Cyrillic. Format: sort folder path_to_folder. File types can be specified in the config.JSON configuration file. It is forbidden to change the name of the "archives" folder!
- CLOSE, GOOD BYE, EXIT: terminates work with the bot and exits to the operating system
- HELP: displays this manual on the screen. The names of the phone book and note book files are also written in the config.JSON file