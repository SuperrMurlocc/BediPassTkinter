#!/usr/bin/env python3

import getpass
import os
import sqlite3
import tkinter as tk
import webbrowser
from mylibrary import *

CHAR_1 = "QWERTYUIOPASDFHJKLZXCVBNM"
CHAR_2 = "qwertyuiopasdfhjklzxcvbnm"
CHAR_3 = "1234567890"
CHAR_4 = "!@#$%^&*"
CHAR_MUST = "BediPass!"
PASS_LENGTH = 20
char1 = 1
char2 = 1
char3 = 1
char4 = 1
AdminLoginAndPass = ["jAkUbBeDnArSkI081001", "BEDI_PASS_AdMiN0405241201"]
global user_key
MACUser = getpass.getuser()


def create_directories() -> None:
    if os.path.exists(f'/Users/{MACUser}/BediGames/BediPass') == 0:
        os.mkdir(f'/Users/{MACUser}/BediGames/BediPass')


def create(conn) -> None:
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS PASSWORDS(
        WEBSITE TEXT NOT NULL,
        PASS TEXT NOT NULL
        );
        '''
    )
    global CHAR_MUST, char1, char2, char3, char4, PASS_LENGTH
    try:
        row = conn.execute("SELECT CHOICE FROM OPTIONS")
        row = row.fetchall()
        CHAR_MUST = str(row[0][0])
        char1 = int(row[1][0])
        char2 = int(row[2][0])
        char3 = int(row[3][0])
        char4 = int(row[4][0])
        PASS_LENGTH = int(row[5][0])
    except sqlite3.OperationalError or IndexError:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS OPTIONS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            OPTION TEXT NOT NULL,
            CHOICE TEXT NOT NULL
            );
            '''
        )
        conn.execute(f'INSERT INTO OPTIONS VALUES (1, \'charmust\', \'{CHAR_MUST}\')')
        conn.execute(f'INSERT INTO OPTIONS VALUES (2, \'char1\', {char1})')
        conn.execute(f'INSERT INTO OPTIONS VALUES (3, \'char2\', {char2})')
        conn.execute(f'INSERT INTO OPTIONS VALUES (4, \'char3\', {char3})')
        conn.execute(f'INSERT INTO OPTIONS VALUES (5, \'char4\', {char4})')
        conn.execute(f'INSERT INTO OPTIONS VALUES (6, \'length\', {PASS_LENGTH})')
        conn.commit()


def create_password(op1: int = 1, op2: int = 1, op3: int = 1, op4: int = 1, length: int = 20) -> str:
    random.seed(int(time.mktime(time.localtime())))
    if len(CHAR_MUST) > length:
        return "not_created(your_word > length)"
    out_pass = ""
    if CHAR_MUST != "":
        out_pass += CHAR_MUST
    container = ""
    if op1:
        container += CHAR_1
    if op2:
        container += CHAR_2
    if op3:
        container += CHAR_3
    if op4:
        container += CHAR_4
    length -= len(out_pass)
    randlist = MyMath.get_rand_list(length, 0, len(container) - 1)
    for i in range(length):
        out_pass += container[randlist[i]]
    return out_pass


def all_children(window) -> list:
    _list = window.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    return _list


