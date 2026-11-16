import tkinter as tk
from tkinter import ttk
import logging
from models import DepositTransaction, WithdrawTransaction, TransferTransaction
from bank_system import BankSystem

logger = logging.getLogger("UI")

TRANSLATIONS = {
    "uk": {
        "title": "🏦 KUDRYAVTSEV BANK",
        "welcome": "ВІТАЄМО В БАНКОМАТІ",
        "cabinet": "ОСОБИСТИЙ КАБІНЕТ",
        "admin_panel": "АДМІНІСТРАТИВНА ПАНЕЛЬ",
        "card_num": "Номер картки:",
        "pin": "PIN-код:",
        "recipient": "Отримувач:",
        "name": "ПІБ:",
        "deposit_lbl": "Депозит (грн):",
        "amount_lbl": "Сума:",
        "confirm": "✔ ПІДТВЕРДИТИ",
        "balance_btn": "💳 БАЛАНС",
        "take_btn": "💵 ЗНЯТИ",
        "deposit_btn": "📥 ПОПОВНИТИ",
        "transfer_btn": "💸 ПЕРЕКАЗ",
        "history_btn": "📄 ІСТОРІЯ",
        "cancel_btn": "✖ СКАСУВАТИ",
        "reg_btn": "➕ НОВИЙ КЛІЄНТ",
        "clear_btn": "⌫ ОЧИСТИТИ",
        "finish_btn": "🚪 ЗАВЕРШИТИ РОБОТУ",
        "unblock_btn": "🔓 РОЗБЛОКУВАТИ",
        "lang_btn": "🇺🇦 UA",
        "processing": "⏳ Обробка запиту...",
        "success": "Успішно!",
        "transfer_success": "Переказ успішний!",
        "unblocked": "Картку розблоковано!",
        "empty_history": "Історія транзакцій порожня",
        "history_title": "ОСТАННІ ОПЕРАЦІЇ:\n",
        "enter_amount": "Введіть суму:",
        "enter_target": "Картка отримувача:",
        "enter_unblock": "Картка для розблокування:",
        "session_timeout": "Сеанс завершено через бездіяльність",
        "support_title": "СЛУЖБА ПІДТРИМКИ",
        "support_phone": "0 800 500 000",
        "support_info": "Безкоштовно по Україні"
    },
    "en": {
        "title": "🏦 KUDRYAVTSEV BANK",
        "welcome": "WELCOME TO ATM",
        "cabinet": "PERSONAL ACCOUNT",
        "admin_panel": "ADMINISTRATION PANEL",
        "card_num": "Card Number:",
        "pin": "PIN Code:",
        "recipient": "Recipient:",
        "name": "Full Name:",
        "deposit_lbl": "Deposit (UAH):",
        "amount_lbl": "Amount:",
        "confirm": "✔ CONFIRM",
        "balance_btn": "💳 BALANCE",
        "take_btn": "💵 WITHDRAW",
        "deposit_btn": "📥 DEPOSIT",
        "transfer_btn": "💸 TRANSFER",
        "history_btn": "📄 HISTORY",
        "cancel_btn": "✖ CANCEL",
        "reg_btn": "➕ NEW CLIENT",
        "clear_btn": "⌫ CLEAR",
        "finish_btn": "🚪 EXIT",
        "unblock_btn": "🔓 UNBLOCK",
        "lang_btn": "🇬🇧 EN",
        "processing": "⏳ Processing request...",
        "success": "Success!",
        "transfer_success": "Transfer successful!",
        "unblocked": "Card unblocked!",
        "empty_history": "Transaction history is empty",
        "history_title": "RECENT OPERATIONS:\n",
        "enter_amount": "Enter amount:",
        "enter_target": "Recipient card:",
        "enter_unblock": "Card to unblock:",
        "session_timeout": "Session ended due to inactivity",
        "support_title": "CUSTOMER SUPPORT",
        "support_phone": "0 800 500 000",
        "support_info": "Toll-free in Ukraine"
    }
}


