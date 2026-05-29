# tests/test_fallback_pipeline.py

import pytest
from unittest.mock import patch, AsyncMock
from app.services.pipeline import extract_and_parse_json, call_with_fallback, run_full_pipeline
from app.services.models import build_prompt

def test_extract_and_parse_json_basic():
    # Test typical clean JSON
    content = '{"key": "value"}'
    parsed = extract_and_parse_json(content)
    assert parsed == {"key": "value"}

def test_extract_and_parse_json_with_thinking_tags():
    # Test Deepseek thinking block stripping
    content = '<thinking>I need to think. Ok, finished.</thinking>{"score": 8, "reason": "Good job"}'
    parsed = extract_and_parse_json(content)
    assert parsed == {"score": 8, "reason": "Good job"}

def test_extract_and_parse_json_with_markdown_fences():
    # Test markdown fences with json indicator
    content = '```json\n{"key": "value"}\n```'
    parsed = extract_and_parse_json(content)
    assert parsed == {"key": "value"}

def test_extract_and_parse_json_with_trailing_fences():
    content = '```\n{"key": "value"}\n```'
    parsed = extract_and_parse_json(content)
    assert parsed == {"key": "value"}

def test_extract_and_parse_json_bracket_fallback():
    # Test when there are preamble words
    content = 'Here is the response: {"summary": "Great guest"} and some suffix.'
    parsed = extract_and_parse_json(content)
    assert parsed == {"summary": "Great guest"}

def test_build_prompt_tweaks():
    core = "Create a summary."
    # Gemini should have no changes
    assert build_prompt(core, "google/gemini-2.5-pro-exp-03-25:free") == core
    # Deepseek should have Output Rule
    deepseek_prompt = build_prompt(core, "deepseek/deepseek-r1:free")
    assert "OUTPUT RULE" in deepseek_prompt
    # Qwen should have /no_think
    qwen_prompt = build_prompt(core, "qwen/qwen-2.5-72b-instruct:free")
    assert "/no_think" in qwen_prompt

@pytest.mark.asyncio
@patch("app.services.pipeline.call_model")
async def test_call_with_fallback_success_first_attempt(mock_call):
    mock_call.return_value = '{"title_formulas": []}'
    
    # We test Step 2 extraction
    result = await call_with_fallback("step2_extraction", "Core Prompt")
    assert result == {"title_formulas": []}
    mock_call.assert_called_once()

@pytest.mark.asyncio
@patch("app.services.pipeline.call_model")
async def test_call_with_fallback_rate_limit_and_success(mock_call):
    import httpx
    # Raise a 429 rate limit error on first call, succeed on second attempt (of the same model)
    req = httpx.Request("POST", "http://test")
    resp = httpx.Response(429, request=req)
    
    mock_call.side_effect = [
        httpx.HTTPStatusError("Rate Limit Exceeded (429)", request=req, response=resp),
        '{"title_formulas": ["formula1"]}'
    ]
    
    result = await call_with_fallback("step2_extraction", "Core Prompt", max_retries=1)
    assert result == {"title_formulas": ["formula1"]}
    assert mock_call.call_count == 2

@pytest.mark.asyncio
@patch("app.services.pipeline.call_model")
async def test_call_with_fallback_advances_on_error(mock_call):
    # First model fails completely with standard exception.
    # Second model returns valid JSON.
    mock_call.side_effect = [
        Exception("Critical API Failure"),
        '{"title_formulas": ["advanced_formula"]}'
    ]
    
    result = await call_with_fallback("step2_extraction", "Core Prompt")
    assert result == {"title_formulas": ["advanced_formula"]}
    assert mock_call.call_count == 2
