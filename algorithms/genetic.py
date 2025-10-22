import random
import math

# === Обчислення відстані між двома точками ===
def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# === Загальна довжина маршруту ===
def total_distance(route, cities):
    dist = 0
    for i in range(len(route) - 1):
        dist += distance(cities[route[i]], cities[route[i + 1]])
    dist += distance(cities[route[-1]], cities[route[0]])  # повертаємося в початок
    return dist

# === Ініціалізація популяції ===
def create_population(cities, pop_size):
    base = list(range(len(cities)))
    population = []
    for _ in range(pop_size):
        individual = base[:]
        random.shuffle(individual)
        population.append(individual)
    return population

# === Вибір батьків (турнірний відбір) ===
def tournament_selection(population, cities, k=3):
    selected = random.sample(population, k)
    selected.sort(key=lambda ind: total_distance(ind, cities))
    return selected[0]

# === Кросовер (OX — Order Crossover) ===
def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    child[start:end] = parent1[start:end]

    fill_values = [x for x in parent2 if x not in child]
    fill_index = [i for i, x in enumerate(child) if x is None]
    for i, val in zip(fill_index, fill_values):
        child[i] = val
    return child

# === Мутація (обмін двох генів) ===
def mutate(individual, mutation_rate=0.02):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

# === Генетичний алгоритм ===
def genetic_algorithm(cities, pop_size=100, generations=500,
                      mutation_rate=0.02, elite_size=5):
    """
    Виконує пошук найкоротшого маршруту між містами.
    Повертає: (найкращий_маршрут, його_довжина)
    """
    population = create_population(cities, pop_size)
    best_route = min(population, key=lambda r: total_distance(r, cities))
    best_distance = total_distance(best_route, cities)

    for gen in range(generations):
        # Оцінка
        population.sort(key=lambda r: total_distance(r, cities))
        new_population = population[:elite_size]  # еліти зберігаємо

        # Вибір + кросовер
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, cities)
            parent2 = tournament_selection(population, cities)
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

        # Оновлення найкращого результату
        current_best = population[0]
        current_distance = total_distance(current_best, cities)
        if current_distance < best_distance:
            best_route, best_distance = current_best, current_distance

        # Кожні 20 поколінь виводимо прогрес
        if gen % 20 == 0 or gen == generations - 1:
            print(f"Покоління {gen+1}/{generations} | Поточна найкраща довжина: {best_distance:.2f}")

    return best_route + [best_route[0]], best_distance
