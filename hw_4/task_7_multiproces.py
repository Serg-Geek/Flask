# Напишите программу на Python, которая будет находить
# сумму элементов массива из 1000000 целых чисел.
# � Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# � Массив должен быть заполнен случайными целыми числами
# от 1 до 100.
# � При решении задачи нужно использовать многопоточность,
# многопроцессорность и асинхронность.
# � В каждом решении нужно вывести время выполнения
# вычислений.


import time
import random
import multiprocessing


def create_random_array():
    return [random.randint(1, 100) for _ in range(1000000)]


def sum_array_elements(array):
    return sum(array)


def sum_chunk(chunk):
    return sum(chunk)


def sum_array_elements_with_processes(array):
    start_time = time.time()

    num_processes = 4
    chunk_size = len(array) // num_processes
    chunks = [array[i:i+chunk_size] for i in range(0, len(array), chunk_size)]

    with multiprocessing.Pool() as pool:
        results = pool.map(sum_chunk, chunks)
        total_sum = sum(results)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Сумма элементов массива с использованием многопроцессорности: {total_sum}")
    print(f"Время вычислений: {execution_time}")


def main():
    array = create_random_array()
    sum_array_elements_with_processes(array)


if __name__ == '__main__':
    main()
