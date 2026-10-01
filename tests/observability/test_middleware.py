import pytest
import json
import uuid
from src.core.context import set_trace_context, get_trace_context

def test_trace_context_propagation():
    """
    Test that request_id and correlation_id properly populate ContextVars
    """
    req_id = str(uuid.uuid4())
    corr_id = str(uuid.uuid4())
    
    set_trace_context(req_id, corr_id)
    
    ctx = get_trace_context()
    assert ctx["request_id"] == req_id
    assert ctx["correlation_id"] == corr_id
