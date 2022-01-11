import matplotlib.pyplot as plt
from database import DatabaseExecutes
from config import NICKNAMES
import numpy as np
import os


def make_graph(database_executor, nickname, filename):
    dates = database_executor.select_from_database('date', nickname)
    ranks = database_executor.select_from_database('rank', nickname)

    # SELECT date FROM tabela;
    # plotting the points

    segregated_ranks = ['PLATINUM IV', 'PLATINUM III', 'PLATINUM II', 'PLATINUM I', 'DIAMOND IV',
                        'DIAMOND III', 'DIAMOND II', 'DIAMOND I', 'MASTER I']
    # seen_ranks = []
    # for r in segregated_ranks:
    #     if r in ranks:
    #         seen_ranks.append(r)
    seen_ranks = [r for r in segregated_ranks if r in ranks]
    # index_by_seen_ranks = {}
    # for i, r in enumerate(seen_ranks):
    #       index_by_seen_ranks[r] = i
    plt.xticks(rotation=45)
    index_by_seen_ranks = {r: i for i, r in enumerate(seen_ranks)}
    plot_sorted_ranks = [index_by_seen_ranks[r] for r in ranks]
    plt.plot(dates, plot_sorted_ranks)
    plt.yticks(range(len(seen_ranks)), seen_ranks)

    print(f'{seen_ranks=}')
    print(f'{index_by_seen_ranks=}')
    print(f'{ranks=}')
    print(f'{plot_sorted_ranks=}')

# naming the x axis
    plt.xlabel('DATE')
    # naming the y axis
    plt.ylabel('RANK')

    # giving a title to my graph
    plt.title(nickname)

    # function to show the plot
    # plt.show()
    # ax = plt.gca()
    # ax.set_ylim(ax.get_ylim()[::-1])
    # function to save as file
    plt.savefig(f'graphs\\{filename}.png', bbox_inches='tight')

    plt.clf()


def portable_execute_func():
    database_executor = DatabaseExecutes(os.path.join("tft_database.sqlite"))
    for nickname in NICKNAMES:
        make_graph(database_executor, nickname, nickname)


def main():
    database_executor = DatabaseExecutes(os.path.join("tft_database.sqlite"))
    for nickname in NICKNAMES:
        make_graph(database_executor, nickname, nickname)


if __name__ == '__main__':
    main()
