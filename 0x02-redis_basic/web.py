#!/usr/bin/env python3
""" Redis Caching Module """

from functools import wraps
import redis
import requests
from typing import Callable

redis_cache = redis.Redis()


def request_counter_decorator(method: Callable) -> Callable:
    """ Decorator for counting requests """
    @wraps(method)
    def decorated_function(url):  # sourcery skip: use-named-expression
        """ Wrapper function for the decorator """
        redis_cache.incr(f"request_count:{url}")
        cached_html = redis_cache.get(f"cached_html:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html_content = method(url)
        redis_cache.setex(f"cached_html:{url}", 10, html_content)
        return html_content

    return decorated_function


@request_counter_decorator
def fetch_html_content(url: str) -> str:
    """ Obtain the HTML content of a URL """
    request = requests.get(url)
    return request.text
