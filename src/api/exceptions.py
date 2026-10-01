from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.api.responses import ErrorResponse, ErrorDetail
from src.core.context import get_trace_context
from src.observability.logger import get_logger

logger = get_logger()

class MoviSabioException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

async def movisabio_exception_handler(request: Request, exc: MoviSabioException):
    ctx = get_trace_context()
    request_id = ctx.get("request_id")
    
    # Log the exception for observability
    logger.warning("api_exception", extra_attrs={
        "code": exc.code,
        "message": exc.message,
        "status_code": exc.status_code,
        "path": request.url.path
    })

    error = ErrorDetail(code=exc.code, message=exc.message, request_id=request_id)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=error).model_dump()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    ctx = get_trace_context()
    request_id = ctx.get("request_id")
    
    error = ErrorDetail(
        code="VALIDATION_ERROR",
        message="The request is invalid. Check schema constraints.",
        request_id=request_id
    )
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(error=error).model_dump()
    )

async def global_exception_handler(request: Request, exc: Exception):
    ctx = get_trace_context()
    request_id = ctx.get("request_id")
    
    logger.error("internal_server_error", extra_attrs={
        "path": request.url.path,
        "error": str(exc)
    }, exc_info=True)
    
    error = ErrorDetail(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
        request_id=request_id
    )
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(error=error).model_dump()
    )
