import pytest

pytestmark = pytest.mark.asyncio

@pytest.mark.skip
async def test_hello(client_board):
    client_board.wait_for_regex_in_line("Hello World")