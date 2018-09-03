def test_monoid(set_strategy, binary_operation, identity_element):
    from hypothesis import given

    @given(set_strategy)
    def test_monoid_identity(a):
        '''e * a == a == a * e'''

        assert binary_operation(identity_element, a) == a
        assert binary_operation(a, identity_element) == a

    @given(set_strategy, set_strategy, set_strategy)
    def test_monoid_associativity(a, b, c):
        '''(a * b) * c == a * (b * c)'''

        d = binary_operation(binary_operation(a, b), c)
        e = binary_operation(a, binary_operation(b, c))
        assert d == e

    test_monoid_identity()
    test_monoid_associativity()


def reverse_add(a, b):
    return b + a


def implies(a, b):
    return (not a) or b


def main():
    import hypothesis.strategies as st
    import operator as op

    # examples

    test_monoid(st.text(), op.add, "")
    test_monoid(st.lists(st.booleans()), op.add, [])
    test_monoid(st.lists(st.booleans()), reverse_add, [])
    test_monoid(st.booleans(), op.__and__, True)
    test_monoid(st.booleans(), op.__or__, False)
    test_monoid(st.booleans(), op.__xor__, False)
    test_monoid(st.integers(), op.add, 0)
    test_monoid(st.integers(), op.mul, 1)

    # counterexamples

    #test_monoid(st.booleans(), implies, False)
    #test_monoid(st.booleans(), implies, True)
    #test_monoid(st.integers(), op.sub, 0)
    #test_monoid(st.integers(), op.div, 1)
    #test_monoid(st.floats(), op.add, 0)
    #test_monoid(st.floats(), op.mul, 1)


if __name__ == '__main__':
    main()
