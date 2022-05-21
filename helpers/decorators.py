def cached(func):
    cache = dict()
    def cached_function(*args):
        if args in cache:
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result
    return cached_function

def cached_with_stats(stats_obj):
    def cached(func):
        cache = dict()
        def cached_function(*args):
            stats_obj['cache'] = cache
            if args in cache:
                return cache[args]
            else:
                result = func(*args)
                cache[args] = result
                return result
        return cached_function
    return cached
