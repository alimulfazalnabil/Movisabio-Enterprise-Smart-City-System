import pytest
from src.api.responses import StandardResponse, PaginatedResponse, PaginationCursor
from src.core.context import set_trace_context

def test_standard_response_schema():
    set_trace_context("req_123", "corr_123")
    
    response = StandardResponse[dict](data={"status": "ok"})
    
    dump = response.model_dump()
    assert "data" in dump
    assert "meta" in dump
    assert dump["meta"]["request_id"] == "req_123"
    assert dump["data"]["status"] == "ok"

def test_paginated_response_schema():
    set_trace_context("req_456", "corr_456")
    
    cursor = PaginationCursor(next_cursor="cursor_abc", has_more=True)
    response = PaginatedResponse[str](data=["item1", "item2"], pagination=cursor)
    
    dump = response.model_dump()
    assert dump["pagination"]["has_more"] is True
    assert dump["pagination"]["next_cursor"] == "cursor_abc"
    assert len(dump["data"]) == 2
    assert dump["meta"]["request_id"] == "req_456"
