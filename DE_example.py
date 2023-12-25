import json
from tg_logger import TelegramBot
import os
import matplotlib.pyplot as plt
from utils import TGTqdm

token = os.getenv('TOKEN')
chat_id = os.getenv('CHAT_ID')

bot = TelegramBot(token, chat_id)
TGTqdm = TGTqdm(bot)

import numpy as np
import random
from scipy.stats import qmc


def send_txt():
    with open('temp/log.txt', 'rb') as f:
        return bot.send_document(chat_id=chat_id, document=f)


def send_json():
    with open('temp/log.json', 'rb') as f:
        return bot.send_document(chat_id=chat_id, document=f)


def plot(history, plot_id, force=False, plot_name='Training'):
    if not history:
        return plot_id
    plt.plot(range(1, len(history) + 1), history, linewidth=3)

    plt.title(plot_name)
    plt.ylabel('Best value')
    plt.xlabel('Iteration')
    plt.xlim(0, len(history) + 1)
    plt.ylim(0, 1.1 * max(history) if history else 1)

    if plot_id is None:
        plot_id = bot.send_plot(plt, plot_name)
    else:
        bot.update_plot(plot_id, plt, plot_name, force=force)

    plt.clf()
    return plot_id


def rastrigin(array, A=10):
    return A * 2 + (array[0] ** 2 - A * np.cos(2 * np.pi * array[0])) + (
            array[1] ** 2 - A * np.cos(2 * np.pi * array[1]))


def griewank(array):
    term_1 = (array[0] ** 2 + array[1] ** 2) / 2
    term_2 = np.cos(array[0] / np.sqrt(2)) * np.cos(array[1] / np.sqrt(2))
    return 1 + term_1 - term_2


def rosenbrock(array):
    return (1 - array[0]) ** 2 + 100 * (array[1] - array[0] ** 2) ** 2


