EXC_404 = {
    404: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Version of public key does not exist"
                }
            }
        }
    }
}
EXC_422 = {
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid version"
                }
            }
        }
    }
}
