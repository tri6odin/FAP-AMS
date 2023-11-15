EXC_400 = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Either email or phone must be provided"
                }
            }
        }
    }
}
EXC_403 = {
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "examples": {
                    "Account Deleted": {
                        "value": {
                            "detail": "Account is deleted"
                        }
                    },
                    "Account Banned": {
                        "value": {
                            "detail": "Account is banned"
                        }
                    },
                    "Account Suspended": {
                        "value": {
                            "detail": "Account is suspended. Please contact support"
                        }
                    }
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
                "examples": {
                    "Email Error": {
                        "value": {"detail": "The email address is not valid. It must have exactly one @-sign."}
                    },
                    "Phone Error": {
                        "value": {"detail": "???"}
                    }
                }
            }
        }
    }
}
EXC_429 = {
    429: {
        "description": "Too Many Requests",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Too many code attempts"
                }
            }
        }
    }
}

EXC_500 = {
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "examples": {
                    "Sending Issue": {
                        "value": {"detail": "Sending failed"}
                    },
                    "Code Error": {
                        "value": {"detail": "Total code unique digits param error"}
                    }
                }
            }
        }
    }
}
