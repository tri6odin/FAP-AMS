from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from config import DEV_MODE


class RequestHTTPError(HTTPException):
    def __init__(self, status_code: int, detail: str, hide_details_in_prod: bool = False):
        super().__init__(status_code=status_code, detail=detail)
        self.hide_details_in_prod = hide_details_in_prod


# Dictionary with generalized messages for different status codes
GENERIC_MESSAGES = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    409: "Conflict",
    429: "Too Many Requests",
    500: "Internal Server Error"
}


async def custom_http_handler(request, exc: RequestHTTPError):
    # If we are in development mode or the error should not be hidden, display a detailed message
    if DEV_MODE or not exc.hide_details_in_prod:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    # In production mode and if the error should be hidden, display a general message
    else:
        generic_message = GENERIC_MESSAGES.get(
            exc.status_code, "Error")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": generic_message},
        )


async def custom_pydantic_handler(request, exc: RequestValidationError):
    # Take the first message from the error and return it
    error_message = exc.errors()[0]["msg"]
    return JSONResponse(
        status_code=422,
        content={"detail": error_message}
    )
