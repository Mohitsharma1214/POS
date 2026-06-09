import asyncio
import os
from dotenv import load_dotenv

# We won't actually hit the API if there's no key, but we can verify the payload structure if we mock httpx
import httpx
from unittest.mock import patch

from app.services.pipeline import call_model

async def main():
    load_dotenv()
    
    # Check if we have a real key, if not, we use mock
    if not os.getenv("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = "sk-ant-dummy-key"
        
    with patch("httpx.post") as mock_post:
        mock_response = httpx.Response(200, json={"content": [{"text": "{\"status\": \"success\"}"}]})
        mock_post.return_value = mock_response
        
        try:
            result = call_model("claude-3-5-sonnet-20241022", "Respond with JSON.")
            print("call_model result:", result)
            
            # verify payload structure
            args, kwargs = mock_post.call_args
            print("URL:", args[0])
            print("Headers:", kwargs.get("headers"))
            print("Payload:", kwargs.get("json"))
            print("MOCK TEST PASSED!")
        except Exception as e:
            print("ERROR:", e)

if __name__ == "__main__":
    asyncio.run(main())