class LoginGUI:
    def __init__(self, master):
        for widget in all_children(master):
            widget.pack_forget()

        self.master = master
        self.new_user = 0
        self.username = ""
        master.geometry('360x480')
        master.title("BediPass - Zaloguj")

        self.conn_logins = sqlite3.connect(f'/Users/{MACUser}/BediGames/BediPass/logins.db')
        self.create_logins()

        self.menu = tk.Menu(self.master)
        cascade = tk.Menu(self.menu)
        self.menu.add_cascade(label="Info", menu=cascade)
        cascade.add_command(label='BediPass')
        cascade.add_command(label='Prosty i wygodny pęk kluczy')
        cascade.add_separator()
        cascade.add_command(label='Wykonał: Jakub "Bedi" Bednarski')
        cascade.add_separator()
        cascade.add_command(label='Miłego użytkowania!')
        cascade2 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Zgłoś problem", menu=cascade2)
        cascade2.add_command(label='Napotkałeś problem?')
        cascade2.add_command(label='Coś nie działa?')
        cascade2.add_separator()
        cascade2.add_command(label='Kliknij tutaj i napisz do mnie!',
                             command=lambda: webbrowser.open('https://www.messenger.com/t/100007144363657'))
        cascade03 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Opcje", menu=cascade03)
        cascade03.add_command(label='Powrót do okienka logowania', command=lambda: LoginGUI(self.master))
        self.master.config(menu=self.menu)

        self.label_logininfo = tk.Label(master, text="\n\nProszę zalogować się do systemu BediPass!\n")
        self.label_logininfo.pack()

        self.label_username = tk.Label(master, text="Nazwa użytkownika: ")
        self.label_username.pack()

        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="\nHasło: ")
        self.label_password.pack()

        self.entry_password = tk.Entry(master)
        self.entry_password.pack()

        self.placetaker = tk.Label(master, text="")
        self.placetaker.pack()

        self.login_button = tk.Button(master, text="Zaloguj", command=self.login)
        self.login_button.pack()

        self.label_didlogin_info = tk.Label(master, text="\n\n")
        self.label_didlogin_info.pack()

        self.new_user_info = tk.Label(master, text="\n\n\n\n\n\nNie masz jeszcze konta?\n")
        self.new_user_info.pack()

        self.new_user_button = tk.Button(master, text="Nowy użytkownik", command=self.new_login)
        self.new_user_button.pack()

        self.enter_button = tk.Button(self.master, text="Wejdź", command=lambda: self.enter_user(self.username))

    def __del__(self):
        self.conn_logins.close()
        del self

    def new_login(self):
        if self.new_user == 0:
            self.new_user = 1
            self.label_logininfo.config(text="\nProszę wprowadzić nową nazwę użytkownika oraz\nwybrać hasło!\n")
            self.login_button.config(text="Stwórz konto")
            self.new_user_info.config(text="\n\n\n\n\n\nMasz już konto?\n")
            self.new_user_button.config(text="Mam już konto")
            self.label_didlogin_info.config(text="\n\n")

        elif self.new_user == 1:
            self.new_user = 0
            self.label_logininfo.config(text="\n\nProszę zalogować się do systemu BediPass!\n")
            self.login_button.config(text="Zaloguj")
            self.new_user_info.config(text="\n\n\n\n\n\nNie masz jeszcze konta?\n")
            self.new_user_button.config(text="Nowy użytkownik")

    def login(self):
        if self.new_user == 0:

            if self.entry_username.get() == AdminLoginAndPass[0] and self.entry_password.get() == AdminLoginAndPass[1]:
                self.label_logininfo.config(text="\n\nZalogowano na konto admina...\n\n")
                self.hide()

                cursor = self.conn_logins.execute("SELECT USERNAME, PASS FROM LOGINS")
                usernames = []
                passwords = []
                for row in cursor:
                    usernames.append(MyEncrypt.decode(row[0]))
                    passwords.append(MyEncrypt.decode(row[1]))

                cascade3 = tk.Menu(self.menu, tearoff=0)
                self.menu.add_cascade(label="Użytkownicy", menu=cascade3)

                for user in usernames:
                    cascade3.add_command(label=f'{user}')
                    cascade4 = tk.Menu(cascade3, tearoff=0)
                    cascade3.add_cascade(label="Hasło", menu=cascade4)
                    cascade4.add_command(label=f'{passwords[usernames.index(user)]}')

                    curr_user_key = 0
                    for letter in user:
                        curr_user_key += ord(letter)

                    conn = sqlite3.connect(f'/Users/{MACUser}/BediGames/BediPass/{user}.db')
                    create(conn)

                    cursor = conn.execute("SELECT WEBSITE, PASS FROM PASSWORDS")
                    websites = []
                    webpasswords = []
                    for row in cursor:
                        websites.append(MyEncrypt.decode(row[0], curr_user_key))
                        webpasswords.append(MyEncrypt.decode(row[1], curr_user_key))

                    cascade5 = tk.Menu(cascade3, tearoff=0)
                    cascade3.add_cascade(label="Zapisane strony", menu=cascade5)

                    for website in websites:
                        cascade5.add_command(label=f'{website}')
                        cascade5.add_command(label=f'{webpasswords[websites.index(website)]}')
                        cascade5.add_separator()

                    conn.close()


                    cascade3.add_separator()

            else:
                cursor = self.conn_logins.execute("SELECT USERNAME, PASS FROM LOGINS")
                usernames = []
                passwords = []
                for row in cursor:
                    usernames.append(MyEncrypt.decode(row[0]))
                    passwords.append(MyEncrypt.decode(row[1]))
                given_username = self.entry_username.get()
                given_password = self.entry_password.get()
                if given_username in usernames:
                    if given_password == passwords[usernames.index(given_username)]:
                        self.label_logininfo.config(text=f'\n\nZalogowano na konto {given_username}...')
                        self.hide()
                        self.username = given_username
                        self.enter_button.pack()
                        global user_key
                        user_key = 0
                        for letter in self.username:
                            user_key += ord(letter)
                    else:
                        self.label_didlogin_info.config(text="\nPodano błędne hasło...\n")
                else:
                    self.label_didlogin_info.config(text="\nNie znaleziono takiego użytkownika...\n")
        elif self.new_user == 1:
            cursor = self.conn_logins.execute("SELECT USERNAME, PASS FROM LOGINS")
            usernames = []
            amount = 1
            for row in cursor:
                usernames.append(MyEncrypt.decode(row[0]))
                amount += 1
            given_username = self.entry_username.get()
            given_password = self.entry_password.get()
            if given_username in usernames or given_username == AdminLoginAndPass[0]:
                self.label_didlogin_info.config(text="\nNazwa użytkownika zajęta...\n")
            else:
                if given_password == "":
                    self.label_didlogin_info.config(text="\nHasło nie może być puste...\n")
                else:
                    self.conn_logins.execute(
                        f'INSERT INTO LOGINS VALUES ({amount}, \'{MyEncrypt.encode(given_username)}\', \'{MyEncrypt.encode(given_password)}\')')
                    self.conn_logins.commit()
                    self.label_logininfo.config(text=f'\n\nStworzono i zalogowano na konto {given_username}...')
                    self.hide()
                    self.username = given_username
                    self.enter_button.pack()
                    user_key = 0
                    for letter in self.username:
                        user_key += ord(letter)

    def hide(self):
        self.master.geometry("360x120")
        self.label_username.pack_forget()
        self.label_password.pack_forget()
        self.entry_username.pack_forget()
        self.entry_password.pack_forget()
        self.login_button.pack_forget()
        self.new_user_button.pack_forget()
        self.new_user_info.pack_forget()
        self.label_didlogin_info.pack_forget()

    def create_logins(self):
        self.conn_logins.execute(
            '''
            CREATE TABLE IF NOT EXISTS LOGINS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            USERNAME TEXT NOT NULL,
            PASS TEXT NOT NULL
            );
            '''
        )

    def enter_user(self, user):
        self.enter_button.pack_forget()
        self.label_logininfo.pack_forget()
        DidLoginGUI(root, user)


