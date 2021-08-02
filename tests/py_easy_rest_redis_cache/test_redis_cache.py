import pytest

from unittest.mock import Mock, AsyncMock
from aiounittest import AsyncTestCase

import aioredis

from py_easy_rest_redis_cache.redis_cache import RedisCache


class RedisPoolMock():
    
    async def get(self, key, encoding):
        pass

    async def set(key, value, expire):
        pass

    async def delete(self, key):
        pass

    def close(self):
        pass

    async def wait_closed(self):
        pass

class TestRedisCache(AsyncTestCase):

    def setUp(self):
        self.redis_pool_mock = Mock(RedisPoolMock)
        aioredis.create_redis_pool = AsyncMock(return_value=self.redis_pool_mock)

    @pytest.mark.asyncio
    async def test_should_get_calls_aioredis_correctly_and_returns_correct_value(self):
        mocked_connection_string = "mocked_connection_string"
        expected_cache_value = "mocked_cache_value"
        cache_key = "cache_key"
        
        self.redis_pool_mock.get.return_value = expected_cache_value
        redis_cache = RedisCache(mocked_connection_string)

        cached_value = await redis_cache.get(cache_key)

        assert cached_value == expected_cache_value

        self.redis_pool_mock.get.assert_called_once_with(cache_key, encoding="utf-8")
        self.redis_pool_mock.close.assert_called_once()
        self.redis_pool_mock.wait_closed.assert_called_once()
        
        aioredis.create_redis_pool.assert_called_once_with(mocked_connection_string)

    @pytest.mark.asyncio
    async def test_should_get_calls_aioredis_correctly_and_returns_None_if_value_not_found(self):
        mocked_connection_string = "mocked_connection_string"
        cache_key = "cache_key"
        
        self.redis_pool_mock.get.return_value = None
        redis_cache = RedisCache(mocked_connection_string)

        cached_value = await redis_cache.get(cache_key)

        assert cached_value is None

        self.redis_pool_mock.get.assert_called_once_with(cache_key, encoding="utf-8")
        self.redis_pool_mock.close.assert_called_once()
        self.redis_pool_mock.wait_closed.assert_called_once()
        
        aioredis.create_redis_pool.assert_called_once_with(mocked_connection_string)

    @pytest.mark.asyncio
    async def test_should_set_calls_aioredis_correctly(self):
        mocked_connection_string = "mocked_connection_string"
        cache_key = "cache_key"
        cache_value = "mocked_value"
        
        redis_cache = RedisCache(mocked_connection_string)

        await redis_cache.set(cache_key, cache_value)

        self.redis_pool_mock.set.assert_called_once_with(cache_key, cache_value, expire=0)
        self.redis_pool_mock.close.assert_called_once()
        self.redis_pool_mock.wait_closed.assert_called_once()
        
        aioredis.create_redis_pool.assert_called_once_with(mocked_connection_string)

    @pytest.mark.asyncio
    async def test_should_set_with_ttl_calls_aioredis_correctly(self):
        mocked_connection_string = "mocked_connection_string"
        cache_key = "cache_key"
        cache_value = "mocked_value"
        cache_ttl = 666
        
        redis_cache = RedisCache(mocked_connection_string)

        await redis_cache.set(cache_key, cache_value, cache_ttl)

        self.redis_pool_mock.set.assert_called_once_with(cache_key, cache_value, expire=cache_ttl)
        self.redis_pool_mock.close.assert_called_once()
        self.redis_pool_mock.wait_closed.assert_called_once()
        
        aioredis.create_redis_pool.assert_called_once_with(mocked_connection_string)

    @pytest.mark.asyncio
    async def test_should_delete_calls_aioredis_correctly(self):
        mocked_connection_string = "mocked_connection_string"
        cache_key = "cache_key"
        
        redis_cache = RedisCache(mocked_connection_string)

        await redis_cache.delete(cache_key)

        self.redis_pool_mock.delete.assert_called_once_with(cache_key)
        self.redis_pool_mock.close.assert_called_once()
        self.redis_pool_mock.wait_closed.assert_called_once()
        
        aioredis.create_redis_pool.assert_called_once_with(mocked_connection_string)