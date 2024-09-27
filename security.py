from typing import Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

#schemas 
from schemas import User, UserInDB


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "hashedsecret",
    },
    "janedoe": {
        "username": "janedoe",
        "hashed_password": "hashedsecret2",
    },
}


def fakely_hash_password(password: str):
    """
    A fake password hasher that just prepends 'hashed' to the password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return f"hashed{password}"

def get_user(db, username: str):
    """
    Gets a user from a database by username.

    Args:
        db (Dict[str, Dict[str, str]]): The database of users.
        username (str): The username to search for.

    Returns:
        UserInDB | None: The user if found, None otherwise.
    """
    if username in db: 
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_token_generator(user: UserInDB) -> str:
    """
    A fake token generator that just prepends 'tokenized' to the user's username.

    Args:
        user (UserInDB): The user to generate a token for.

    Returns:
        str: The generated token.
    """
    return f'tokenized{user.username}'

def fake_decode_token(token: str) -> Union[UserInDB, None]:
    if token.startswith('tokenized'):
        user_id = token.removeprefix('tokenized')
        user = get_user(fake_users_db, user_id)
        return user
    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_user_from_token(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """
    Decodes a token and returns the associated user.

    Args:
        token (str): The token to decode.

    Returns:
        UserInDB: The user associated with the token.

    Raises:
        HTTPException: If the token is invalid.
    """
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
    