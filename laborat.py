import tkinter as tk
usersbank = []

window = tk.Tk()
window.geometry("550x615")
window.config(bg="lightgreen")
window.title("Bankomat")

text = tk.Label(
    window,
    text="Kudravcev BANK",
    bg="lightgreen",
    fg="black",
    font=("Arial", 14)
)
text.place(x=192, y=70)

info_window = tk.Frame(
    window,
    bg="white",
    width=300,
    height=150
)
info_window.place(x=125, y=155)

info = tk.Label(
    info_window,
    text="Банковский счет",
    bg="white",
    font=("Arial", 12)
)
info.place(x=86, y=23)

card_label = tk.Label(
    window,
    text="Card:",
    font=('hard', 12)
)
card_label.place(x=146, y=230)

pin_label = tk.Label(
    window,
    text="PIN:",
    font=('Arial', 12)
)
(pin_label.place(x=155, y=255))


card_entry = tk.Entry(window)
card_entry.place(x=210, y=225)

pin_entry = tk.Entry(window, show="*")
pin_entry.place(x=210, y=255)


class User:
    def __init__(self, name, pin, card_number, balance):
        self.name = name
        self.pin = pin
        self.card_number = card_number
        self.balance = balance

user1 = User('Sanya', "1111", "654321", "2000")
user2 = User('Dima', "2222", "123456", "1000")

usersbank.append(user1)
usersbank.append(user2)


def find_user(card_number):
    for user in usersbank:
        if user.card_number == card_number:
            return user
    return None

active_entry = None

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
        self.buttonBalance = tk.Button(
            window,
            text='Баланс',
            command=self.buttonBalance_click,
            width=5,
            height=2
        )
        self.buttonBalance.place(x=340, y=325)

        self.buttonVhod = tk.Button(
            window,
            text="Подтвердить",
            width=5,
            height=2
        )
        self.buttonVhod.place(x=340, y=370)

        self.button1 = tk.Button(
            window,
            text="1",
            command=self.button1_click,
            width=2,
            height=2
        )
        self.button1.place(x=175, y=325)

        self.button2 = tk.Button(
            window,
            text="2",
            command=self.button2_click,
            width=2,
            height=2
        )
        self.button2.place(x=225, y=325)

        self.button3 = tk.Button(
            window,
            text="3",
            command=self.button3_click,
            width=2,
            height=2
        )
        self.button3.place(x=275, y=325)

        self.button4 = tk.Button(
            window,
            text="4",
            command=self.button4_click,
            width=2,
            height=2
        )
        self.button4.place(x=175, y=368)

        self.button5 = tk.Button(
            window,
            text="5",
            command=self.button5_click,
            width=2,
            height=2
        )
        self.button5.place(x=225, y=368)

        self.button6 = tk.Button(
            window,
            text="6",
            command=self.button6_click,
            width=2,
            height=2
        )
        self.button6.place(x=275, y=368)

        self.button7 = tk.Button(
            window,
            text="7",
            command=self.button7_click,
            width=2,
            height=2
        )
        self.button7.place(x=175, y=410)

        self.button8 = tk.Button(
            window,
            text="8",
            command=self.button8_click,
            width=2,
            height=2
        )
        self.button8.place(x=225, y=410)

        self.button9 = tk.Button(
            window,
            text="9",
            command=self.button9_click,
            width=2,
            height=2
        )
        self.button9.place(x=275, y=410)

        self.button0 = tk.Button(
            window,
            text="0",
            command=self.button0_click,
            width=2,
            height=2
        )
        self.button0.place(x=225, y=450)

    def button1_click(self):
        if active_entry:
            active_entry.insert(tk.END, "1")
    def button2_click(self):
        if active_entry:
            active_entry.insert(tk.END, "2")

    def button3_click(self):
        if active_entry:
            active_entry.insert(tk.END, "3")

    def button4_click(self):
        if active_entry:
            active_entry.insert(tk.END, "4")

    def button5_click(self):
        if active_entry:
            active_entry.insert(tk.END, "5")

    def button6_click(self):
        if active_entry:
            active_entry.insert(tk.END, "6")

    def button7_click(self):
        if active_entry:
            active_entry.insert(tk.END, "7")

    def button8_click(self):
        if active_entry:
            active_entry.insert(tk.END, "8")

    def button9_click(self):
        if active_entry:
            active_entry.insert(tk.END, "9")

    def button0_click(self):
        if active_entry:
            active_entry.insert(tk.END, "0")

    def buttonBalance_click(self):
            print('Была нажата кнопка BALANCE')

    def buttonVhod_click(self):
        print('f')

buttons = Button(window)

window.mainloop()