class DidLoginGUI:
    def __init__(self, master, user):
        self.master = master
        master.geometry('360x480')
        master.title("BediPass - Zalogowano")

        self.user = user

        self.conn = sqlite3.connect(f'/Users/{MACUser}/BediGames/BediPass/{self.user}.db')
        create(self.conn)

        self.label_maininfo = tk.Label(master, text=f'Witaj {self.user}!\nDziękujemy, że korzystasz z BediPass!\n\n')
        self.label_maininfo.pack()

        self.label_getpass = tk.Label(master, text="\nPobierz zapisane hasło")
        self.label_getpass.pack()

        self.getpass_button = tk.Button(master, text="Pobierz", command=lambda: GetPassGUI(user))
        self.getpass_button.pack()

        self.label_savepass = tk.Label(master, text="\nZapisz nowe hasło")
        self.label_savepass.pack()

        self.savepass_button = tk.Button(master, text="Zapisz", command=lambda: SavePassGUI(user))
        self.savepass_button.pack()

        self.label_weblist = tk.Label(master, text="\nZobacz zapisane witryny")
        self.label_weblist.pack()

        self.weblist_button = tk.Button(master, text="Lista", command=lambda: WebListGUI(user))
        self.weblist_button.pack()

        self.label_delpass = tk.Label(master, text="\nUsuń hasło z listy")
        self.label_delpass.pack()

        self.delpass_button = tk.Button(master, text="Usuń", command=lambda: DelPassGUI(user))
        self.delpass_button.pack()

        self.label_managepass = tk.Label(master, text="\nZarządzaj ustawieniami generatora haseł")
        self.label_managepass.pack()

        self.managepass_button = tk.Button(master, text="Ustawienia", command=lambda: ManagePassGUI(user))
        self.managepass_button.pack()

    def __del__(self):
        self.conn.close()
        del self


