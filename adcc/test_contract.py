#!/usr/bin/env python3
## vi: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
## ---------------------------------------------------------------------
##
## Copyright (C) 2019 by the adcc authors
##
## This file is part of adcc.
##
## adcc is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## adcc is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with adcc. If not, see <http://www.gnu.org/licenses/>.
##
## ---------------------------------------------------------------------
import unittest
import numpy as np

from numpy.testing import assert_allclose

from adcc import contract, empty_like, nosym_like
from adcc.testdata.cache import cache

# Note: The tuples "in C++" refer to the (N_CONTR_IDCS, DIMA, DIMB)
#       tuple in the IF_DIMENSIONS_MATCH_EXECUTE preprocessor macro
#       of the TensorImpl::contract_to function in adccore.

class TestContract(unittest.TestCase):
    def base_test(self, contr, a, b, out):
        a.set_random()
        b.set_random()
        out.set_random()

        ref = np.einsum(contr, a.to_ndarray(), b.to_ndarray())
        contract(contr, a, b, out)
        assert_allclose(out.to_ndarray(), ref, rtol=1e-10, atol=1e-14)

        out2 = contract(contr, a, b)
        assert_allclose(out2.to_ndarray(), ref, rtol=1e-10, atol=1e-14)

    def test_contract_1_2_1_ij(self):  # (1,1,2) in C++
        refstate = cache.refstate["h2o_sto3g"]
        a = nosym_like(refstate.orbital_energies("o1"))
        b = nosym_like(refstate.fock("o1v1"))
        out = nosym_like(refstate.orbital_energies("v1"))
        self.base_test("i,ij->j", a, b, out)

    def test_contract_1_2_1_ji(self):  # (1,1,2) in C++
        refstate = cache.refstate["h2o_sto3g"]
        a = nosym_like(refstate.orbital_energies("o1"))
        b = nosym_like(refstate.fock("v1o1"))
        out = nosym_like(refstate.orbital_energies("v1"))
        self.base_test("i,ji->j", a, b, out)

    def test_contract_2_1_1(self):  # (1,2,1) in C++
        refstate = cache.refstate["h2o_sto3g"]
        a = empty_like(refstate.fock("o1v1"))
        b = empty_like(refstate.orbital_energies("v1"))
        out = nosym_like(refstate.orbital_energies("o1"))
        self.base_test("ij,j->i", a, b, out)

    def test_contract_2_2_2(self):  # (1, 2, 2) in C++
        refstate = cache.refstate["h2o_sto3g"]
        a = nosym_like(refstate.fock("o1v1"))
        b = nosym_like(refstate.fock("v1v1"))
        out = nosym_like(refstate.fock("o1v1"))
        self.base_test("ij,jk->ik", a, b, out)

    def test_contract_2_4_4(self):  # (1, 2, 4) in C++
        refstate = cache.refstate["h2o_sto3g"]
        a = empty_like(refstate.fock("o1o1"))
        b = empty_like(refstate.eri("o1v1o1v1"))
        out = nosym_like(refstate.eri("o1o1v1v1"))
        self.base_test("ij,iklm->jlkm", a, b, out)

    def test_contract_2_4_2(self):  # (2, 2, 4) in C++
        refstate = cache.refstate["h2o_sto3g"]
        a = empty_like(refstate.fock("o1o1"))
        b = empty_like(refstate.eri("o1v1o1v1"))
        out = nosym_like(refstate.fock("v1v1"))
        self.base_test("ij,ikjl->kl", a, b, out)

    def test_contract_4_2_4(self):  # (1, 4, 2) in C++
        refstate = cache.refstate["cn_sto3g"]
        a = empty_like(refstate.eri("o1o1v1v1"))
        b = empty_like(refstate.fock("v1v1"))
        out = nosym_like(refstate.eri("o1v1o1v1"))
        self.base_test("ijkl,km->iljm", a, b, out)

    def test_contract_4_2_4_perm(self):  # (1, 4, 2) in C++
        refstate = cache.refstate["cn_sto3g"]
        a = empty_like(refstate.eri("o1o1v1v1"))
        b = empty_like(refstate.fock("v1v1"))
        out = nosym_like(refstate.eri("o1v1o1v1"))
        self.base_test("ijkl,km->imjl", a, b, out)
        #               oovv vv  ovov

    def test_contract_4_2_2(self):  # (2, 4, 2) in C++
        refstate = cache.refstate["cn_sto3g"]
        a = empty_like(refstate.eri("o1o1v1v1"))
        b = empty_like(refstate.fock("o1v1"))
        out = nosym_like(refstate.fock("v1o1"))
        self.base_test("ijkl,jk->li", a, b, out)

    def test_contract_4_4_4_oipj(self):  # (2, 4, 4) in C++
        refstate = cache.refstate["cn_sto3g"]
        a = empty_like(refstate.eri("o1o1v1v1"))
        b = empty_like(refstate.eri("v1v1v1v1"))
        out = nosym_like(refstate.eri("o1v1o1v1"))
        self.base_test("opvw,vijw->oipj", a, b, out)

    def test_contract_4_4_4_ojpi(self):  # (2, 4, 4) in C++
        refstate = cache.refstate["cn_sto3g"]
        a = empty_like(refstate.eri("o1o1v1v1"))
        b = empty_like(refstate.eri("v1v1v1v1"))
        out = nosym_like(refstate.eri("o1v1o1v1"))
        self.base_test("opvw,vijw->ojpi", a, b, out)

    def test_contract_4_4_4_pjoi(self):  # (2, 4, 4) in C++
        refstate = cache.refstate["cn_sto3g"]
        a = empty_like(refstate.eri("o1o1v1v1"))
        b = empty_like(refstate.eri("v1v1v1v1"))
        out = nosym_like(refstate.eri("o1v1o1v1"))
        self.base_test("opvw,vijw->pjoi", a, b, out)

    def test_contract_4_4_2(self):  # (3, 4, 4) in C++
        refstate = cache.refstate["cn_sto3g"]
        a = empty_like(refstate.eri("o1v1o1v1"))
        b = empty_like(refstate.eri("o1o1o1v1"))
        out = nosym_like(refstate.fock("o1v1"))
        self.base_test("iajb,jikb->ka", a, b, out)