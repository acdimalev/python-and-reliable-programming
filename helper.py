def function(returns):
    '''A simple function strategy for Hypothesis.

    based on
    https://github.com/jsverify/jsverify/blob/v0.8.3/lib/fn.js#L18

    to be succeeded by
    https://github.com/HypothesisWorks/hypothesis/issues/167
    '''
    from frozendict import frozendict
    from hypothesis.strategies import builds, from_type, just

    def new_function():
        d = {}

        def f(*args, **kwargs):
            key = (args, frozendict(kwargs))
            if key not in d:
                d[key] = from_type(returns).example()
            return d[key]
        return f
    return builds(new_function)
