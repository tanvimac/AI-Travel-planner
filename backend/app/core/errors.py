import uuid
from typing import Optional, Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppException(Exception):
    """Base application exception providing standardized error codes and messages."""
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Any] = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


class ProviderException(AppException):
    def __init__(self, message: str = "External travel provider is currently unavailable", details: Optional[Any] = None):
        super().__init__(
            code="PROVIDER_UNAVAILABLE",
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details,
        )


class NotFoundException(AppException):
    def __init__(
        self,
        resource: Optional[str] = None,
        identifier: Optional[Any] = None,
        message: Optional[str] = None,
        details: Optional[Any] = None,
    ):
        if not message:
            message = f"{resource or 'Resource'} with identifier '{identifier}' was not found."
        super().__init__(
            code="RESOURCE_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class ValidationException(AppException):
    def __init__(self, message: str = "Validation failed for submitted request", details: Optional[Any] = None):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


class ConflictException(AppException):
    def __init__(self, message: str = "Resource conflict occurred", details: Optional[Any] = None):
        super().__init__(
            code="RESOURCE_CONFLICT",
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            details=details,
        )


class AuthenticationException(AppException):
    def __init__(self, message: str = "Authentication credentials were invalid or missing."):
        super().__init__(
            code="AUTHENTICATION_REQUIRED",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class PermissionException(AppException):
    def __init__(self, message: str = "You do not have permission to perform this action."):
        super().__init__(
            code="PERMISSION_DENIED",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class RateLimitException(AppException):
    def __init__(self, message: str = "Rate limit exceeded. Please wait before retrying."):
        super().__init__(
            code="RATE_LIMIT_EXCEEDED",
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )


def _get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", str(uuid.uuid4()))


def format_error_response(
    code: str,
    message: str,
    request: Request,
    details: Optional[Any] = None,
) -> dict:
    resp = {
        "error": {
            "code": code,
            "message": message,
            "request_id": _get_request_id(request),
        }
    }
    if details is not None:
        resp["error"]["details"] = details
    return resp


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(exc.code, exc.message, request, exc.details),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    detail = exc.detail
    message = detail if isinstance(detail, str) else "An HTTP error occurred."
    code = f"HTTP_{exc.status_code}"
    if exc.status_code == 404:
        code = "RESOURCE_NOT_FOUND"
    elif exc.status_code == 401:
        code = "AUTHENTICATION_REQUIRED"
    elif exc.status_code == 403:
        code = "PERMISSION_DENIED"
    elif exc.status_code == 503:
        code = "SERVICE_UNAVAILABLE"

    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(code, message, request),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    simplified_errors = [
        {"field": ".".join(str(loc) for loc in err["loc"] if loc != "body"), "message": err["msg"]}
        for err in errors
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=format_error_response(
            "VALIDATION_ERROR",
            "Request validation failed. Please check submitted parameters.",
            request,
            details=simplified_errors,
        ),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Sanitized error message without leaking stack traces or internal secrets
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error_response(
            "INTERNAL_SERVER_ERROR",
            "An internal error occurred while processing the request.",
            request,
        ),
    )
