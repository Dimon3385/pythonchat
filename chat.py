from customtkinter import *
from socket import *
import threading

class Window(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('400x400')
        self.minsize(300, 300)
        
        # Змінна для теми
        self.is_dark = True  # CustomTkinter за замовчуванням темна

        # --- БІЧНЕ МЕНЮ ---
        self.menu = CTkFrame(self)
        self.menu.place(x=0, y=0, relheight=1)
        self.menu.configure(width=0)
        self.menu.pack_propagate(False)

        self.show_menu = False
        self.menu_width = 0

        self.text = CTkLabel(self.menu, text='Ваш нік')
        self.text.pack(pady=30)

        self.pole = CTkEntry(self.menu)
        self.pole.pack()

        self.btn = CTkButton(self, text='🔱', width=40, height=40, command=self.show_hide)
        self.btn.place(x=5, y=5)
        
        # --- КНОПКА ТЕМИ ---
        self.theme_btn = CTkButton(self, text='☀️', width=40, height=40, command=self.toggle_theme)
        self.theme_btn.place(x=50, y=5)


        
        self.theme_btn = CTkButton(self, text='✔️', width=40, height=40, command=self.show_auth)
        self.theme_btn.place(x=100, y=5)


        # --- ЧАТ ---
        self.comm = CTkTextbox(self, state='disable')
        self.comm.place(x=0, y=0)

        # --- ПОЛЕ ВВЕДЕННЯ ---
        self.message_input = CTkEntry(self, placeholder_text="Введіть повідомлення")
        self.message_input.place(x=0, y=0)

        self.send_btn = CTkButton(self, text="➤", width=30,height = 30,  command=self.send_message)
        self.send_btn.place(x=0, y=0)
        self.name = '1nyux'
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(("6.tcp.eu.ngrok.io", 14965))
            self.sock.send(self.name.encode("utf-8"))
            threading.Thread(target=self.receive_message).start()
        except Exception as e:
            self.add_message(f"Не вдалося підключитись до сервера {e}")
        self.adaptive()

    def toggle_theme(self):
        if self.is_dark:
            set_appearance_mode("light")
            self.theme_btn.configure(text='🌙')
        else:
            set_appearance_mode("dark")
            self.theme_btn.configure(text='☀️')
        self.is_dark = not self.is_dark

    def adaptive(self):
        menu_w = self.menu.winfo_width()
        win_w = self.winfo_width()
        win_h = self.winfo_height()

        input_h = 35
        padding = 10

        # Відображення повідомлень
        self.comm.configure(width=win_w - menu_w, height=win_h - input_h - 150)
        self.comm.place(x=menu_w, y=50)

        # Поле введення
        self.message_input.configure(width=win_w - menu_w - 170, height=input_h)
        self.message_input.place(x=menu_w + padding, y=win_h - input_h - 100)

        # Кнопка відправки
        self.send_btn.configure(width=30, height=30)
        self.send_btn.place(x=win_w - 150, y=win_h - input_h - 100)

        self.after(30, self.adaptive)

    # --- МЕНЮ ---
    def show_hide(self):
        if self.show_menu:
            self.show_menu = False
            self.close_menu()
        else:
            self.show_menu = True
            self.open_menu()

    def open_menu(self):
        self.name = self.pole.get()
        if self.menu_width < 200:
            self.menu_width += 20
            self.menu.configure(width=self.menu_width)
            self.after(20, self.open_menu)

    def close_menu(self):
        self.name = self.pole.get()
        if self.menu_width > 0:
            self.menu_width -= 20
            self.menu.configure(width=self.menu_width)
            self.after(20, self.close_menu)
        #---auth---#
    def show_auth(self):
        if self.show_menu:
            self.show_menu = False
            self.close_auth()
        else:
            self.show_menu = True
            self.open_auth()

    def open_auth(self):
        if self.menu_width < 200:
            self.menu_width += 20
            self.menu.configure(width=self.menu_width)
            
            # Змінюємо вміст меню на форму авторизації
            if self.menu_width == 20:  # Тільки при першому відкритті
                # Очищаємо меню
                for widget in self.menu.winfo_children():
                    widget.destroy()
                
                # Додаємо елементи авторизації
                CTkLabel(self.menu, text="🔐 АВТОРИЗАЦІЯ", font=("Arial", 16, "bold")).pack(pady=40)
                
                CTkLabel(self.menu, text="Нікнейм:").pack(pady=5)
                self.auth_nick = CTkEntry(self.menu, placeholder_text="Введіть нікнейм")
                self.auth_nick.pack(pady=5, padx=10, fill="x")
                
                CTkLabel(self.menu, text="Пароль:").pack(pady=5)
                self.auth_pass = CTkEntry(self.menu, placeholder_text="Введіть пароль", show="*")
                self.auth_pass.pack(pady=5, padx=10, fill="x")
                
                CTkButton(self.menu, text="✅ Увійти", command=self.do_login, 
                         fg_color="green", hover_color="darkgreen").pack(pady=20, padx=10, fill="x")
                
                self.auth_status = CTkLabel(self.menu, text="")
                self.auth_status.pack(pady=5)
            
            self.after(20, self.open_auth)

    def close_auth(self):
        if self.menu_width > 0:
            self.menu_width -= 20
            self.menu.configure(width=self.menu_width)
            
            if self.menu_width == 0:  # Коли меню повністю закрите
                # Повертаємо оригінальний вміст
                for widget in self.menu.winfo_children():
                    widget.destroy()
                
                self.text = CTkLabel(self.menu, text='Ваш нік')
                self.text.pack(pady=30)
                self.pole = CTkEntry(self.menu)
                self.pole.pack()
            
            self.after(20, self.close_auth)

    def do_login(self):
        """Функція входу"""
        nickname = self.auth_nick.get().strip()
        password = self.auth_pass.get().strip()
        
        if not nickname or not password:
            self.auth_status.configure(text="❌ Заповніть всі поля!", text_color="red")
            return
        
        # Тут можна додати перевірку з сервером
        self.name = nickname
        self.is_authorized = True
        
        self.auth_status.configure(text=f"✅ Авторизовано як {nickname}", text_color="green")
        self.add_message(f"✅ Авторизовано як {self.name}")
        self.connect_to_server()
        
        # Закриваємо меню через 1 секунду
        self.after(1000, self.close_auth)



    def add_message(self, text):
        self.comm.configure(state='normal')
        self.comm.insert(END, text + '\n')
        self.comm.configure(state='disable')
        
    def send_message(self):
        message = self.message_input.get()
        if message:
            self.add_message(f"{self.name}: {message}")
            data = f"TEXT@{self.name}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
        self.message_input.delete(0, END)
        
    def receive_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()
    
    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]

        if msg_type == "TEXT":
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                self.add_message(f"{author}: {message}")
        elif msg_type == "IMAGE":
            if len(parts) >= 4:
                author = parts[1]
                filename = parts[2]
                self.add_message(f"{author} надіслав(ла) зображення: {filename}")
        else:
            self.add_message(line)

win = Window()
win.mainloop()
