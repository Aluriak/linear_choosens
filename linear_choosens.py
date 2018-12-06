

import random
from random import SystemRandom
from itertools import islice


RANDOMIZER = SystemRandom()  # the slower but less biased random
RANDOMIZER = random  # the standard module basic interface


def choice_stdlib(nb_choosen:int, it:iter, it_size=None, random=RANDOMIZER):
    """Use the random.sample of stdlib"""
    return random.sample(it, nb_choosen)


def choice_dumb(nb_choosen:int, it:iter, it_size=None, random=RANDOMIZER):
    """Mix elements, then return the nb_choosen firsts"""
    # parse parameters
    if it_size is None:
        nb_elem = len(it)
    else:
        nb_elem = it_size
    assert nb_choosen <= nb_elem
    # mix the iterable
    it = list(it)
    random.shuffle(it)
    # take the firsts
    return it[:nb_choosen]


def choice_linear(nb_choosable:int, it:iter, it_size=None, random=RANDOMIZER):
    """Return a subset of iterable it, with a cardinal of n.

    Is performed in a O(|it|). For each element, the probability to found it
    in the output subset is equal to:
        (number of element in the subset) / (number of elements in it)

    for the n-th element, the probability is equivalent to:
        (number of element not already in the subset) /
        (number of non-treated elements in it)

    """
    nb_elem = len(it) if it_size is None else it_size
    if nb_choosable > nb_elem // 2:
        return set(gen_revchoice_linear(nb_elem - nb_choosable, it, nb_elem, random))
    return set(gen_choice_linear(nb_choosable, it, nb_elem, random))

def gen_choice_linear(nb_choosable:int, it:iter, it_size=None, random=RANDOMIZER):
    """Yield element of a subset of iterable it, with a cardinal of n.

    Is performed in a O(|it|). For each element, the probability to found it
    in the output subset is equal to:
        (number of element in the subset) / (number of elements in it)

    for the n-th element, the probability is equivalent to:
        (number of element not already in the subset) /
        (number of non-treated elements in it)

    """
    # parameters treatment
    nb_elem = len(it) if it_size is None else it_size
    it = iter(it)
    assert nb_choosable <= nb_elem
    random = random.random  # direct access to function
    # implementation
    for elem in islice(it, 0, nb_elem):
        likelihood = nb_choosable / nb_elem  # modified later, depending of elem
                                             # inclusion in the choosens set
        # assert 0 <= likelihood <= 1.
        if random() <= likelihood:
            yield elem
            nb_choosable -= 1
        nb_elem -= 1
        if nb_choosable == 0:  # no more element to choose
            break
        if nb_choosable == nb_elem:  # all remaining elements must be taken
            # Note that a simple 'yield from it' can't be used,
            #  since the input iterable may be a generator,
            #  and the given it_size be smaller than reality.
            yield from islice(it, 0, nb_choosable)
            break


def gen_revchoice_linear(nb_choosable:int, it:iter, it_size=None, random=RANDOMIZER):
    """Yield element that are NOT in a subset of iterable it, with a cardinal of n.

    It is basically equivalent to gen_choice_linear, but yield non-choosen
    elements instead of the choosen one.

    """
    # parameters treatment
    nb_elem = len(it) if it_size is None else it_size
    it = iter(it)
    assert nb_choosable <= nb_elem
    random = random.random  # direct access to function
    # implementation
    for elem in islice(it, 0, nb_elem):
        likelihood = nb_choosable / nb_elem  # modified later, depending of elem
                                             # inclusion in the choosens set
        if random() <= likelihood:
            nb_choosable -= 1
        else:
            yield elem
        nb_elem -= 1
        # if nb_choosable == 0:  # no more element to choose
            # NOTHING TO DO: how many elements must be yielded ?
        if nb_choosable == nb_elem:  # all remaining elements belong to the subset
            break  # ignore them all


def choice_rec(nb_choosen:int, it:iter, it_size=None, random=RANDOMIZER):
    """See choice function for explanations, and _choice_rec
    for recursive implementation that is wrapped here."""
    try:
        nb_elem = len(it)
        assert it_size is None
    except TypeError:  # generator/iterable have no len method
        assert it_size is not None
        nb_elem = it_size
    return _choice_rec(nb_choosen, iter(it), nb_elem, random=random.random)


def _choice_rec(nb_choosen:int, it:iter, it_size:int, random:callable):
    """Recursive implementation of choice function algorithm"""
    if nb_choosen == 0:
        return []
    try:
        elem = next(it)
        it_size -= 1
    except StopIteration:
        return []
    likelihood = (nb_choosen / (1+it_size))
    if random() <= likelihood:
        return [elem] + _choice_rec(nb_choosen - 1, it, it_size, random)
    else:  # don't take the elem
        return _choice_rec(nb_choosen, it, it_size, random)
