import unittest
import sys
import os
import numpy as np
from SparseComputation import ApproximatePCA
from SparseComputation import PCA


class TestApproximatePCA(unittest.TestCase):

    def setUp(self):
        self.ap = ApproximatePCA(3, 0.01, 1, 100, 150)
        self.small_ap = ApproximatePCA(2, 0.01, 0.01, 2, 3)
        data = []
        for i in range(5):
            elt = []
            for j in range(1, 6):
                elt.append(5*i+j)
            data.append(elt)
        self._data = np.array(data)
        self._row_proba = np.array([0.0099547511312217188, 0.05972850678733032,
                                   0.15475113122171946, 0.29502262443438915,
                                   0.48054298642533938])
        self._col_proba = np.array([0.15475113, 0.17556561, 0.19819005,
                                   0.22262443, 0.24886878])
        self._seed = 10
        factor = np.sqrt(self._col_proba[[4, 0, 3]]*3.0)
        self._col_reduced_data = np.array([[5,  1,  4], [10,  6,  9],
                                          [15, 11, 14], [20, 16, 19],
                                          [25, 21, 24]])/factor

        self._row_reduced_data = np.array([[25, 21, 24], [20, 16, 19]])
        self._pca = np.array([[ 3.90947025e+01,   0.00000000e+00],
                              [ 2.79247875e+01,  -8.88178420e-16],
                              [ 1.67548725e+01,   8.88178420e-16],
                              [ 5.58495750e+00,   2.22044605e-15],
                              [-5.58495750e+00,   1.33226763e-15]])

    def test_approx_pca_init(self):
        self.assertEqual(self.ap.dimLow, 3)
        self.assertEqual(self.ap.fracRow, 0.01)
        self.assertEqual(self.ap.fracCol, 1)
        self.assertEqual(self.ap.minRow, 100)
        self.assertEqual(self.ap.minCol, 150)

    def test_proba_col(self):
        data = np.array([[1, 2], [3, 4]])
        exp_result = np.array([10.0/30, 20.0/30])
        result = np.array(self.ap._get_proba_col(data))
        np.testing.assert_array_almost_equal(exp_result, result)
        result = np.array(self.small_ap._get_proba_col(self._data))
        exp_result = self._col_proba
        np.testing.assert_array_almost_equal(exp_result, result)

    def test_proba_col(self):
        data = np.array([[1, 2], [3, 4]])
        exp_result = np.array([5.0/30, 25.0/30])
        result = np.array(self.ap._get_proba_row(data))
        np.testing.assert_array_almost_equal(exp_result, result)
        result = np.array(self.small_ap._get_proba_row(self._data))
        exp_result = self._row_proba
        np.testing.assert_array_almost_equal(exp_result, result)

    def test_col_reduction(self):
        np.random.seed(self._seed)
        result = self.small_ap._col_reduction(self._data)
        exp_result = self._col_reduced_data
        np.testing.assert_array_almost_equal(exp_result, result)

    def test_row_reduction(self):
        np.random.seed(self._seed)
        rand_select = self.small_ap._col_reduction(self._data)
        data = np.array([[5,  1,  4], [10,  6,  9],
                         [15, 11, 14], [20, 16, 19],
                         [25, 21, 24]])
        result = np.array(self.small_ap._row_reduction(data))
        exp_result = self._row_reduced_data
        np.testing.assert_array_almost_equal(exp_result, result)

    def test_approx_pca_fit_transform_small_dim(self):
        exp_pca = self._pca
        np.random.seed(self._seed)
        pca_res = self.small_ap.fit_transform(self._data)
        np.testing.assert_array_almost_equal(exp_pca, pca_res)
