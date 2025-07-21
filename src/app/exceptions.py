from fastapi import HTTPException, status

def NotFoundException(detail: dict):
    """
    Exception raised when a requested resource is not found.
    
    Args:
        message (str): The error message to be displayed.
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )
    