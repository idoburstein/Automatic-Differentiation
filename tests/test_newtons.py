import pytest
import src.autodiffpypi as adp
from src.autodiffpypi.forward_mode import Forward
from src.autodiffpypi.dual_number import DualNumber
from src.autodiffpypi.base_derivatives import *
from applications.newtons import newton

def test_newton_full():
    """
    Test suite for the Newton class.
    """
    allowed_error = 0.0001

    def test_newton():
        # Test for success on good guess
        init_guess = 0.1
        function = lambda x : x - adp.exp(-2.0 * adp.sin(4.0 * x) * adp.sin(4.0 * x))
        res = newton.newton(function, [init_guess], 10000)
        assert abs(res[0]  - 2.473481e-01) <= allowed_error

        # Test for failure on bad guess
        init_guess = 10
        f = lambda x : x - adp.exp(-2.0 * adp.sin(4.0 * x) * adp.sin(4.0 * x))
        res = newton.newton(f, [init_guess], 100)
        assert abs(res[0]  - 2.473481e-01) > allowed_error

        # Test for failure on bad guess
        init_guess = [0]
        with pytest.raises(TypeError):
            f = lambda x : x - adp.exp(-2.0 * adp.sin(4.0 * x) * adp.sin(4.0 * x))
            print(newton.newton(f, init_guess, max_iterations=100))

        # Test for success on good guess
        init_guess = 1
        f = lambda x : x - adp.cos(x)
        res = newton.newton(f, [init_guess], 1000)
        assert abs(res[0] - 0.7390851332151606416553) <= allowed_error

        # Test for failure on bad guess
        init_guess = 500
        f = lambda x : x - adp.cos(x)
        res = newton.newton(f, [init_guess], 200)
        assert abs(res[0]  - 0.7390851332151606416553) > allowed_error

        # Test multiple functions multiple inputs
        f2 = lambda x, y: x*y+1
        f3 = lambda x, y: 3*x+5*y-1
        f1 = lambda x, y, z: x+4*y-z
        res = newton.newton([f1, f2, f3], [0.1, 0.1, 0.1], max_iterations=200)
        assert abs(res[0] - -1.135041) <= allowed_error
        assert abs(res[1] - 0.881024) <= allowed_error
        assert abs(res[2] - 2.389058) <= allowed_error

        # Test dimension mismatch
        with pytest.raises(ValueError):
            f1 = lambda x, y: x+4*y
            print(newton.newton([f1], [1, 1], max_iterations=100))

    test_newton()


test_newton_full()
