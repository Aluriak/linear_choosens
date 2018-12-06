"""Application of the linear choosens algorithm:
Bollobas et al., Directed scale-free graphs.


Objectif:

Idea is to generate a random graph knowing the number of nodes, using the following constraint:
- the number of edges is roughtly equal to (3/2) * nb_node ** (3/2)


Implementations:

The basic implementation is, knowing |V|, computing the number of edges |E|,
and then choose E elements in the permutation of 2 elements in the list of node id.

The "stdlib" method use itertools to generate the permutation, and random.sample
for get a subset of generated pairs.

The "linear" method avoid a full memory load, by using the linear choosen
implementation found in this repo.


Results:

The stdlib method require more than 4GB of memory when |V| == 10000,
where the linear method runs smoothly without needing more than the space
needed to store the final graph.

However, the linear method is obviously slower.


For |V| == 1000, both methods works, but timeit show an obvious performance gain
in favor of the stdlib method.

For |V| <= 100, stdlib method is faster.

|V|:  100, |E|:   1500, stdlib_method: 0.013s
|V|:  100, |E|:   1500, linear_method: 0.022s
|V|: 1000, |E|:  47434, stdlib_method: 0.657s
|V|: 1000, |E|:  47434, linear_method: 2.166s
|V|: 2000, |E|: 134164, stdlib_method: 2.334s
|V|: 2000, |E|: 134164, linear_method: 8.522s



"""


import timeit
from itertools import permutations
from random import sample
from linear_choosens import choice_linear
from functools import partial


def edge_number(node_number:int) -> int:
    return round((3/2) * node_number ** (3/2))


def stdlib_method(nb_node:int, nb_edge:int):
    edges = permutations(range(nb_node), 2)
    return sample(tuple(edges), nb_edge)


def linear_method(nb_node:int, nb_edge:int):
    edges = permutations(range(nb_node), 2)
    permutation_size = nb_node * (nb_node-1)
    return tuple(choice_linear(nb_edge, it=edges, it_size=permutation_size))


if __name__ == '__main__':
    for n in (100, 1000, 2000):
        edge_count = edge_number(n)
        for method in (stdlib_method, linear_method):
            func = partial(method, n, edge_count)
            print("|V|: {}, |E|: {}, {}: {}s".format(
                str(n).rjust(4), str(len(func())).rjust(6), method.__name__,
                str(round(timeit.timeit(func, number=4), 3)).ljust(5),
            ))