class GetPassGUI:
    def __init__(self, user):
        self.get_pass_window = tk.Toplevel()
        self.get_pass_window.title("Pobierz hasło")
        self.get_pass_window.geometry("360x240")

        self.user = user

        self.conn = sqlite3.connect(f'/Users/{MACUser}/BediGames/BediPass/{self.user}.db')

        self.description_label = tk.Label(self.get_pass_window,
                                          text="\nWpisz witrynę dla której hasło\nchcesz pobrać:\n")
        self.description_label.pack()

        self.return_info_label = tk.Label(self.get_pass_window, text="")

        self.get_pass_entry = tk.Entry(self.get_pass_window)
        self.get_pass_entry.pack()

        self.get_pass_button = tk.Button(self.get_pass_window, text="Pobierz", command=lambda: self.GetPassAction())
        self.get_pass_button.pack()

    def __del__(self):
        self.conn.close()
        del self

    def GetPassAction(self):
        self.return_info_label.pack_forget()

        cursor = self.conn.execute("SELECT WEBSITE, PASS FROM PASSWORDS")
        websites = []
        passwords = []
        for row in cursor:
            websites.append(MyEncrypt.decode(row[0], user_key))
            passwords.append(MyEncrypt.decode(row[1], user_key))

        if self.get_pass_entry.get() not in websites:
            self.return_info_label.config(text="\nNie ma takiej witryny\nw bazie haseł...")
        else:
            self.return_info_label.config(
                text=f'\nZnaleziono i skopiowano do schowka\nhasło do witryny: {self.get_pass_entry.get()}')
            my_copy(passwords[websites.index(self.get_pass_entry.get())])

        self.get_pass_entry.delete(0, 'end')

        self.return_info_label.pack()


class SavePassGUI:
    def __init__(self, user):
        self.save_pass_window = tk.Toplevel()
        self.save_pass_window.title("Zapisz hasło")
        self.save_pass_window.geometry("360x240")

        self.user = user

        self.conn = sqlite3.connect(f'/Users/{MACUser}/BediGames/BediPass/{self.user}.db')

        self.description_label = tk.Label(self.save_pass_window,
                                          text="\nWpisz witrynę dla której hasło\nchcesz wygenerować i zapisać:\n")
        self.description_label.pack()

        self.return_info_label = tk.Label(self.save_pass_window, text="")

        self.save_pass_entry = tk.Entry(self.save_pass_window)
        self.save_pass_entry.pack()

        self.save_pass_button = tk.Button(self.save_pass_window, text="Zapisz", command=lambda: self.SavePassAction())
        self.save_pass_button.pack()

    def __del__(self):
        self.conn.close()
        del self

    def SavePassAction(self):
        self.return_info_label.pack_forget()

        cursor = self.conn.execute("SELECT WEBSITE, PASS FROM PASSWORDS")
        websites = []
        for row in cursor:
            websites.append(MyEncrypt.decode(row[0], user_key))

        if self.save_pass_entry.get() in websites:
            self.return_info_label.config(text="\nTaka witryna znajduje się już\nw bazie haseł...")
        else:
            new_pass = create_password(char1, char2, char3, char4, PASS_LENGTH)
            self.return_info_label.config(
                text=f'\nWygenerowano, zapisano i skopiowano do schowka\nhasło do witryny: {self.save_pass_entry.get()}')
            my_copy(new_pass)
            self.conn.execute(
                f'INSERT INTO PASSWORDS VALUES (\'{MyEncrypt.encode(self.save_pass_entry.get(), user_key)}\', \'{MyEncrypt.encode(new_pass, user_key)}\')')
            self.conn.commit()

        self.save_pass_entry.delete(0, 'end')

        self.return_info_label.pack()