def differential_evolution(fobj=rosenbrock, bounds=2, mutation_coefficient=0.3,
                           crossover_coefficient=0.5, population_size=500, iterations=50,
                           init_setting='random', mutation_setting='rand1',
                           selection_setting='current', p_min=0.1, p_max=0.2):
    # Инициалиация популяции и получение первичных результатов
    SEED = 7
    random.seed(SEED)
    np.random.seed(SEED)
    bounds = np.array(bounds)
    dimensions = len(bounds)
    history = []
    if fobj == "Rosenbrock":
        fobj = rosenbrock
    elif fobj == "Griewank":
        fobj = griewank
    elif fobj == "Rastrigin":
        fobj = rastrigin
    # Случайная инициализация
    if init_setting == 'LatinHypercube':
        # your code
        population = qmc.LatinHypercube(d=dimensions, seed=SEED)
        assert population.__class__ == qmc.LatinHypercube
        population = population.random(n=population_size)
    elif init_setting == 'Halton':
        # your code
        population = qmc.Halton(d=dimensions, seed=SEED)
        assert population.__class__ == qmc.Halton
        population = population.random(n=population_size)
    elif init_setting == 'Sobol':
        # your code
        population = qmc.Sobol(d=dimensions, seed=SEED)
        assert population.__class__ == qmc.Sobol
        population = population.random(n=population_size)
    else:
        population = np.random.rand(population_size, dimensions)

    min_bound, max_bound = bounds.T
    diff = np.fabs(min_bound - max_bound)
    population_denorm = min_bound + population * diff
    fitness = np.asarray([fobj(ind) for ind in population_denorm])
    # Найти лучший индекс
    best_idx = np.argmin(fitness)
    best = population_denorm[best_idx]
    plot_id = None
    for iteration in TGTqdm(range(iterations)):
        for population_index in range(population_size):
            idxs = np.setdiff1d(np.arange(population_size), [best_idx, population_index], assume_unique=True)

            # Выбор трех случайных элементов
            # Оператор мутации
            if mutation_setting == 'rand2':
                a, b, c, d, e = population[np.random.choice(idxs, 5, replace=False)]
                mutant = np.clip(a + mutation_coefficient * (b - c) + mutation_coefficient * (d - e), 0, 1)
                assert 'e' in locals(), "Данный ассерт проверяет, что вы точно написали формулу"
                assert 'd' in locals(), "Данный ассерт проверяет, что вы точно написали формулу"

            elif mutation_setting == 'best1':
                index_of_best1 = np.array(idxs[np.argmin([fitness[ind] for ind in idxs])])
                idxs = np.delete(idxs, np.where(idxs == index_of_best1))
                b, c = population[np.random.choice(idxs, 2, replace=False)]
                assert index_of_best1 not in idxs, "Данный ассерт проверяет, что вы для выбора b и c вы не будете использовать выбранный, чтобы не повторятmся"
                assert index_of_best1 != population_index, "Данный ассерт проверяет, что вы не взяли индекс нынешнего индивида"
                assert index_of_best1 != best_idx, "Данный ассерт проверяет, что вы не взяли индекс самого лучшего индивида"
                if iteration == 0:
                    for idx in idxs: assert np.array_equal(population[index_of_best1], population[
                        idx]) is False, "Данный ассерт проверяет правильность выбранного индекса"
                    assert np.array_equal(population[index_of_best1], population[
                        population_index]) is False, "Данный ассерт проверяет правильность выбранного индекса"
                    assert np.array_equal(population[index_of_best1], population[
                        best_idx]) is False, "Данный ассерт проверяет правильность выбранного индекса"
                mutant = np.clip(population[index_of_best1] + mutation_coefficient * (b - c), 0, 1)

            elif mutation_setting == 'rand_to_p_best1':
                p = np.random.uniform(p_min, p_max)  # не удалять
                p_th = int(p * len(idxs))

                sorted_guys = np.setdiff1d(np.argsort(fitness), [best_idx, population_index], assume_unique=True)
                index_of_rand_to_p_best1 = np.random.choice(sorted_guys[:p_th], replace=False)
                idxs = [i for i in range(population_size) if
                        i not in [best_idx, population_index, index_of_rand_to_p_best1]]
                b, c = population[np.random.choice(idxs, 2, replace=False)]

                assert 'a' not in locals()
                assert index_of_rand_to_p_best1 not in idxs, "Данный ассерт проверяет, что вы для выбора b и c вы не будете использовать выбранный, чтобы не повторятmся"
                assert index_of_rand_to_p_best1 != population_index, "Данный ассерт проверяет, что вы не взяли индекс нынешнего индивида"
                assert index_of_rand_to_p_best1 != best_idx, "Данный ассерт проверяет, что вы не взяли индекс самого лучшего индивида"
                if iteration == 0:
                    for idx in idxs: assert np.array_equal(population[index_of_rand_to_p_best1], population[
                        idx]) is False, "Данный ассерт проверяет правильность выбранного индекса"
                    assert np.array_equal(population[index_of_rand_to_p_best1], population[
                        population_index]) is False, "Данный ассерт проверяет правильность выбранного индекса"
                    assert np.array_equal(population[index_of_rand_to_p_best1], population[
                        best_idx]) is False, "Данный ассерт проверяет правильность выбранного индекса"
                mutant = np.clip(population[index_of_rand_to_p_best1] + mutation_coefficient * (b - c), 0, 1)
            else:
                a, b, c = population[np.random.choice(idxs, 3, replace=False)]
                mutant = np.clip(a + mutation_coefficient * (b - c), 0, 1)
            # Оператор кроссовера
            cross_points = np.random.rand(dimensions) < crossover_coefficient
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            # Рекомбинация (замена мутантными значениями)
            trial = np.where(cross_points, mutant, population[population_index])
            trial_denorm = min_bound + trial * diff
            # Оценка потомка
            result_of_evolution = fobj(trial_denorm)
            # Селекция
            if selection_setting == 'worst':
                selection_index = np.argmax(fitness)
            elif selection_setting == 'random_among_worst':
                worse_guys = np.argwhere(fitness > result_of_evolution).flatten()
                if len(worse_guys) > 0:
                    selection_index = np.random.choice(worse_guys, replace=False)
                else:
                    selection_index = population_index
            elif selection_setting == 'random_selection':
                selection_index = np.random.choice(idxs)
            else:
                selection_index = population_index

            if result_of_evolution < fitness[selection_index]:
                fitness[selection_index] = result_of_evolution
                population[selection_index] = trial
                if result_of_evolution < fitness[best_idx]:
                    best_idx = selection_index
                    best = trial_denorm
        history.append(fitness[best_idx])
        plot_id = plot(history, plot_id, force=True if iteration == iterations - 1 else False)
        yield best, fitness[best_idx]
    json_object = json.dumps(history, indent=4)
    with open("temp/log.json", "w") as outfile:
        outfile.write(json_object)
    bot.send_json()
    json_string = json.dumps(history)
    with open('temp/log.txt', 'w') as file:
        file.write(json_string)
    bot.send_txt()
    bot.clean_tmp_dir()
