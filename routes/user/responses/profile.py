EXC_401 = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "examples": {
                    "Unexpected Token": {
                        "value": {
                            "detail": "Expected an another token"
                        }
                    },
                    "Token Expired": {
                        "value": {
                            "detail": "Token has expired"
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
                    "Invalid Signature": {
                        "value": {
                            "detail": "Token has an invalid signature"
                        }
                    },
                    "Invalid Format": {
                        "value": {
                            "detail": "Invalid token format"
                        }
                    },
                    "First Name Error": {
                        "value": {"detail": "Invalid length"}
                    },
                    "Last Name Error": {
                        "value": {"detail": "Invalid length"}
                    },
                    "Nickname Error": {
                        "value": {"detail": "Invalid length"}
                    },
                    "Gender Error": {
                        "value": {"detail": "Invalid gender"}
                    },
                    "Age Error": {
                        "value": {"detail": "Invalid age"}
                    }
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

EXC_404 = {
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            }
        }
    }
}

EXC_409 = {
    409: {
        "description": "Conflict",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Nickname already exists"
                }
            }
        }
    }
}