class ATMApp:
    def __init__(self, root: tk.Tk, bank: BankSystem):
        self.root = root
        self.bank = bank
        self.current_user = None
        self.active_entry = None
        self.mode = "login"
        self.is_processing = False
        self.timeout_id = None
        self.current_lang = "uk"

        self._setup_window()
        self._setup_styles()
        self._create_widgets()
        self._bind_events()
        self.reset_timeout()

    def t(self, key: str) -> str:
        return TRANSLATIONS[self.current_lang].get(key, key)

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "uk" else "uk"
        self.btn_lang.config(text=self.t("lang_btn"))
        self.title_label.config(text=self.t("title"))
        self.card_label.config(text=self.t("card_num"))
        self.pin_label.config(text=self.t("pin"))
        self.btn_confirm.config(text=self.t("confirm"))
        self.btn_cancel.config(text=self.t("cancel_btn"))
        self.btn_register.config(text=self.t("reg_btn"))
        self.btn_clear.config(text=self.t("clear_btn"))
        self.btn_finish.config(text=self.t("finish_btn"))
        self.supp_title.config(text=self.t("support_title"))
        self.supp_phone.config(text=self.t("support_phone"))
        self.supp_info.config(text=self.t("support_info"))

        if self.mode == "login":
            self.screen_title.config(text=self.t("welcome"))
        elif self.mode == "account":
            self.screen_title.config(text=f"{self.t('cabinet')}: {self.current_user.name}")
        elif self.mode == "admin":
            self.screen_title.config(text=self.t("admin_panel"))

    def reset_timeout(self, event=None):
        if self.timeout_id:
            self.root.after_cancel(self.timeout_id)
        if self.current_user or self.mode == "admin":
            self.timeout_id = self.root.after(30000, self.auto_logout)

    def auto_logout(self):
        if self.current_user or self.mode == "admin":
            self.status_label.config(text=self.t("session_timeout"), fg="#ff8a80")
            self.logout()

    def _setup_window(self):
        self.root.geometry("700x740")
        self.root.config(bg="#121820")
        self.root.title("Банкомат - Kudryavtsev BANK")
        self.root.resizable(False, False)

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Num.TButton", font=("Consolas", 14, "bold"), background="#2a3441", foreground="#ffffff")
        self.style.configure("Confirm.TButton", font=("Arial", 10, "bold"), background="#2e7d32", foreground="#ffffff")
        self.style.configure("Primary.TButton", font=("Arial", 10, "bold"), background="#1565c0", foreground="#ffffff")
        self.style.configure("Dark.TButton", font=("Arial", 10, "bold"), background="#37474f", foreground="#ffffff")
        self.style.configure("Warning.TButton", font=("Arial", 10, "bold"), background="#ef6c00", foreground="#ffffff")
        self.style.configure("Danger.TButton", font=("Arial", 10, "bold"), background="#c62828", foreground="#ffffff")

    def _create_widgets(self):
        self.header_frame = tk.Frame(self.root, bg="#0a0e14", height=55)
        self.header_frame.pack(fill="x", side="top")

        self.title_label = tk.Label(self.header_frame, text=self.t("title"), bg="#0a0e14", fg="#00e676",
                                    font=("Consolas", 18, "bold"))
        self.title_label.pack(side="left", padx=20, pady=12)

        self.btn_lang = ttk.Button(self.header_frame, text=self.t("lang_btn"), command=self.toggle_language,
                                   style="Dark.TButton")
        self.btn_lang.pack(side="right", padx=20, pady=10)

        self.atm_display_outer = tk.Frame(self.root, bg="#1e2631", bd=5, relief="raised")
        self.atm_display_outer.place(x=60, y=75, width=580, height=250)
        self.info_frame = tk.Frame(self.atm_display_outer, bg="#081826", bd=3, relief="sunken")
        self.info_frame.place(x=15, y=15, width=540, height=210)

        self.screen_title = tk.Label(self.info_frame, text=self.t("welcome"), bg="#081826", fg="#80d8ff",
                                     font=("Arial", 12, "bold"))
        self.screen_title.place(x=20, y=15)

        self.card_label = tk.Label(self.info_frame, text=self.t("card_num"), bg="#081826", fg="white",
                                   font=("Arial", 10, "bold"))
        self.card_label.place(x=20, y=55)
        self.card_entry = tk.Entry(self.info_frame, font=("Consolas", 12, "bold"), bg="#e0f7fa", fg="#004d40", width=20)
        self.card_entry.place(x=150, y=53)

        self.pin_label = tk.Label(self.info_frame, text=self.t("pin"), bg="#081826", fg="white",
                                  font=("Arial", 10, "bold"))
        self.pin_label.place(x=20, y=90)
        self.pin_entry = tk.Entry(self.info_frame, show="*", font=("Consolas", 12, "bold"), bg="#e0f7fa", fg="#004d40",
                                  width=20)
        self.pin_entry.place(x=150, y=88)

        self.admin_entry = tk.Entry(self.info_frame, font=("Consolas", 12, "bold"), bg="#e0f7fa", fg="#004d40",
                                    width=20)
        self.reg_name_entry = tk.Entry(self.info_frame, font=("Arial", 11), bg="#e0f7fa", width=20)
        self.amount_entry = tk.Entry(self.info_frame, font=("Consolas", 12, "bold"), bg="#e0f7fa", width=20)

        self.status_label = tk.Label(self.info_frame, text="", bg="#081826", fg="#ffd54f", font=("Arial", 10, "bold"),
                                     wraplength=500, justify="left")
        self.status_label.place(x=20, y=168)
        self.balance_label = tk.Label(self.info_frame, text="", bg="#081826", fg="#69f0ae",
                                      font=("Consolas", 12, "bold"), justify="left")

        self._create_keypad()
        self._create_control_buttons()
        self._create_support_block()

    def _create_keypad(self):
        self.keypad_frame = tk.Frame(self.root, bg="#1a222d", bd=4, relief="groove")
        self.keypad_frame.place(x=215, y=355, width=270, height=280)
        positions = {"1": (12, 12), "2": (98, 12), "3": (184, 12), "4": (12, 75), "5": (98, 75), "6": (184, 75),
                     "7": (12, 138), "8": (98, 138), "9": (184, 138), "0": (98, 201)}
        for num, (x, y) in positions.items():
            btn = ttk.Button(self.keypad_frame, text=num, command=lambda n=num: self.number_click(n),
                             style="Num.TButton")
            btn.place(x=x, y=y, width=74, height=54)

    def _create_control_buttons(self):
        self.btn_confirm = ttk.Button(self.root, text=self.t("confirm"), command=self.handle_confirm,
                                      style="Confirm.TButton")
        self.btn_confirm.place(x=505, y=355, width=160, height=42)

        self.btn_balance = ttk.Button(self.root, text=self.t("balance_btn"), command=self.show_balance,
                                      style="Dark.TButton")
        self.btn_take = ttk.Button(self.root, text=self.t("take_btn"), command=self.start_take_money,
                                   style="Dark.TButton")
        self.btn_deposit = ttk.Button(self.root, text=self.t("deposit_btn"), command=self.start_deposit_money,
                                      style="Primary.TButton")
        self.btn_transfer = ttk.Button(self.root, text=self.t("transfer_btn"), command=self.start_transfer,
                                       style="Primary.TButton")
        self.btn_history = ttk.Button(self.root, text=self.t("history_btn"), command=self.show_history,
                                      style="Dark.TButton")
        self.btn_unblock = ttk.Button(self.root, text=self.t("unblock_btn"), command=self.admin_unblock,
                                      style="Warning.TButton")

        self.btn_cancel = ttk.Button(self.root, text=self.t("cancel_btn"), command=self.cancel_action,
                                     style="Cancel.TButton")
        self.btn_cancel.place(x=505, y=575, width=160, height=42)

        self.btn_register = ttk.Button(self.root, text=self.t("reg_btn"), command=self.show_registration,
                                       style="Primary.TButton")
        self.btn_register.place(x=35, y=355, width=160, height=42)
        self.btn_clear = ttk.Button(self.root, text=self.t("clear_btn"), command=self.clear, style="Warning.TButton")
        self.btn_clear.place(x=35, y=410, width=160, height=42)
        self.btn_finish = ttk.Button(self.root, text=self.t("finish_btn"), command=self.logout, style="Danger.TButton")
        self.btn_finish.place(x=225, y=660, width=250, height=45)

    def _create_support_block(self):
        self.support_frame = tk.Frame(self.root, bg="#1a222d", bd=2, relief="groove")
        self.support_frame.place(x=505, y=410, width=160, height=152)

        self.supp_title = tk.Label(self.support_frame, text=self.t("support_title"), bg="#1a222d", fg="#78909c",
                                   font=("Arial", 9, "bold"))
        self.supp_title.pack(pady=(10, 2))

        self.supp_icon = tk.Label(self.support_frame, text="📞", bg="#1a222d", fg="#42a5f5", font=("Arial", 18))
        self.supp_icon.pack()

        self.supp_phone = tk.Label(self.support_frame, text=self.t("support_phone"), bg="#1a222d", fg="#ffffff",
                                   font=("Consolas", 11, "bold"))
        self.supp_phone.pack(pady=(2, 2))

        self.supp_info = tk.Label(self.support_frame, text=self.t("support_info"), bg="#1a222d", fg="#546e7a",
                                  font=("Arial", 8))
        self.supp_info.pack()

    def _bind_events(self):
        self.root.bind("<Any-KeyPress>", self.reset_timeout)
        self.root.bind("<Any-ButtonPress>", self.reset_timeout)

        self.card_entry.bind("<FocusIn>", lambda e: setattr(self, 'active_entry', self.card_entry))
        self.pin_entry.bind("<FocusIn>", lambda e: setattr(self, 'active_entry', self.pin_entry))
        self.amount_entry.bind("<FocusIn>", lambda e: setattr(self, 'active_entry', self.amount_entry))
        self.admin_entry.bind("<FocusIn>", lambda e: setattr(self, 'active_entry', self.admin_entry))

        # ВОЗВРАЩЕНО АВТОМАТИЧЕСКОЕ ФОРМАТИРОВАНИЕ КАРТЫ (ДЕФИСЫ)
        self.card_entry.bind("<KeyRelease>", self._format_card_entry)
        self.admin_entry.bind("<KeyRelease>", self._format_card_entry)

        self.active_entry = self.card_entry
        self.card_entry.focus_set()

    def _format_card_entry(self, event=None):
        if event and event.keysym in ("BackSpace", "Delete", "Left", "Right"):
            return
        if self.active_entry not in (self.card_entry, self.admin_entry):
            return

        text = self.active_entry.get().replace("-", "")
        digits = "".join([ch for ch in text if ch.isdigit()])[:16]

        formatted = ""
        for i, ch in enumerate(digits):
            if i > 0 and i % 4 == 0:
                formatted += "-"
            formatted += ch

        self.active_entry.delete(0, tk.END)
        self.active_entry.insert(0, formatted)

    def number_click(self, number: str):
        if not self.is_processing and self.active_entry and self.active_entry.winfo_viewable():
            self.active_entry.insert(tk.END, number)
            if self.active_entry in (self.card_entry, self.admin_entry):
                self._format_card_entry()
            self.reset_timeout()

    def clear(self):
        if not self.is_processing and self.active_entry and self.active_entry.winfo_viewable():
            txt = self.active_entry.get()
            if txt:
                self.active_entry.delete(len(txt) - 1, tk.END)
                if self.active_entry in (self.card_entry, self.admin_entry):
                    self._format_card_entry()

    def _simulate_processing(self, callback):
        self.is_processing = True
        self.status_label.config(text=self.t("processing"), fg="#ffd54f")
        self.root.after(800, lambda: self._finish_processing(callback))

    def _finish_processing(self, callback):
        self.is_processing = False
        try:
            callback()
        except ValueError as err:
            self.status_label.config(text=str(err), fg="#ff8a80")

    def handle_confirm(self):
        if self.is_processing: return
        self.reset_timeout()
        if self.mode == "login":
            self.login()
        elif self.mode == "withdraw":
            self._simulate_processing(lambda: self.execute_tx(WithdrawTransaction))
        elif self.mode == "deposit":
            self._simulate_processing(lambda: self.execute_tx(DepositTransaction))
        elif self.mode == "transfer":
            self._simulate_processing(self.execute_transfer)

    def login(self):
        card = self.card_entry.get().replace("-", "")
        pin = self.pin_entry.get()
        if card == "0000000000000000" and pin == "0000":
            self._simulate_processing(self.show_admin_panel)
            return

        def action():
            self.current_user = self.bank.authenticate(card, pin)
            self.mode = "account"
            self._hide_all()
            self.screen_title.config(text=f"{self.t('cabinet')}: {self.current_user.name}")
            self.btn_balance.place(x=505, y=410, width=160, height=42)
            self.btn_take.place(x=505, y=465, width=160, height=42)
            self.btn_deposit.place(x=505, y=520, width=160, height=42)
            self.btn_transfer.place(x=35, y=465, width=160, height=42)
            self.btn_history.place(x=35, y=355, width=160, height=42)
            self.btn_clear.place(x=35, y=410, width=160, height=42)
            self.show_balance()

        self._simulate_processing(action)

    def execute_tx(self, tx_class):
        amount = float(self.amount_entry.get() or 0)
        if self.bank.process_transaction(self.current_user, tx_class(amount)):
            self.status_label.config(text=self.t("success"), fg="#69f0ae")
            self.show_balance()

    def execute_transfer(self):
        amount = float(self.amount_entry.get() or 0)
        target_card = self.admin_entry.get().replace("-", "")
        if not self.bank.is_valid_luhn(target_card):
            raise ValueError("Невірний формат картки!" if self.current_lang == "uk" else "Invalid card format!")
        target = self.bank.db.get_user(target_card)
        if not target:
            raise ValueError("Отримувача не знайдено!" if self.current_lang == "uk" else "Recipient not found!")
        if self.bank.process_transaction(self.current_user, TransferTransaction(amount, target)):
            self.status_label.config(text=self.t("transfer_success"), fg="#69f0ae")
            self.show_balance()

    def show_balance(self):
        self._hide_inputs()
        self.mode = "account"
        self.balance_label.config(
            text=f"Баланс: {self.current_user.balance:,.2f} UAH" if self.current_lang == "uk" else f"Balance: {self.current_user.balance:,.2f} UAH")
        self.balance_label.place(x=20, y=90)
        self.status_label.config(text="")

    def show_history(self):
        self._hide_inputs()
        history = self.bank.db.get_user_history(self.current_user.card_number)
        txt = self.t("history_title") + "\n".join(history) if history else self.t("empty_history")
        self.status_label.config(text=txt, fg="#80d8ff")

    def start_take_money(self):
        self._setup_input(self.t("enter_amount"), self.amount_entry, "withdraw")

    def start_deposit_money(self):
        self._setup_input(self.t("enter_amount"), self.amount_entry, "deposit")

    def start_transfer(self):
        self._setup_input(self.t("enter_target"), self.admin_entry, "transfer")
        self.amount_entry.place(x=150, y=125)
        tk.Label(self.info_frame, text=self.t("amount_lbl"), bg="#081826", fg="white",
                 font=("Arial", 10, "bold")).place(x=20, y=127)

    def show_admin_panel(self):
        self.mode = "admin"
        self._hide_all()
        self.screen_title.config(text=self.t("admin_panel"))
        self.balance_label.config(text=self.bank.get_admin_stats())
        self.balance_label.place(x=20, y=55)
        self.btn_unblock.place(x=35, y=355, width=160, height=42)
        self._setup_input(self.t("enter_unblock"), self.admin_entry, "admin")
        self.reset_timeout()

    def admin_unblock(self):
        card = self.admin_entry.get().replace("-", "")

        def action():
            self.bank.unblock_user_card(card)
            self.status_label.config(text=self.t("unblocked"), fg="#69f0ae")
            self.balance_label.config(text=self.bank.get_admin_stats())

        self._simulate_processing(action)

    def show_registration(self):
        def action():
            card = self.bank.register_client("Новий Клієнт", "1111", 0.0)
            self.status_label.config(text=f"Створено: {card}\nPIN: 1111", fg="#69f0ae")

        self._simulate_processing(action)

    def _setup_input(self, label_text, entry_widget, mode):
        self.balance_label.place_forget()
        self.status_label.config(text=label_text, fg="white")
        entry_widget.delete(0, tk.END)
        entry_widget.place(x=150, y=165)
        entry_widget.focus_set()
        self.active_entry = entry_widget
        self.mode = mode

    def _hide_inputs(self):
        self.amount_entry.place_forget()
        self.admin_entry.place_forget()
        for widget in self.info_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") in ("Сума:", "Amount:"): widget.place_forget()

    def _hide_all(self):
        self._hide_inputs()
        self.card_entry.place_forget()
        self.pin_entry.place_forget()
        self.card_label.place_forget()
        self.pin_label.place_forget()
        self.balance_label.place_forget()
        self.btn_register.place_forget()
        self.btn_balance.place_forget()
        self.btn_take.place_forget()
        self.btn_deposit.place_forget()
        self.btn_transfer.place_forget()
        self.btn_history.place_forget()
        self.btn_unblock.place_forget()
        self.support_frame.place_forget()
        self.status_label.config(text="")

    def cancel_action(self):
        if self.current_user:
            self.show_balance()
        else:
            self.logout()

    def logout(self):
        self.current_user = None
        self.mode = "login"
        self._hide_all()
        self.screen_title.config(text=self.t("welcome"))
        self.card_label.config(text=self.t("card_num"))
        self.card_label.place(x=20, y=55)
        self.card_entry.delete(0, tk.END)
        self.card_entry.place(x=150, y=53)
        self.pin_label.config(text=self.t("pin"))
        self.pin_entry.delete(0, tk.END)
        self.pin_entry.place(x=150, y=88)
        self.btn_register.place(x=35, y=355, width=160, height=42)
        self.btn_clear.place(x=35, y=410, width=160, height=42)
        self.support_frame.place(x=505, y=410, width=160, height=152)
        self.active_entry = self.card_entry
        if self.timeout_id: self.root.after_cancel(self.timeout_id)