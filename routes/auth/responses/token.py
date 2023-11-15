EXC_400 = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "Missing Email Or Phone": {
                        "value": {
                            "detail": "Either email or phone must be provided"
                        }
                    },
                    "Password Required": {
                        "value": {
                            "detail": "Password is required"
                        }
                    }
                }
            }
        }
    }
}

EXC_401 = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "examples": {
                    "Invalid Code": {
                        "value": {
                            "detail": "Invalid code"
                        }
                    },
                    "Code Expired": {
                        "value": {
                            "detail": "Code has expired"
                        }
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
                    },
                    "Invalid Password": {
                        "value": {
                            "detail": "Invalid password"
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

EXC_429 = {
    429: {
        "description": "Too Many Requests",
        "content": {
            "application/json": {
                "examples": {
                    "Too Many Token Attempts": {
                        "value": {
                            "detail": "Too many token attempts"
                        }
                    },
                    "Too Many Code Attempts": {
                        "value": {
                            "detail": "Too many code attempts"
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
                    },
                    "Code Error": {
                        "value": {"detail": "Invalid length"}
                    },
                    "Password Error": {
                        "value": {"detail": "Invalid length"}
                    }
                }
            }
        }
    }
}
