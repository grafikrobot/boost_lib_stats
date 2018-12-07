"""
Copyright (c) 2017 ActiveState Software Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Additional changes, to deal with incomplete graphs are Copyright (c) 2018
Rene Rivera.
"""


def strongly_connected_components_path(vertices, edges):
    """
    Find the strongly connected components of a directed graph.
    Uses a recursive linear-time algorithm described by Gabow [1]_ to find all
    strongly connected components of a directed graph.
    Parameters
    ----------
    vertices : iterable
        A sequence or other iterable of vertices.  Each vertex should be
        hashable.
    edges : mapping
        Dictionary (or mapping) that maps each vertex v to an iterable of the
        vertices w that are linked to v by a directed edge (v, w).
    Returns
    -------
    components : iterator
        An iterator that yields sets of vertices.  Each set produced gives the
        vertices of one strongly connected component.
    Raises
    ------
    RuntimeError
        If the graph is deep enough that the algorithm exceeds Python's
        recursion limit.
    Notes
    -----
    The algorithm has running time proportional to the total number of vertices
    and edges.  It's practical to use this algorithm on graphs with hundreds of
    thousands of vertices and edges.
    The algorithm is recursive.  Deep graphs may cause Python to exceed its
    recursion limit.
    `vertices` will be iterated over exactly once, and `edges[v]` will be
    iterated over exactly once for each vertex `v`.  `edges[v]` is permitted to
    specify the same vertex multiple times, and it's permissible for `edges[v]`
    to include `v` itself.  (In graph-theoretic terms, loops and multiple edges
    are permitted.)
    References
    ----------
    .. [1] Harold N. Gabow, "Path-based depth-first search for strong and
       biconnected components," Inf. Process. Lett. 74 (2000) 107--114.
    .. [2] Robert E. Tarjan, "Depth-first search and linear graph algorithms,"
       SIAM J.Comput. 1 (2) (1972) 146--160.
    Examples
    --------
    Example from Gabow's paper [1]_.
    >>> vertices = [1, 2, 3, 4, 5, 6]
    >>> edges = {1: [2, 3], 2: [3, 4], 3: [], 4: [3, 5], 5: [2, 6], 6: [3, 4]}
    >>> for scc in strongly_connected_components_path(vertices, edges):
    ...     print(scc)
    ...
    set([3])
    set([2, 4, 5, 6])
    set([1])
    Example from Tarjan's paper [2]_.
    >>> vertices = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> edges = {1: [2], 2: [3, 8], 3: [4, 7], 4: [5],
    ...          5: [3, 6], 6: [], 7: [4, 6], 8: [1, 7]}
    >>> for scc in  strongly_connected_components_path(vertices, edges):
    ...     print(scc)
    ...
    set([6])
    set([3, 4, 5, 7])
    set([8, 1, 2])
    """
    identified = set()
    stack = []
    index = {}
    boundaries = []

    def dfs(v):
        index[v] = len(stack)
        stack.append(v)
        boundaries.append(index[v])

        if v in edges:
            for w in edges[v]:
                if w not in index:
                    # For Python >= 3.3, replace with "yield from dfs(w)"
                    for scc in dfs(w):
                        yield scc
                elif w not in identified:
                    while index[w] < boundaries[-1]:
                        boundaries.pop()

        if boundaries[-1] == index[v]:
            boundaries.pop()
            scc = set(stack[index[v]:])
            del stack[index[v]:]
            identified.update(scc)
            yield scc

    for v in vertices:
        if v not in index:
            # For Python >= 3.3, replace with "yield from dfs(v)"
            for scc in dfs(v):
                yield scc
