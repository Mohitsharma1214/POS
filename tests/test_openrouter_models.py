import os
import pytest
from unittest.mock import patch
from app.services.openrouter_service import OpenRouterService, FREE_MODEL_SLUGS

def test_openrouter_service_defaults_to_free_models():
    # If no model is specified and no env variable is set, it should have self.model = None
    # and try all free models.
    with patch.dict(os.environ, {}, clear=True):
        service = OpenRouterService()
        assert service.model is None
        
        # When model is None, it should construct the list from FREE_MODEL_SLUGS
        # Let's inspect the model_list inside the complete call (mocked)
        with patch("httpx.AsyncClient.post") as mock_post:
            # We raise an exception to exit the complete method early or just mock a response
            # to verify what model it attempts first.
            mock_post.side_effect = Exception("Stop early")
            with pytest.raises(Exception):
                import asyncio
                asyncio.run(service.complete("Hello", return_json=False))
            
            # Verify the first call tried the first model of FREE_MODEL_SLUGS
            args, kwargs = mock_post.call_args
            payload = kwargs.get("json") or args[0] # depending on client signature
            # Let's check payload model
            assert kwargs["json"]["model"] in FREE_MODEL_SLUGS

def test_openrouter_service_respects_free_model_slug():
    # If a free model ending in :free is passed, it should be accepted.
    service = OpenRouterService(model="google/gemma-2-9b-it:free")
    assert service.model == "google/gemma-2-9b-it:free"

def test_openrouter_service_ignores_paid_model_slug():
    # If a paid model is passed, it must be ignored (set to None) to enforce only free models.
    service = OpenRouterService(model="openai/gpt-4o")
    assert service.model is None

def test_openrouter_service_respects_env_free_model():
    # If OPENROUTER_MODEL env var is set to a free model, it should be accepted.
    with patch.dict(os.environ, {"OPENROUTER_MODEL": "meta-llama/llama-3-8b-instruct:free"}):
        service = OpenRouterService()
        assert service.model == "meta-llama/llama-3-8b-instruct:free"

def test_openrouter_service_ignores_env_paid_model():
    # If OPENROUTER_MODEL env var is set to a paid model, it must be ignored.
    with patch.dict(os.environ, {"OPENROUTER_MODEL": "meta-llama/llama-3.1-405b-instruct"}):
        service = OpenRouterService()
        assert service.model is None