class WebListGUI:
    def __init__(self, user):
        self.web_list_window = tk.Toplevel()
        self.web_list_window.title("Lista witryn")
        self.web_list_window.geometry("360x360")

        self.user = user

        self.conn = sqlite3.connect(f'/Users/{MACUser}/BediGames/BediPass/{self.user}.db')

        self.description_label1 = tk.Label(self.web_list_window,
                                           text="\nLista twoich zapisanych witryn: \n(aby zobaczyć hasło użyj metody \"Pobierz\"\nlub dwukrotnie kliknij w witrynę)\n")
        self.description_label1.pack()

        self.return_info_label = tk.Label(self.web_list_window, text="")

        self.description_label2 = tk.Label(self.web_list_window, text="Wyszukaj:")
        self.description_label2.pack()

        self.starts_with = tk.StringVar()
        self.starts_with.trace("w", lambda name, index, mode, sv=self.starts_with: self.MakeWebList())
        self.web_list_starts_with_entry = tk.Entry(self.web_list_window, textvariable=self.starts_with)
        self.web_list_starts_with_entry.pack()

        self.web_list = tk.Listbox(self.web_list_window, height=8)
        self.web_list.bind("<Double-Button-1>", self.WebListAction)
        self.web_list.pack()

        self.MakeWebList()

        self.refresh_list_button = tk.Button(self.web_list_window, text="Odśwież", command=lambda: self.MakeWebList())
        self.refresh_list_button.pack()

    def __del__(self):
        self.conn.close()
        del self

    def MakeWebList(self):
        self.web_list.delete(0, tk.END)

        cursor = self.conn.execute("SELECT WEBSITE, PASS FROM PASSWORDS")
        websites = []
        for row in cursor:
            websites.append(MyEncrypt.decode(row[0], user_key))

        for website in websites:
            if website.startswith(self.starts_with.get()):
                self.web_list.insert(websites.index(website), website)

    def WebListAction(self, event):
        self.return_info_label.pack_forget()

        cursor = self.conn.execute("SELECT WEBSITE, PASS FROM PASSWORDS")
        websites = []
        passwords = []
        for row in cursor:
            websites.append(MyEncrypt.decode(row[0], user_key))
            passwords.append(MyEncrypt.decode(row[1], user_key))

        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        my_copy(passwords[websites.index(value)])

        self.return_info_label.config(text=f'\nZnaleziono i skopiowano do schowka\nhasło do witryny: {value}')
        self.return_info_label.pack()


class DelPassGUI:
    def __init__(self, user):
        self.del_pass_window = tk.Toplevel()
        self.del_pass_window.title("Usuń hasło")
        self.del_pass_window.geometry("360x240")

        self.user = user

        self.conn = sqlite3.connect(f'/Users/{MACUser}/BediGames/BediPass/{self.user}.db')

        self.description_label = tk.Label(self.del_pass_window,
                                          text="\n[AKCJA NIEODWRACALNA]\nWpisz witrynę dla której hasło\nchcesz usunąć:\n")
        self.description_label.pack()

        self.return_info_label = tk.Label(self.del_pass_window, text="")

        self.del_pass_entry = tk.Entry(self.del_pass_window)
        self.del_pass_entry.pack()

        self.del_pass_button = tk.Button(self.del_pass_window, text="Usuń", command=lambda: self.DelPassAction())
        self.del_pass_button.pack()

    def __del__(self):
        self.conn.close()
        del self

    def DelPassAction(self):
        self.return_info_label.pack_forget()

        cursor = self.conn.execute("SELECT WEBSITE, PASS FROM PASSWORDS")
        websites = []
        for row in cursor:
            websites.append(MyEncrypt.decode(row[0], user_key))

        if self.del_pass_entry.get() not in websites:
            self.return_info_label.config(text="\nNie ma takiej witryny\nw bazie haseł...")
        else:
            self.return_info_label.config(text=f'\nUsunięto hasło do witryny: {self.del_pass_entry.get()}')
            self.conn.execute(
                f'DELETE FROM PASSWORDS WHERE WEBSITE = \'{MyEncrypt.encode(self.del_pass_entry.get(), user_key)}\'')
            self.conn.commit()

        self.del_pass_entry.delete(0, 'end')
        self.return_info_label.pack()


