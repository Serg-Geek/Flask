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
import threading
import asyncio


def create_random_array():
    return [random.randint(1, 100) for _ in range(1000000)]


def sum_array_elements(array):
    return sum(array)


def sum_array_elements_with_threads(array):
    start_time = time.time()

    num_threads = 4
    chunk_size = len(array) // num_threads
    chunks = [array[i:i+chunk_size] for i in range(0, len(array), chunk_size)]

    results = []

    def sum_chunk(chunk):
        result = sum(chunk)
        results.append(result)

    threads = []

    for chunk in chunks:
        t = threading.Thread(target=sum_chunk, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_sum = sum(results)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Сумма элементов массива с использованием многопоточности: {total_sum}")
    print(f"Время вычислений: {execution_time}")


async def sum_array_elements_with_asyncio(array):
    start_time = time.time()

    chunk_size = len(array) // 4
    chunks = [array[i:i+chunk_size] for i in range(0, len(array), chunk_size)]

    results = []

    async def sum_chunk(chunk):
        result = sum(chunk)
        results.append(result)

    tasks = []

    for chunk in chunks:
        task = asyncio.create_task(sum_chunk(chunk))
        tasks.append(task)

    await asyncio.gather(*tasks)

    total_sum = sum(results)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Сумма элементов массива с использованием асинхронности: {total_sum}")
    print(f"Время вычислений: {execution_time}")


def main():
    array = create_random_array()

    # Вычисление суммы с использованием многопоточности
    sum_array_elements_with_threads(array)

    # Вычисление суммы с использованием асинхронности
    asyncio.run(sum_array_elements_with_asyncio(array))


if __name__ == '__main__':
    main()
