import tkinter as tk
from tkinter import ttk, messagebox
from gui import TSPGui
from algorithms.brute_force import brute_force

# Если есть генетический алгоритм — можно подключить
try:
    from algorithms.genetic import genetic_algorithm
except ImportError:
    genetic_algorithm = None


class TSPApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg='black')
        self.root.title("Задача комівояжера — Вибір методу")
        self.root.geometry("350x400")
        self.root.resizable(False, False)

        # ======== Вибір мови ========
        """
        self.lang_var = tk.StringVar(value="Українська")
        tk.Label(self.root, text="Мова інтерфейсу:", font=("Arial", 12, "bold"), bg='black', fg='white').pack(pady=5)
        self.lang_menu = ttk.Combobox(
            self.root, textvariable=self.lang_var,
            values=["Українська", "English", "Deutsch"],
            state="readonly", font=("Arial", 11)
        )
        self.lang_menu.pack(pady=5)
        """

        # ======== Вибір методу ========
        self.method_var = tk.StringVar(value="Brute Force")
        tk.Label(self.root, text="Виберіть метод розв’язання:", font=("Arial", 12, "bold"),bg='black', fg='white').pack(pady=10)
        self.method_menu = ttk.Combobox(
            self.root,
            textvariable=self.method_var,
            values=["Brute Force", "Genetic Algorithm"],
            state="readonly", font=("Arial", 11)
        )
        self.method_menu.pack(pady=5)
        self.method_menu.current(0)

        # ======== Вибір карти ========
        self.map_var = tk.StringVar(value="Без карти") # add your image as background
        tk.Label(self.root, text="Вибір карти:", font=("Arial", 12, "bold"),bg='black', fg='white').pack(pady=5)
        self.map_menu = ttk.Combobox(
            self.root, textvariable=self.map_var,
            values=["Без карти", "Україна", "Німеччина"],
            state="readonly", font=("Arial", 11)
        )
        self.map_menu.pack(pady=5)
        self.map_menu.current(0)
        # Автоматична зміна меж при виборі карти
        self.map_menu.bind("<<ComboboxSelected>>", self.on_map_change)


        # ======== Межі координат ========
        frame = tk.LabelFrame(self.root, text="Параметри координат", font=("Arial", 11, "bold"), labelanchor="nw")       
        frame.pack(pady=10)

        # X limits
        tk.Label(frame, text="X від:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.x_min = tk.Entry(frame, width=5)
        self.x_min.insert(0, "0")
        self.x_min.grid(row=0, column=1)

        tk.Label(frame, text="до:", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.x_max = tk.Entry(frame, width=5)
        self.x_max.insert(0, "100")
        self.x_max.grid(row=0, column=3)

        # Y limits
        tk.Label(frame, text="Y від:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.y_min = tk.Entry(frame, width=5)
        self.y_min.insert(0, "0")
        self.y_min.grid(row=1, column=1)

        tk.Label(frame, text="до:", font=("Arial", 10)).grid(row=1, column=2, padx=5)
        self.y_max = tk.Entry(frame, width=5)
        self.y_max.insert(0, "100")
        self.y_max.grid(row=1, column=3)

        # --- Кнопка запуску ---
        tk.Button(
            self.root,
            text="Почати введення міст",
            font=("Arial", 11, "bold"),
            bg="#333333",  # тёмно-серый
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            padx=10, pady=5,
            command=self.start_app
        ).pack(pady=20)


        tk.Label(self.root, text="Після вибору методу і введення точок закрий вікно карти", font=("Arial", 9), bg='black', fg='white').pack()
        tk.Label(self.root, text="© ArtG", font=("Arial", 9, "italic"), bg='black', fg='gray').pack(side="bottom", pady=5)
        
        self.root.mainloop()

    def on_map_change(self, event=None):
        """Автоматично змінює межі X/Y при виборі карти"""
        choice = self.map_var.get()

        if choice == "Україна":
            self.x_min.delete(0, tk.END)
            self.x_min.insert(0, "0")
            self.x_max.delete(0, tk.END)
            self.x_max.insert(0, "1200")

            self.y_min.delete(0, tk.END)
            self.y_min.insert(0, "0")
            self.y_max.delete(0, tk.END)
            self.y_max.insert(0, "848")

        elif choice == "Німеччина":
            self.x_min.delete(0, tk.END)
            self.x_min.insert(0, "0")
            self.x_max.delete(0, tk.END)
            self.x_max.insert(0, "1555")

            self.y_min.delete(0, tk.END)
            self.y_min.insert(0, "0")
            self.y_max.delete(0, tk.END)
            self.y_max.insert(0, "2200")

        else:  # Без карти
            self.x_min.delete(0, tk.END)
            self.x_min.insert(0, "0")
            self.x_max.delete(0, tk.END)
            self.x_max.insert(0, "100")

            self.y_min.delete(0, tk.END)
            self.y_min.insert(0, "0")
            self.y_max.delete(0, tk.END)
            self.y_max.insert(0, "100")


    def start_app(self):
        """Запускає введення точок та вибір алгоритму"""
        method = self.method_var.get()
        map_choice = self.map_var.get()

        try:
            xlim = (float(self.x_min.get()), float(self.x_max.get()))
            ylim = (float(self.y_min.get()), float(self.y_max.get()))
        except ValueError:
            messagebox.showerror("Помилка", "Уведіть правильні числові межі для координат.")
            return

        if xlim[0] >= xlim[1] or ylim[0] >= ylim[1]:
            messagebox.showerror("Помилка", "Максимальне значення має бути більше мінімального!")
            return

        app = TSPGui(method, xlim=xlim, ylim=ylim, map_choice=map_choice)
        cities = app.input_points()

        if len(cities) < 2:
            messagebox.showwarning("Помилка", "Потрібно хоча б 2 точки!")
            return

        print(f"🔹 Обрано метод: {method}")
        print(f"📏 Поле координат: X={xlim}, Y={ylim}")

        if method == "Brute Force":
            route, dist = brute_force(cities)
        elif method == "Genetic Algorithm" and genetic_algorithm:
            route, dist = genetic_algorithm(cities)
        else:
            messagebox.showerror("Помилка", f"'{method}' ще не реалізований.")
            return

        app.show_route(route, dist)

        print("\n🚗 Найкоротший маршрут:", ' → '.join(str(i + 1) for i in route))
        print(f"📏 Довжина маршруту: {dist:.2f}")


if __name__ == "__main__":
    TSPApp()
