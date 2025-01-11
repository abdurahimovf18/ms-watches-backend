"""
This module provides utilities for caching methods and functions throughout the codebase.

It enables caching of specific methods or functions, such as those related to models, model services, 
or other parts of the application. By utilizing these caching utilities, you can improve performance 
by reducing redundant calculations or database queries, storing results for reuse in subsequent calls.

The utilities in this module help avoid circular import issues by providing a central place for caching 
logic, ensuring that the caching mechanism is decoupled from the actual database services. This allows 
you to apply caching without introducing dependencies on actual database operations, reducing the risk 
of circular imports.

Additionally, the caching utilities support the principle of "Don't Repeat Yourself" (DRY), enabling 
you to efficiently reuse cached results, improving both performance and maintainability. By centralizing 
the caching logic, this module ensures that caching can be applied consistently across various parts of 
the application without needing to duplicate code or rely on complex import dependencies.
"""

from functools import wraps
import hashlib


def cache(func):
    _cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = generate_cache_key(func, args, kwargs)
        
        if key in _cache:
            return _cache[key]
        
        result = func(*args, **kwargs)
        _cache[key] = result
        return result
    
    return wrapper


def generate_cache_key(func, args, kwargs):
    key = f"{func.__name__}{args}{kwargs}"
    return hashlib.md5(key.encode()).hexdigest()
