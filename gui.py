# gui.py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

plt.style.use('dark_background')


class TSPGui:
    def __init__(self, method, xlim=(0, 100), ylim=(0, 100), map_choice="Без карти", figsize=(10, 8), fullscreen=False):
        self.method = method  # добавить алгоритм из main.py

        self.cities = []
        self.xlim = xlim
        self.ylim = ylim
        self.map_choice = map_choice


        self.figsize = figsize
        self.fullscreen = fullscreen
        self.fig = None
        self.cid = None

        self.maps_dir = os.path.join(os.path.dirname(__file__), "maps") # 📂 абсолютный путь к папке "maps"


    def _load_map(self):
        """Завантажує фонове зображення карти (якщо обрано)."""
        try:
            if self.map_choice == "Україна":
                img_path = os.path.join(self.maps_dir, "ukraine.png")
                # img_path = "maps/ukraine.png"
            elif self.map_choice == "Німеччина":
                img_path = os.path.join(self.maps_dir, "germany.png")
            else:
                return  # Без карти

            img = mpimg.imread(img_path)
            plt.imshow(img, extent=[*self.xlim, *self.ylim], alpha=0.7)
        except FileNotFoundError:
            print(f"⚠️ Не знайдено файл: {img_path}")

    def _reset_figure(self):
        """Создаёт новую фигуру, отключая старые обработчики"""
        # если был подключён старый обработчик — отключаем
        try:
            if self.fig is not None and self.cid is not None:
                try:
                    self.fig.canvas.mpl_disconnect(self.cid)
                except Exception:
                    pass
                plt.close(self.fig)
        except Exception:
            pass


        self.fig = plt.figure(f"Введення міст. Метод: {self.method}, Карта: {self.map_choice}", figsize=self.figsize)
        ax = self.fig.add_subplot(111)
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        ax.set_xlim(*self.xlim)
        ax.set_ylim(*self.ylim)
        ax.grid(True, color='gray', alpha=0.3)
        ax.set_title(f"Додай міста кліками миші. Карта ({self.map_choice}). Закрий вікно, коли завершиш.", color='white')
        
        self._load_map()  # вызов карты

        if self.fullscreen:
            try:
                mng = plt.get_current_fig_manager()
                mng.window.state('zoomed')  # для Windows
            except Exception:
                pass

        self.fig.canvas.draw()


    def onclick(self, event):
        """Добавление точки при клике"""
        if event.xdata is not None and event.ydata is not None:
            self.cities.append((event.xdata, event.ydata))
            plt.scatter(event.xdata, event.ydata, color='red')
            plt.text(event.xdata + 0.5, event.ydata + 0.5, str(len(self.cities)),
                     fontsize=12, color='cyan')
            plt.draw()

    def input_points(self):
        """Открывает окно для ввода точек. Всегда начинает с чистого состояния."""
        # очищаем старые точки
        self.cities = []

        self._reset_figure()
        # подключаем новый обработчик
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.show()

        # После закрытия окна — отключаем обработчик и возвращаем список городов
        try:
            if self.fig is not None and self.cid is not None:
                try:
                    self.fig.canvas.mpl_disconnect(self.cid)
                except Exception:
                    pass
        except Exception:
            pass

        return self.cities

    def show_route(self, route, distance):
        """Отображает найденный маршрут.
           route может быть:
             - замкнутым: [0,1,2,0]
             - незамкнутым: [0,1,2]  (тогда мы добавим возврат в старт)
        """
        if route is None:
            print("⚠️ Нет маршрута для отображения.")
            return

        # Проверяем корректность индексов и длину
        n = len(self.cities)
        if n == 0:
            print("⚠️ Нет точек для отображения.")
            return

        # Если маршрут задан как незамкнутый — замкнём его
        if len(route) > 0 and route[0] != route[-1]:
            route = list(route) + [route[0]]

        # Проверка: все индексы должны принадлежать 0..n-1
        if not all(isinstance(idx, int) and 0 <= idx < n for idx in route):
            print("⚠️ Некорректный маршрут (индексы не соответствуют точкам).")
            return

        plt.figure(F"Оптимальний маршрут, Метод: {self.method}", figsize=self.figsize)
        plt.clf() # очистка окна
        plt.xlim(*self.xlim)
        plt.ylim(*self.ylim)
        plt.grid(True, color='gray', alpha=0.3)
        self._load_map()  # фон карты

        x = [self.cities[i][0] for i in route]
        y = [self.cities[i][1] for i in route]

        plt.plot(x, y, 'y-o', lw=2)
        for i, (cx, cy) in enumerate(self.cities):
            plt.text(cx + 0.5, cy + 0.5, str(i + 1), fontsize=12, color='cyan')

        plt.title(f"Найкоротший маршрут (длина: {distance:.2f})", color='white')
        plt.xlabel("X координата", color='white')
        plt.ylabel("Y координата", color='white')
        plt.show()
