from unittest import TestCase
import hypothesis.strategies as st
import operator as op

from helper import function


def assert_functor(set_strategy, functor_map):
    from hypothesis import given

    @given(set_strategy)
    def assert_functor_identity(F_x):
        '''F(id) = id

        assuming a simple identity function
        for all values
        '''
        def identity(x): return x
        assert identity(F_x) == functor_map(identity)(F_x)

    @given(
        function(st.integers()),
        function(st.integers()),
        set_strategy,
    )
    def assert_functor_composition(g, f, F_x):
        '''F(g . f) == F(g) . F(f)

        assuming the domain of F has an object mapping
        for arbitrary (Python) objects
        '''
        assert op.eq(
            functor_map(lambda x: g(f(x)))(F_x),
            functor_map(g)(functor_map(f)(F_x)),
        )

    assert_functor_identity()
    assert_functor_composition()


class TestFunctorExamples(TestCase):

    def test_list_map(self):
        def list_map(f):
            return lambda x: list(map(f, list(x)))
        assert_functor(st.lists(st.integers()), list_map)


class TestFunctorCounterexamples(TestCase):

    def test_map(self):
        with self.assertRaises(Exception):
            assert_functor(st.lists(st.integers()), map)

    def test_fixed_function_map(self):
        def fixed_function_map(f):
            return lambda x: 1 + x
        with self.assertRaises(Exception):
            assert_functor(st.integers(), fixed_function_map)
