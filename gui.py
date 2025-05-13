# gui.py - графический интерфейс пользователя

import tkinter as tk
from tkinter import ttk
import threading
import asyncio
from parser import collect_vacancies
from database import get_saved_vacancies


class VacancyParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Парсер вакансий HH")
        self.root.geometry("800x600")

        # Выбор языка программирования
        self.label = tk.Label(root, text="Выберите язык программирования:")
        self.label.pack(pady=5)

        self.languages = ["Python", "JavaScript", "Java", "C++", "Go", "Ruby"]
        self.lang_var = tk.StringVar(value=self.languages[0])
        self.combo = ttk.Combobox(root, textvariable=self.lang_var, values=self.languages, state="readonly")
        self.combo.pack(pady=5)

        # Кнопка запуска парсинга
        self.btn = tk.Button(root, text="Начать парсинг", command=self.start_parsing)
        self.btn.pack(pady=10)

        # Статус операции
        self.status = tk.Label(root, text="")
        self.status.pack()

        # Таблица результатов
        self.columns = ("Должность", "Компания", "Город", "Зарплата", "Ссылка")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=150)

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Для сортировки
        self.sort_reverse = {col: False for col in self.columns}

        # Добавляем обработчик клика по ссылке
        self.tree.bind("<Double-1>", self.open_link)

    def sort_column(self, col, reverse):
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        
        if col == "Зарплата":
            def extract_salary(val):
                try:
                    return int(''.join(filter(str.isdigit, val)))
                except:
                    return 0
            data.sort(key=lambda x: extract_salary(x[0]), reverse=reverse)
        else:
            data.sort(reverse=reverse)

        for idx, (_, k) in enumerate(data):
            self.tree.move(k, "", idx)

        self.sort_reverse[col] = not reverse
        self.tree.heading(col, command=lambda: self.sort_column(col, self.sort_reverse[col]))

    def open_link(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        url = values[-1]
        import webbrowser
        webbrowser.open(url)

    def start_parsing(self):
        keyword = self.lang_var.get()
        self.status.config(text=f"🔄 Идёт поиск по: {keyword}...")
        threading.Thread(target=self.run_async, args=(keyword,), daemon=True).start()

    def run_async(self, keyword):
        asyncio.run(collect_vacancies(keyword))
        self.show_results()

    def show_results(self):
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = get_saved_vacancies()
        for item in data:
            self.tree.insert("", "end", values=item)
        self.status.config(text=f"✅ Найдено {len(data)} вакансий")


def run_gui():
    root = tk.Tk()
    app = VacancyParserGUI(root)
    root.mainloop()