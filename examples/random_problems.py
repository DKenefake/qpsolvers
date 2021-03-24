#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2020 Stephane Caron <stephane.caron@normalesup.org>
#
# This file is part of qpsolvers.
#
# qpsolvers is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# qpsolvers is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with qpsolvers. If not, see <http://www.gnu.org/licenses/>.

"""
Test all available QP solvers on random quadratic programs.
"""

import sys

try:
    from IPython import get_ipython
except ImportError:
    print("This example requires IPython, try installing ipython3")
    sys.exit(-1)

from numpy import dot, ones, random
from os.path import basename
from scipy.linalg import toeplitz
from timeit import timeit

from qpsolvers import available_solvers, solve_qp

colors = {
    'cvxopt': 'r',
    'cvxpy': 'c',
    'ecos': 'c',
    'gurobi': 'b',
    'mosek': 'g',
    'osqp': 'k',
    'qpoases': 'y',
    'quadprog': 'm'}

nb_iter = 10
sizes = [10, 20, 50, 100, 200, 500, 1000, 2000]


def solve_random_qp(n, solver):
    M, b = random.random((n, n)), random.random(n)
    P, q = dot(M.T, M), dot(b, M).reshape((n,))
    G = toeplitz([1., 0., 0.] + [0.] * (n - 3), [1., 2., 3.] + [0.] * (n - 3))
    h = ones(n)
    return solve_qp(P, q, G, h, solver=solver)


def plot_results(perfs):
    try:
        from pylab import clf, grid, ion, legend, plot, xscale, yscale
    except ImportError:
        print("Cannot plot results, try installing python3-matplotlib")
        print("Results are stored in the global `perfs` dictionary")
        return
    ion()
    clf()
    for solver in perfs:
        plot(sizes, perfs[solver], lw=2, color=colors[solver])
    grid(True)
    legend(list(perfs.keys()), loc='lower right')
    xscale('log')
    yscale('log')
    for solver in perfs:
        plot(sizes, perfs[solver], marker='o', color=colors[solver])


if __name__ == "__main__":
    if get_ipython() is None:
        print("Usage: ipython -i %s" % basename(__file__))
        exit()
    perfs = {}
    print("\nTesting all QP solvers on a random quadratic programs...\n")
    for solver in available_solvers:
        try:
            perfs[solver] = []
            for size in sizes:
                print("Running %s on problem size %d..." % (solver, size))
                cum_time = timeit(
                    stmt="solve_random_qp(%d, '%s')" % (size, solver),
                    setup="from __main__ import solve_random_qp",
                    number=nb_iter)
                perfs[solver].append(cum_time / nb_iter)
        except Exception as e:
            print("Warning: %s" % str(e))
            if solver in perfs:
                del perfs[solver]
    plot_results(perfs)
