def function(returns):
    '''A simple function strategy for Hypothesis.'''
    from frozendict import frozendict
    from hypothesis.strategies import builds, from_type, just
    def new_function():
        d = {}
        def f(*args, **kwargs):
            key = (args, frozendict(kwargs))
            if not key in d:
                d[key] = from_type(returns).example()
            return d[key]
        return f
    return builds(new_function)
