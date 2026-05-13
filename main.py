import tkinter as tk
from tkinter import messagebox
from tkinter import font as ff
import random
import string

class PasswordManager():

    def __init__(self, root, users={}, current_user=None):
        
        self.root = root
        self.users = users
        self.current_user = current_user
        self.clear_window()

        self.center_frame = tk.Frame(self.root)
        self.center_frame.pack(expand=True) 
        
       
        self.start_login_btn = Button(self.center_frame, text='Войти') 
        self.start_login_btn['command'] = lambda: self.login()
        self.start_login_btn.pack(pady=5, fill='x') 
        
        
        self.start_reg_btn = Button(self.center_frame, text='Регистрация')
        self.start_reg_btn['command'] = lambda: self.registration()
        self.start_reg_btn.pack(pady=5, fill='x') 
        
    def main_page(self, *args, **kwargs):
        self.clear_window()
    
        top_nav = tk.Frame(self.root)
        top_nav.pack(side='top', fill='x', padx=10, pady=5)
        
        self.username_info_lbl = Label(top_nav, text=f'Пользователь: {self.current_user}')
        self.username_info_lbl.pack(side='left')
        
        self.logout_btn = Button(top_nav, text="Выйти")
        self.logout_btn['command'] = lambda: self.__init__(self.root, current_user=None, users=self.users)
        self.logout_btn.pack(side='right')

       
        content = tk.Frame(self.root)
        content.pack(expand=True)

        self.add_acc_btn = Button(content, text="Добавить")
        self.add_acc_btn['command'] = lambda: self.add_site()
        self.add_acc_btn.pack(pady=10, fill='x')

        self.get_acc_btn = Button(content, text="Получить данные")
        self.get_acc_btn['command'] = lambda: self.get_site_name()
        self.get_acc_btn.pack(pady=10, fill='x')
        
        count = len(self.users[self.current_user].keys()) - 1
        self.site_name_lbl = Label(content, text=f"Записей: {count}")
        self.site_name_lbl.pack(pady=5)

    def get_site_name(self):
        self.clear_window()
        self.main_page()
        
        bottom_area = tk.Frame(self.root)
        bottom_area.pack(side='bottom', pady=20)
        
        Label(bottom_area, text="Введите название сайта:").pack()
        self.site_name_entry = Entry(bottom_area)
        self.site_name_entry.pack(pady=5)

        self.enter_btn = Button(bottom_area, text="Ввод")
        self.enter_btn['command'] = self.get_data
        self.enter_btn.pack(pady=5)

    def get_data(self):
        site = self.site_name_entry.get()
        if site in self.users[self.current_user]:
            data = self.users[self.current_user][site]
            Label(self.root, text=f"Имя: {data['username']}").pack()
            Label(self.root, text=f"Пароль: {data['password']}").pack()
        else:
            messagebox.showinfo("Неверные данные", "Сайт не найден")

    def add_site(self):
        self.clear_window()
        self.main_page()
        
        frame = tk.Frame(self.root)
        frame.pack(side='bottom', pady=20, expand=1)
            
        Label(frame, text="Название сайта:").grid(column=1)
        self.site_name_entry = Entry(frame)
        self.site_name_entry.grid(column=1)
    
        Label(frame, text="Имя пользователя:").grid(column=1)
        self.username_entry = Entry(frame)
        self.username_entry.grid(column=1)

        Label(frame, text="Пароль:").grid(column=1)
        self.password_entry = Entry(frame)
        self.password_entry.grid(column=1)
        Button(frame, text="Сгенерировать", command=self.generate_password).grid(column=2, row=5, padx=15)
        

        self.save_btn = Button(frame, text="Сохранить")
        self.save_btn['command'] = lambda: self.save_site()
        self.save_btn.grid(column=1)


    def generate_password(self, *args, **kwargs):
        self.password_entry.delete(0, tk.END)
        data = list(string.digits + string.ascii_letters + '-' + '_' + '@')
        for i in range(15):
            self.password_entry.insert(i, random.choice(data))
        

    def save_site(self):
        try:
            self.users[self.current_user][self.site_name_entry.get()] = {
                'username': self.username_entry.get(), 
                'password': self.password_entry.get()
            }
            self.clear_window()
            self.main_page()
        except Exception as err:
            print(err)
            messagebox.showwarning(title="Ошибка", message="Попробуйте еще раз")

    def try_log(self, *args, **kwargs):
        username = self.username_log_input.get()
        password = self.password_log_input.get()
        try:
            if username in self.users and self.users[username]['password'] == password:
                self.current_user = username
                self.main_page()
            else:
                messagebox.showwarning(title="Ошибка", message="Неверные данные")
        except Exception:
            messagebox.showwarning(title="Ошибка", message="Ошибка входа")

    def login(self, *args, **kwargs):
        self.clear_window()
        container = tk.Frame(self.root)
        container.pack(expand=True)

        Label(container, text="Введите имя:").pack()
        self.username_log_input = Entry(container)
        self.username_log_input.pack(pady=5)

        Label(container, text="Введите пароль:").pack()
        self.password_log_input = Entry(container, show="*")
        self.password_log_input.pack(pady=5)

        btns = tk.Frame(container)
        btns.pack(pady=20)
        
        Button(btns, text="Войти", command=self.try_log).pack(side='left', padx=10)
        Button(btns, text="Назад", command=lambda: self.__init__(self.root, self.users)).pack(side='left', padx=10)

    def clear_window(self, *args, **kwargs):
        for el in self.root.winfo_children():
            el.destroy()
        
    def try_reg(self, *args, **kwargs):
        username = self.username_input.get()
        password = self.password_input.get()
        confirmed_password = self.confirm_password_input.get()

        if confirmed_password != password:
            messagebox.showwarning("Ошибка", "Пароли не совпадают")
            return {}
            
        if username:
            self.users[username] = {'password': password}
            self.__init__(self.root, self.users)
        else:
            messagebox.showwarning("Ошибка", "Ошибка ввода")

    def registration(self, *args, **kwargs):
        self.clear_window()
        container = tk.Frame(self.root)
        container.pack(expand=True)

        Label(container, text="Придумайте имя:").pack()
        self.username_input = Entry(container)
        self.username_input.pack(pady=5)

        Label(container, text="Придумайте пароль:").pack()
        self.password_input = Entry(container, show="*")
        self.password_input.pack(pady=5)

        Label(container, text="Повторите пароль:").pack()
        self.confirm_password_input = Entry(container, show="*")
        self.confirm_password_input.pack(pady=5)

        btns = tk.Frame(container)
        btns.pack(pady=20)

        Button(btns, text="Создать", command=self.try_reg).pack(side='left', padx=10)
        Button(btns, text="Назад", command=lambda: self.__init__(self.root, self.users)).pack(side='left', padx=10)

window = tk.Tk()
window.geometry('1000x800')
window.title('Passwor Manager')
custom_font = ff.Font(family="JetBrainsMono", size=20)

class Label(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, font=custom_font, **kwargs)
        
class Button(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, font=custom_font, **kwargs)
        
class Entry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, font=custom_font, **kwargs)
        
if __name__ == "__main__":
    app = PasswordManager(window)
    window.mainloop()
