import tkinter as tk
from tkinter import messagebox

usersbank = []

window = tk.Tk()
window.geometry("600x620")
window.config(bg="lightgreen")
window.title("Банкомат")



class User:
    def __init__(self, name, pin, card_number, balance):
        self.name = name
        self.pin = pin
        self.card_number = card_number
        self.balance = balance


user1 = User("Саня", "1111", "654321", 2000)
user2 = User("Діма", "2222", "123456", 1000)

usersbank.append(user1)
usersbank.append(user2)


def find_user(card_number):
    for user in usersbank:
        if user.card_number == card_number:
            return user
    return None


current_user = None
active_entry = None



title = tk.Label(
    window,
    text="Kudravcev BANK",
    bg="lightgreen",
    fg="black",
    font=("Arial", 18, "bold")
)
title.place(x=190, y=50)


info_window = tk.Frame(
    window,
    bg="white",
    width=350,
    height=180,
    bd=2,
    relief="ridge"
)
info_window.place(x=125, y=120)


info = tk.Label(
    info_window,
    text="Банківський рахунок",
    bg="white",
    font=("Arial", 14, "bold")
)
info.place(x=75, y=20)


card_label = tk.Label(
    window,
    text="Номер картки:",
    bg="white",
    font=("Arial", 11)
)
card_label.place(x=150, y=195)


pin_label = tk.Label(
    window,
    text="PIN-код:",
    bg="white",
    font=("Arial", 11)
)
pin_label.place(x=150, y=235)


card_entry = tk.Entry(
    window,
    font=("Arial", 12),
    width=18
)
card_entry.place(x=260, y=195)


pin_entry = tk.Entry(
    window,
    show="*",
    font=("Arial", 12),
    width=18
)
pin_entry.place(x=260, y=235)


status_label = tk.Label(
    window,
    text="",
    bg="white",
    fg="green",
    font=("Arial", 10)
)
status_label.place(x=180, y=270)



def select_card(event):
    global active_entry
    active_entry = card_entry


def select_pin(event):
    global active_entry
    active_entry = pin_entry


card_entry.bind("<Button-1>", select_card)
pin_entry.bind("<Button-1>", select_pin)



class Button:

    def __init__(self, window):

        button_style = {
            "width": 4,
            "height": 2,
            "font": ("Arial", 12)
        }

        positions = {
            "1": (170, 330),
            "2": (225, 330),
            "3": (280, 330),
            "4": (170, 380),
            "5": (225, 380),
            "6": (280, 380),
            "7": (170, 430),
            "8": (225, 430),
            "9": (280, 430),
            "0": (225, 480)
        }

        for number, position in positions.items():

            button = tk.Button(
                window,
                text=number,
                command=lambda n=number: self.number_click(n),
                **button_style
            )

            button.place(
                x=position[0],
                y=position[1]
            )


        self.buttonLogin = tk.Button(
            window,
            text="Підтвердити",
            command=self.login,
            width=12,
            height=2,
            font=("Arial", 11)
        )
        self.buttonLogin.place(x=370, y=335)


        self.buttonBalance = tk.Button(
            window,
            text="Баланс",
            command=self.show_balance,
            width=12,
            height=2,
            font=("Arial", 11)
        )
        self.buttonBalance.place(x=370, y=390)


        self.buttonClear = tk.Button(
            window,
            text="Очистити",
            command=self.clear,
            width=12,
            height=2,
            font=("Arial", 11)
        )
        self.buttonClear.place(x=370, y=445)


    def number_click(self, number):

        if active_entry:
            active_entry.insert(tk.END, number)


    def login(self):

        global current_user

        card_number = card_entry.get()
        pin = pin_entry.get()

        user = find_user(card_number)

        if user is None:

            status_label.config(
                text="Картку не знайдено",
                fg="red"
            )

            return

        if user.pin != pin:

            status_label.config(
                text="Неправильний PIN-код",
                fg="red"
            )

            return

        current_user = user

        status_label.config(
            text=f"Вітаємо, {user.name}!",
            fg="green"
        )


    def show_balance(self):

        if current_user is None:

            messagebox.showwarning(
                "Увага",
                "Спочатку увійдіть у свій рахунок"
            )

            return

        messagebox.showinfo(
            "Баланс",
            f"Ваш баланс: {current_user.balance} грн"
        )


    def clear(self):

        card_entry.delete(0, tk.END)
        pin_entry.delete(0, tk.END)

        status_label.config(text="")


buttons = Button(window)

window.mainloop()