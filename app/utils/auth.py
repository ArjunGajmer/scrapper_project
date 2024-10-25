from fastapi import Header


def authenticate_user(token: str = Header(...)):
    return token == "your_static_token_here"
