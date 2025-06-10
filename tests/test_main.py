import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Import module to test
import main


class TestHandleMessage(unittest.TestCase):
    """Test the handle_message function."""

    @pytest.mark.asyncio
    async def test_handle_message_success(self):
        """Test successful message handling."""
        # Mock update
        update = MagicMock()
        update.message.from_user.id = 123456789
        update.message.text = "Hello, sage!"
        update.message.reply_text = AsyncMock()

        # Mock context
        context = MagicMock()

        # Mock OpenAI client
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "A wise response"

        # Create patch for OpenAI client
        with patch("main.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client

            # Call function
            await main.handle_message(update, context)

            # Assert the response was sent
            update.message.reply_text.assert_called_once_with("A wise response")

    @pytest.mark.asyncio
    async def test_handle_message_error(self):
        """Test error handling."""
        # Mock update
        update = MagicMock()
        update.message.from_user.id = 123456789
        update.message.text = "Hello, sage!"
        update.message.reply_text = AsyncMock()

        # Mock context
        context = MagicMock()

        # Create patch for OpenAI client with exception
        with patch("main.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_client.chat.completions.create.side_effect = Exception("API error")
            mock_openai.return_value = mock_client

            # Call function
            await main.handle_message(update, context)

            # Assert the fallback response was sent
            update.message.reply_text.assert_called_once_with(main.FALLBACK_MESSAGE)

    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting logic."""
        # Mock update
        update = MagicMock()
        update.message.from_user.id = 123456789
        update.message.text = "Hello, sage!"
        update.message.reply_text = AsyncMock()

        # Mock context
        context = MagicMock()

        # Create a clean user_last_request dictionary
        main.user_last_request = {}

        # Call function first time
        with patch("main.OpenAI"):
            await main.handle_message(update, context)
            assert update.message.reply_text.called
            update.message.reply_text.reset_mock()

            # Call function second time (should be rate limited)
            await main.handle_message(update, context)
            assert not update.message.reply_text.called


if __name__ == "__main__":
    unittest.main()
