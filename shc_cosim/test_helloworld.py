import pytest

pytestmark = pytest.mark.asyncio

async def test_hello(host_board):
    host_board.wait_for_regex_in_line("Hello World")