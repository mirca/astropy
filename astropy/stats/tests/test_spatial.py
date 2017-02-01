from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np

from numpy.testing.utils import assert_allclose
from ..spatial import RipleysKEstimator
from ...utils.misc import NumpyRNGContext

def test_ripley_K_implementation():
    """
    Test against Ripley's K function implemented in R package `spatstat`
        +-+---------+---------+----------+---------+-+
      6 +                                          * +
        |                                            |
        |                                            |
    5.5 +                                            +
        |                                            |
        |                                            |
      5 +                     *                      +
        |                                            |
    4.5 +                                            +
        |                                            |
        |                                            |
      4 + *                                          +
        +-+---------+---------+----------+---------+-+
          1        1.5        2         2.5        3
    """
    a = np.array([[1, 4], [2, 5], [3, 6]])
    area = 100
    r = np.linspace(0, 2.5, 5)
    Kest = RipleysKEstimator(area=area, x_max=10, y_max=10)

    ANS_NONE = np.array([0, 0, 0, 66.667, 66.667])
    assert_allclose(ANS_NONE, Kest(data=a, radii=r, mode='none'), atol=1e-3)

    ANS_TRANS = np.array([0, 0, 0, 82.304, 82.304])
    assert_allclose(ANS_TRANS, Kest(data=a, radii=r, mode='translation'), atol=1e-3)

def test_ripley_uniform_property():
    # Ripley's K function without edge-correction converges to the area when
    # the number of points and the argument radii are large enough, i.e.,
    # K(x) --> area as x --> inf
    with NumpyRNGContext(123):
        z = np.random.uniform(low=5, high=10, size=(100, 2))

        area = 50
        Kest = RipleysKEstimator(area=area)
        r = np.linspace(0, 20, 5)
        assert_allclose(area, Kest(data=z, radii=r, mode='none')[4])

def test_ripley_large_density():
    with NumpyRNGContext(123):
        z = np.random.uniform(low=0, high=1, size=(500, 2))

        Kest = RipleysKEstimator(area=1, x_max=1, y_max=1, lratio=1)
        r = np.linspace(0, 0.25, 25)

        assert_allclose(Kest.poisson(r),
                        Kest(data=z, radii=r, mode='ohser'), atol=1e-2)
        assert_allclose(Kest.poisson(r),
                        Kest(data=z, radii=r, mode='var-width'), atol=1e-2)
        assert_allclose(Kest.poisson(r),
                        Kest(data=z, radii=r, mode='translation'), atol=1e-2)
        assert_allclose(Kest.poisson(r),
                        Kest(data=z, radii=r, mode='ripley'), atol=1e-2)

def test_ripley_modes():
    with NumpyRNGContext(123):
        z = np.random.uniform(low=5, high=10, size=(500, 2))

        Kest = RipleysKEstimator(area=25, x_max=10, y_max=10, lratio=1, x_min=5, y_min=5)
        r = np.linspace(0, 1.2, 25)

        assert_allclose(Kest.poisson(r),
                        Kest(data=z, radii=r, mode='ohser'), atol=1e-1)
        assert_allclose(Kest.poisson(r),
                        Kest(data=z, radii=r, mode='var-width'), atol=1e-1)
        assert_allclose(Kest.poisson(r),
                        Kest(data=z, radii=r, mode='translation'), atol=1e-1)
        assert_allclose(Kest.poisson(r),
                        Kest(data=z, radii=r, mode='ripley'), atol=1e-1)
