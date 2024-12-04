from fastapi import HTTPException, status


EXCEPTION_FAILED_TO_CONNECT_DB = HTTPException(
    detail="couldn't connect to database",
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
)
EXCEPTION_BLANK_CLIENT_IP = HTTPException(
    detail="somehow you are non-existance client. couldn't get your IP",
    status_code=status.HTTP_400_BAD_REQUEST,
)
EXCEPTION_BLANK_QUERY = HTTPException(
    detail="query was blank",
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
)
EXCEPTION_REQUEST_INVALID = HTTPException(
    detail="request form was invalid to read. check data structure",
    status_code=status.HTTP_400_BAD_REQUEST,
)
EXCEPTION_REQUEST_FAILED_TO_PROCESS = HTTPException(
    detail="request was failed to process.",
    status_code=status.HTTP_400_BAD_REQUEST,
)
