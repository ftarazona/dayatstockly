""" Fox and Names

Purpose of the exercise is to find, if possible, an ordering so that a list of 
names in input is sorted lexicographically.

An obvious but very naive solution would be to test every possible ordering of
the latin alphabet. Simply enough to implement, but really non conceivable in
complexity.

The first example from CodeForces gives the following ordered list:
 rivest
 shimar
 adleman
A possible result is 'bcdefghijklmnopqrsatuvwxyz'. Some hints at this first
example:
 - only the first letters are necessary. 
 - any ordering of the alphabet where 'r' < 's' < 'a' would be possible

So it may be a good thing to think of the algorithm as advancing letter by
letter.

An iteration invariant is that the list must remain sorted according to the
solution used.

The second example is interesting for understanding the "impossible" case: the
list contains two non adjacent words having the same letter 't' at beginning.
Obviously, if two words start with the same letter, they must be adjacent.

This hints at a recursive algorithm. Maybe backpropagation with constraints.

First letters give constraints, then if two adjacent words had the same first
letter, they lead to other constraints or impossibility, and so on.
When no more ambiguous case (adjacent words with same first letter) is found,
then we have the constraints, and we can fill the rest with random ordering.

The solutions to examples seem to be generated from the usual ordering of the
alphabet (you can notice good ordering at some points). This could be another
approach. Let's integrate this.

We can start from the usual order, then constraints are simply swaps between
some letters. And we do it recursively.
But how do we deal with such a case:
 car
 ccr
 ae
We must recall the first constraint 'c' < 'a' so that we can tell at the second
level (car/ccr) that there is an impossibility.

Starting from a fully ordered alphabet seems to me not to be a easier way.
"""

import itertools

def read_input():
    n = int(input())
    names = [input() for _ in range(n)]
    return names

def check_empty_suffixes(words):
    """Check that any empty word is at the beginning of the list"""
    encountered_non_empty = False
    for word in words:
        if encountered_non_empty and len(word) <= 1:
            return False
        if len(word) > 1:
            encountered_non_empty = True
    return True

def generate_constraints(names):
    """Generate the constraints as described above. The constraints are tuples
    like (a, b) meaning that a must be before b in the final ordering.
    The function also returns the set of constraint letters."""
    constraints = set()
    letters = set()

    lists = [names]

    while len(lists) > 0:
        names = lists.pop()
        order = [name[0] for name in names]
        for i in range(len(order) - 1):
            inf, sup = order[i], order[i + 1]
            if inf != sup:
                constraints.add((inf, sup))
                letters.add(inf)
                letters.add(sup)

        # See https://docs.python.org/3/library/itertools.html#itertools.groupby
        # for more information on itertools.grouby
        groups = [list(g) for _, g in itertools.groupby(names, key=lambda word: word[0])]
        for g in groups:
            if len(g) > 1:
                if not check_empty_suffixes(g):
                    return None
                g = [word[1:] for word in g if len(word) > 1]
                lists.append(g)

    return constraints, letters


def no_incoming_edge(node, edges):
    for edge in edges:
        if edge[1] == node:
            return False
    return True

def generate_ordering(edges, nodes):
    """Using a graph then topological sort for finding out a possible ordering
    if possible.
    Could not remember the algorithm, so used the thread below:
    https://stackoverflow.com/questions/4168/graph-serialization/4577#4577"""

    L = []
    Q = set([node for node in nodes if no_incoming_edge(node, edges)])

    while len(Q) > 0:
        n = Q.pop()
        L.append(n)
        for m in nodes:
            if (n, m) in edges:
                edges.discard((n, m))
                if no_incoming_edge(m, edges):
                    Q.add(m)

    if len(edges) > 0:
        return None
    else:
        return L
    

if __name__ == "__main__":
    names = read_input()

    result = generate_constraints(names)
    if result is None:
        print('Impossible')
    else:
        constraints, nodes = result

        ordering = generate_ordering(constraints, nodes)

        if ordering is None:
            print('Impossible')
        else:
            alphabet = set(list('abcdefghijklmnopqrstuvwxyz'))
            alphabet -= set(ordering)
            ordering = ''.join(list(alphabet) + ordering)
            print(ordering)