class ManagePassGUI:
    def __init__(self, user):
        self.manage_pass_window = tk.Toplevel()
        self.manage_pass_window.title("Ustawienia")
        self.manage_pass_window.geometry("360x360")

        self.user = user

        self.conn = sqlite3.connect(f'/Users/{MACUser}/BediGames/BediPass/{self.user}.db')

        self.placetaker = tk.Label(self.manage_pass_window, text="\n")

        self.description_label1 = tk.Label(self.manage_pass_window, text="\nOd czego ma zaczynać się twoje hasło:")
        self.description_label1.pack()

        self.manage_pass_entry1 = tk.Entry(self.manage_pass_window)
        self.manage_pass_entry1.pack()
        self.manage_pass_entry1.insert(tk.END, CHAR_MUST)

        self.description_label2 = tk.Label(self.manage_pass_window, text="\nJaka ma być długość wygenerowanego hasła:")
        self.description_label2.pack()

        self.manage_pass_entry2 = tk.Entry(self.manage_pass_window)
        self.manage_pass_entry2.pack()
        self.manage_pass_entry2.insert(tk.END, str(PASS_LENGTH))

        self.placetaker.pack()

        self.var1 = tk.IntVar(value=char1)
        self.var2 = tk.IntVar(value=char2)
        self.var3 = tk.IntVar(value=char3)
        self.var4 = tk.IntVar(value=char4)

        self.checkbox1 = tk.Checkbutton(self.manage_pass_window, text="Hasło może zawierać duże litery.",
                                        variable=self.var1, onvalue=1, offvalue=0)
        self.checkbox1.pack(anchor=tk.W)
        self.checkbox2 = tk.Checkbutton(self.manage_pass_window, text="Hasło może zawierać małe litery.",
                                        variable=self.var2, onvalue=1, offvalue=0)
        self.checkbox2.pack(anchor=tk.W)
        self.checkbox3 = tk.Checkbutton(self.manage_pass_window, text="Hasło może zawierać cyfry.", variable=self.var3,
                                        onvalue=1, offvalue=0)
        self.checkbox3.pack(anchor=tk.W)
        self.checkbox4 = tk.Checkbutton(self.manage_pass_window, text="Hasło może zawierać znaki specjalne. ",
                                        variable=self.var4, onvalue=1, offvalue=0)
        self.checkbox4.pack(anchor=tk.W)

        self.placetaker.pack()

        self.return_info_label = tk.Label(self.manage_pass_window, text="")

        self.manage_pass_button = tk.Button(self.manage_pass_window, text="Zapisz",
                                            command=lambda: self.ManagePassAction())
        self.manage_pass_button.pack()

    def __del__(self):
        self.conn.close()
        del self

    def ManagePassAction(self):
        self.return_info_label.pack_forget()
        try:
            length = int(self.manage_pass_entry2.get())
            if length >= len(self.manage_pass_entry1.get()):

                global CHAR_MUST, char1, char2, char3, char4, PASS_LENGTH
                CHAR_MUST = self.manage_pass_entry1.get()
                PASS_LENGTH = length
                char1 = self.var1.get()
                char2 = self.var2.get()
                char3 = self.var3.get()
                char4 = self.var4.get()
                self.conn.execute(f'UPDATE OPTIONS SET CHOICE = \'{CHAR_MUST}\' WHERE OPTION = \'charmust\'')
                self.conn.execute(f'UPDATE OPTIONS SET CHOICE = {char1} WHERE OPTION = \'char1\'')
                self.conn.execute(f'UPDATE OPTIONS SET CHOICE = {char2} WHERE OPTION = \'char2\'')
                self.conn.execute(f'UPDATE OPTIONS SET CHOICE = {char3} WHERE OPTION = \'char3\'')
                self.conn.execute(f'UPDATE OPTIONS SET CHOICE = {char4} WHERE OPTION = \'char4\'')
                self.conn.execute(f'UPDATE OPTIONS SET CHOICE = {PASS_LENGTH} WHERE OPTION = \'length\'')
                self.conn.commit()
                self.conn.close()

                self.return_info_label.config(text="\nPomyślnie zapisano ustawienia.")
            else:
                self.return_info_label.config(text="\nWpisana długość jest za krótka...")
        except ValueError:
            self.return_info_label.config(text="\nWpisz długość jako liczbę całkowitą...")
        self.return_info_label.pack()


create_directories()
root = tk.Tk()
root.resizable(0, 0)
login_gui = LoginGUI(root)
root.mainloop()
