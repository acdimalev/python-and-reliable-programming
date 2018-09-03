from unittest import TestCase
import hypothesis.strategies as st
import operator as op


def assert_monoid(set_strategy, binary_operation, identity_element):
    from hypothesis import given

    @given(set_strategy)
    def assert_monoid_identity(a):
        '''e * a == a == a * e'''

        assert a == binary_operation(identity_element, a)
        assert a == binary_operation(a, identity_element)

    @given(set_strategy, set_strategy, set_strategy)
    def assert_monoid_associativity(a, b, c):
        '''(a * b) * c == a * (b * c)'''

        assert op.eq(
            binary_operation(binary_operation(a, b), c),
            binary_operation(a, binary_operation(b, c)),
        )

    assert_monoid_identity()
    assert_monoid_associativity()


class TestMonoidExamples(TestCase):

    def test_string_concatenation(self):
        assert_monoid(st.text(), op.add, "")

    def test_list_concatenation(self):
        assert_monoid(st.lists(st.booleans()), op.add, [])

    def test_list_reverse_concatenation(self):
        def radd(x, y): return y + x
        assert_monoid(st.lists(st.booleans()), radd, [])

    def test_boolean_conjunction(self):
        assert_monoid(st.booleans(), op.__and__, True)

    def test_boolean_disjunction(self):
        assert_monoid(st.booleans(), op.__or__, False)

    def test_boolean_exclusive_disjunction(self):
        assert_monoid(st.booleans(), op.__xor__, False)

    def test_integer_addition(self):
        assert_monoid(st.integers(), op.add, 0)

    def test_integer_multiplication(self):
        assert_monoid(st.integers(), op.mul, 1)


class TestMonoidCounterexamples(TestCase):

    def test_boolean_implication(self):
        def implies(a, b): return (not a) or b
        with self.assertRaises(Exception):
            assert_monoid(st.booleans(), implies, False),
        with self.assertRaises(Exception):
            assert_monoid(st.booleans(), implies, True),

    def test_integer_subtraction(self):
        with self.assertRaises(Exception):
            assert_monoid(st.integers(), op.sub, 0)

    def test_integer_division(self):
        with self.assertRaises(Exception):
            assert_monoid(st.integers(), op.div, 0)

    def test_float_addition(self):
        with self.assertRaises(Exception):
            assert_monoid(st.floats(), op.add, 0)

    def test_float_multiplication(self):
        with self.assertRaises(Exception):
            assert_monoid(st.floats(), op.mul, 1)
