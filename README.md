![Lint](https://github.com/JeanPinzon/py-easy-rest-redis-cache/actions/workflows/python-lint.yml/badge.svg)
![Build and Test](https://github.com/JeanPinzon/py-easy-rest-redis-cache/actions/workflows/python-test.yml/badge.svg)
![Upload Package](https://github.com/JeanPinzon/py-easy-rest-redis-cache/actions/workflows/python-publish.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/py-easy-rest-redis-cache.svg)](https://badge.fury.io/py/py-easy-rest-redis-cache)

# py-easy-rest-redis-cache

Cache lib to use with [py-easy-rest](https://github.com/JeanPinzon/py-easy-rest)


## Getting Started

### How to install

`pip install py-easy-rest py-easy-rest-redis-cache`


### Integrating with your [py-easy-rest](https://github.com/JeanPinzon/py-easy-rest) app


```python
#main.py
from py_easy_rest.server import App
from py_easy_rest_redis_cache.redis_cache import RedisCache


config = {
    "name": "Project Name",
    "schemas": [{
        "name": "Mock",
        "slug": "mock",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
        },
        "required": ["name"],
    }]
}

cache = RedisCache("redis://localhost")

pyrApp = App(config, cache=cache)

pyrApp.app.run(
    host='0.0.0.0',
    port=8000,
    debug=True,
    auto_reload=True,
)
```
