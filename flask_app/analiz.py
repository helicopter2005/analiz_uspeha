import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_data(path):
    data = pd.read_excel(path)

    tests_count = sum(1 for col in data.columns if "Вопрос" in col)
    data_tests = data.iloc[:-1, :tests_count+1]

    data_practices = pd.DataFrame(data['Имя Студента'])
    data_practices = data_practices.join(data.iloc[:-1, tests_count+1:])
    return data_tests, data_practices

def cr_test_zero_count(path):
    data_tests, data_practices = create_data(path)
    test_zero_count = list()
    for ind, col in enumerate(data_tests.columns[1:]):
        test_zero_count.append((ind + 1, len(data_tests[data_tests[col] == 0])))
    test_zero_count.sort(key=lambda x: x[1])
    return data_tests, data_practices, test_zero_count


def cr_practice_zero_count(path):
    data_tests, data_practices = create_data(path)
    practice_zero_count = list()
    for ind, col in enumerate(data_practices.columns[1:]):
        practice_zero_count.append((ind + 1, len(data_practices[data_practices[col] == 0])))
    practice_zero_count.sort(key=lambda x: x[1])
    return data_tests, data_practices, practice_zero_count


def test_zero_count_hist(path):
    data_tests, data_practices, test_zero_count = cr_test_zero_count(path)
    if test_zero_count:
        fig, ax = plt.subplots(figsize=(10, 10), facecolor='white', dpi=80)
        ax.vlines(x=range(1, len(data_tests.columns)), ymin=0, ymax=[x[1] for x in test_zero_count], color='firebrick',
                  alpha=0.7, linewidth=25)
        for i, test in enumerate(test_zero_count):
            ax.text(i + 1, test[1] + 0.5, test[1], horizontalalignment='center')
        ax.set_title('Тестовая часть', fontdict={'size': 22})
        ax.set(ylabel='Количество студентов, которые не смогли ответить на вопрос', ylim=(0, 30))
        plt.xticks(range(1, len(data_tests.columns)), ['Вопрос ' + str(x[0]) for x in test_zero_count], rotation=60,
                   horizontalalignment='right', fontsize=12)
    return plt


def practice_zero_count_hist(path):
    data_tests, data_practices, practice_zero_count = cr_practice_zero_count(path)
    if practice_zero_count:
        fig, ax = plt.subplots(figsize=(10, 10), facecolor='white', dpi=80)
        ax.vlines(x=range(1, len(data_practices.columns)), ymin=0, ymax=[x[1] for x in practice_zero_count],
                  color='firebrick', alpha=0.7, linewidth=25)

        ax.set_title('Практическая часть', fontdict={'size': 22})
        ax.set(ylabel='Количество студентов, которые не смогли решить задачу', ylim=(0, 30))

        for i, test in enumerate(practice_zero_count):
            ax.text(i + 1, test[1] + 0.5, test[1], horizontalalignment='center')
        plt.xticks(range(1, len(data_practices.columns)), ['Вопрос ' + str(x[0]) for x in practice_zero_count], rotation=60,
                   horizontalalignment='right', fontsize=12)
    return plt

def test_zero_count_diag(path):
    data_tests, data_practices, test_zero_count = cr_test_zero_count(path)

    if test_zero_count:
        fig = plt.figure(figsize=(10, 10), dpi=80)
        ax = fig.add_subplot()
        ax.set_title('% студентов, которые не решили тестовые вопросы', fontdict={'size': 22})
        ax.pie([x[1] for x in test_zero_count], labels=['Вопрос ' + str(x[0]) for x in test_zero_count], autopct='%.2f',
               shadow=True, explode=[0] * (len(data_tests.columns[1:]) - 2) + [.1, .2])
    return plt


def practice_zero_count_diag(path):
    data_tests, data_practices, practice_zero_count = cr_practice_zero_count(path)

    if practice_zero_count:
        fig = plt.figure(figsize=(10, 10), dpi=80)
        ax = fig.add_subplot()
        ax.set_title('% студентов, которые не решили практические задачи', fontdict={'size': 22})
        ax.pie([x[1] for x in practice_zero_count], labels=['Вопрос ' + str(x[0]) for x in practice_zero_count],
               autopct='%.2f', shadow=True, explode=[0] * (len(data_practices.columns[1:]) - 2) + [.1, .2])
    return plt

