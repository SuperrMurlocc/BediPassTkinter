
# PRZEGLAD DANYHC UZYTKOWNIKA
"""

    def admin_options_GUI(self, user):
        widget_list = all_children(self.master)
        for widget in widget_list:
            widget.pack_forget()

        self.label_logininfo.pack_forget()
        self.master.geometry("360x260")

        global user_key
        user_key = 0

        for letter in user:
            user_key += ord(letter)

        cursor = self.conn_logins.execute("SELECT USERNAME, PASS FROM LOGINS")
        users = []
        user_pass = []
        for row in cursor:
            users.append(MyEncrypt.decode(row[0]))
            user_pass.append(MyEncrypt.decode(row[1]))

        change_pass_label1 = tk.Label(self.master,
                                      text=f'\nUżytkownik: {user}\tHasło: {user_pass[users.index(user)]}\n\n')
        change_pass_label1.pack()

        conn = sqlite3.connect(f'/Users/{MACUser}/BediPass/{user}.db')
        create(conn)

        cursor = conn.execute("SELECT WEBSITE, PASS FROM PASSWORDS")
        websites = []
        passwords = []
        for row in cursor:
            websites.append(MyEncrypt.decode(row[0], user_key))
            passwords.append(MyEncrypt.decode(row[1], user_key))

        conn.close()

        web_list = tk.Listbox(self.master, height=8, width=32)
        for website in websites:
            web_list.insert(websites.index(website), f'{website} : {passwords[websites.index(website)]}')
        web_list.pack()

"""