from typing import Any, Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field
from src.core.context import get_trace_context

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: Optional[str] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail

class ResponseMeta(BaseModel):
    request_id: Optional[str] = None

class StandardResponse(BaseModel, Generic[T]):
    data: T
    meta: ResponseMeta = Field(default_factory=lambda: ResponseMeta(request_id=get_trace_context().get("request_id")))

class PaginationCursor(BaseModel):
    next_cursor: Optional[str]
    has_more: bool

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    pagination: PaginationCursor
    meta: ResponseMeta = Field(default_factory=lambda: ResponseMeta(request_id=get_trace_context().get("request_id")))
