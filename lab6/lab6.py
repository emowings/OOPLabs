import tkinter as tk
import threading
import time
import random
import math


class ParticleSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Симулятор частиц в космосе")
        self.root.geometry("500x500")
        self.root.configure(bg="#000022")

        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="#000022", highlightthickness=0)
        self.canvas.pack()

        # Центр гравитации (в середине экрана)
        self.gravity_center = [250, 250]

        # Три частицы с разными свойствами
        self.particles = []
        colors = ["#ff3366", "#33ff99", "#6699ff"]
        sizes = [18, 22, 15]
        masses = [1.2, 1.8, 0.9]  # влияют на силу притяжения и отталкивания

        for i in range(3):
            x = random.randint(80, 420)
            y = random.randint(80, 420)
            vx = random.uniform(-2.5, 2.5)
            vy = random.uniform(-2.5, 2.5)
            particle = {
                "id": None,
                "x": x,
                "y": y,
                "vx": vx,
                "vy": vy,
                "color": colors[i],
                "size": sizes[i],
                "mass": masses[i]
            }
            self.particles.append(particle)

        # Создаём фигуры на канвасе
        for p in self.particles:
            p["id"] = self.canvas.create_oval(
                p["x"] - p["size"], p["y"] - p["size"],
                p["x"] + p["size"], p["y"] + p["size"],
                fill=p["color"], outline="#ffffff", width=1
            )

        self.running = True
        self.start_animation_threads()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def animate_particle(self, particle_index: int):
        """Поток для движения одной частицы"""
        p = self.particles[particle_index]

        while self.running:
            # Гравитация к центру
            dx = self.gravity_center[0] - p["x"]
            dy = self.gravity_center[1] - p["y"]
            dist = math.hypot(dx, dy) or 1  # избегать деления на 0
            force = 0.0008 * p["mass"] / (dist ** 1.5)  # слабая гравитация

            p["vx"] += force * dx
            p["vy"] += force * dy

            # Небольшое случайное ускорение (турбулентность)
            if random.random() < 0.03:
                p["vx"] += random.uniform(-0.8, 0.8)
                p["vy"] += random.uniform(-0.8, 0.8)

            # Обновление позиции
            p["x"] += p["vx"]
            p["y"] += p["vy"]

            # Отскок от границ (мягкий, с потерей энергии)
            if p["x"] < p["size"] or p["x"] > 500 - p["size"]:
                p["vx"] *= -0.85
                p["x"] = max(p["size"], min(500 - p["size"], p["x"]))
            if p["y"] < p["size"] or p["y"] > 500 - p["size"]:
                p["vy"] *= -0.85
                p["y"] = max(p["size"], min(500 - p["size"], p["y"]))

            # Простое отталкивание от других частиц
            for other in self.particles:
                if other is p:
                    continue
                dx = p["x"] - other["x"]
                dy = p["y"] - other["y"]
                dist = math.hypot(dx, dy)
                if 0 < dist < p["size"] + other["size"]:
                    # Отталкивание пропорционально массам
                    repel_force = 1.5 / (dist ** 1.2)
                    p["vx"] += repel_force * dx * other["mass"]
                    p["vy"] += repel_force * dy * other["mass"]

            # Обновление на канвасе (в главном потоке через after)
            self.root.after(0, lambda pid=particle_index: self.update_canvas(pid))

            time.sleep(0.025 + random.uniform(-0.005, 0.005))  # небольшая случайность

    def update_canvas(self, particle_index: int):
        """Обновление позиции частицы на канвасе"""
        if not self.running:
            return
        p = self.particles[particle_index]
        size = p["size"]
        self.canvas.coords(
            p["id"],
            p["x"] - size, p["y"] - size,
            p["x"] + size, p["y"] + size
        )

    def start_animation_threads(self):
        """Запуск трёх независимых потоков"""
        for i in range(3):
            t = threading.Thread(target=self.animate_particle, args=(i,), daemon=True)
            t.start()

    def on_close(self):
        self.running = False
        self.root.destroy()


def main():
    ParticleSimulator()


if __name__ == "__main__":
    main()
