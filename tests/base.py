import asyncio
from unittest import TestCase


class BaseTestCase(TestCase):
    """
    This class can be used as a base for async test cases.
    Usage:
        async def test__some_async_thing(self):
            await some_method()
        async def asyncSetUp(self):
            await some_setup()
        async def asyncTearDown(self):
            await some_teardown()
    """

    def __getattribute__(self, name):
        """
        Gather test methods.
        If method is async, then wrap it in an event loop runner.
        """
        attr = super().__getattribute__(name)
        if name.startswith('test_') and asyncio.iscoroutinefunction(attr):
            return lambda: asyncio.run(self.async_test_wrapper(attr))
        else:
            return attr

    async def async_test_wrapper(self, func):
        asyncSetUp = getattr(self, 'asyncSetUp', None)
        await asyncSetUp() if asyncSetUp else None

        await func()

        asyncTearDown = getattr(self, 'asyncTearDown', None)
        await asyncTearDown() if asyncTearDown else None
