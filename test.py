"""Test the linear_choosens module"""

import timeit
import statistics
import random
from collections import Counter, defaultdict
from operator import itemgetter
from functools import partial
from itertools import chain

from linear_choosens import choice_linear, choice_rec, choice_stdlib, choice_dumb
import plot


FIGNAME = 'results/benchmark_{}_{}_{}_{}.png'

# benchmark control
FUNCTIONS = (choice_linear, choice_dumb, choice_rec, choice_stdlib)
NB_RUNS   = (10000,)
SETS_SIZE = lambda: (
    ((n, 100)  for n in range(10, 101, 10)),
    ((n, 1000) for n in range(100, 1001, 100)),
)
TIMEIT_NB_RUN = 100

# debug values
# FUNCTIONS = (choice_linear,)
# NB_RUNS   = (10, 100,)
# SETS_SIZE = lambda: (( (10, 1000), (50, 1000), (90, 1000) ),)
# SETS_SIZE = lambda: (( (10, 1000),  ),)
# TIMEIT_NB_RUN = 1


def choice_tester(func:callable, nb_call, nb_choosen, items):
    """Wrapper around linear_choosens.choice_* functions.
    Return frequencies of all items return by nb_call call of func"""
    def found_numbers():
        """Yield numbers found by choice function, called nb times"""
        for _ in range(nb_call):
            yield from func(nb_choosen, items)
    counts = Counter(found_numbers())
    # add values with zero
    for elem in items:
        if elem not in counts:
            counts[elem] = 0
    return counts


def benchmark_all(funcs:iter, nb_runs:int, sets_size:iter):
    # timescores : {nb_items: {method: times sorted by rank}}
    timescores = defaultdict(lambda: defaultdict(list))
    meanscores = defaultdict(lambda: defaultdict(list))
    ranks = defaultdict(list)
    for nb_run in nb_runs:
        for nb_choosen, nb_items in chain.from_iterable(sets_size):
            ranks[nb_items].append(nb_choosen)
            for func in funcs:
                # prepare plot printing
                method = func.__name__[len('choice_'):]
                title = ('Search for {} in {} elements, {} times\n'
                         'using {} method needs ')
                title = title.format(nb_choosen, nb_items, nb_run, method)
                figname = FIGNAME.format(method[0], nb_choosen, nb_items, nb_run)
                timescore, _ = benchmark(
                    (func, nb_run, nb_choosen, range(nb_items)),
                    func.__name__,
                    figname,
                    title + '{} seconds ({} run)'
                )
                if timescore:
                    timescores[nb_items][func.__name__].append(float(timescore))

        fulltime = dict()
        for nb_items, scores in timescores.items():
            for method, score in scores.items():
                fulltime[method + '_' + str(nb_items)] = score
        fulltime = {**fulltime, **{'rank': ranks[nb_items]}}  # add ranks for indexing

        plot.plot_time(
            fulltime,
            show=False,
            savefile='results/runtime_{}.png'.format(nb_run),
            nb_run=TIMEIT_NB_RUN,
            nb_method=len(funcs),
        )


def benchmark(func_args:tuple, func_name:str, figname:str, title:str):
    func = partial(choice_tester, *func_args)
    _, _, _, items = func_args
    try:
        timescore = timeit.timeit(func, number=TIMEIT_NB_RUN)
        # print(func_name + ':', timescore)
        counts = func()
    except RecursionError:  # choice_rec raise it when too many numbers
        print(func_name + ': Recursive method failed (too large population)')
        return None, None
    mean = statistics.mean(counts.values())
    stdev = statistics.stdev(counts.values())
    meanscore = str(mean) + '±' + str(round(stdev, 2))
    # get results as a vector of score ; index is the item
    data = tuple(counts.get(item, 0) for item in items)
    xlabel = 'Each item is found {} times'.format(meanscore)
    plot.plots(
        data,
        title=title.format(round(timescore, 2), TIMEIT_NB_RUN),
        savefile=figname,
        xlabel=xlabel,
        show=False
    )
    return timescore, mean


if __name__ == "__main__":
    benchmark_all(funcs=FUNCTIONS, nb_runs=NB_RUNS, sets_size=SETS_SIZE())
