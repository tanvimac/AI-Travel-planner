import os
import sys
from unittest.mock import MagicMock
from google.genai.errors import ClientError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.gemini_retry import gemini_generate

def test_retry_on_429():
    mock_client = MagicMock()
    call_count = 0

    def mock_generate_content(**kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # First call raises ClientError 429
            raise ClientError(429, {"error": {"code": 429, "message": "Resource exhausted"}}, None)
        
        # Second call succeeds
        mock_response = MagicMock()
        mock_response.text = "Success after 429 retry"
        return mock_response

    mock_client.models.generate_content = mock_generate_content

    result = gemini_generate(
        mock_client,
        model="dummy-model",
        contents="test",
    )

    assert result.text == "Success after 429 retry"
    assert call_count == 2
    print("SUCCESS: gemini_generate retried on 429 and succeeded on call 2!")

if __name__ == "__main__":
    test_retry_on_429()
