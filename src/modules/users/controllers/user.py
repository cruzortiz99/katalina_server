from src.modules.users.domain.repositories import user as repository
from src.modules.users.domain.entities.user import User


def save_user(requestBody):
    '''
    Logical process to save a user

    Parameters:
    ----
    :param {name: str, email: str, password: str} requestBody: user entity

    Return:
    ----
    :return Tuple[json, int]: with the user saved/error msj and status
    '''
    local_user = User(requestBody['name'],
                      requestBody['email'], requestBody['password'])
    try:
        return next(repository.save(local_user)), 200
    except StopIteration:
        return {'msj': 'Request has an error'}, 400
    except PermissionError:
        return {'msj': 'User Already exists'}, 403


def login(requestBody):
    '''
    Logical process to get a user

    Parameters:
    ----
    :param {email:str, password:str} requestBody: user email and password

    Return:
    ----
    :return Tuple[json, int]: json response and status
    '''
    try:
        user_dic = next(repository.get_by_id(requestBody['email']))
    except StopIteration:
        return {'msj': 'User was not found'}, 404
    if user_dic['password'] != requestBody['password']:
        return {'msj': 'User or password were wrong'}, 403
    name = user_dic['name']
    email = user_dic['email']
    password = user_dic['password']
    token = f'{name}{email}{password}'
    user_dic_with_token = dict()
    user_dic_with_token.update(user_dic)
    user_dic_with_token.update(token=token)
    return user_dic_with_token, 200


def getUser(email):
    '''
    Get user by email

    Parameters:
    ----
    :param str email: email of the user

    Return:
    ----
    :return Tuple[json, int]: json response and status
    '''
    try:
        return next(repository.get_by_id(email)), 200
    except StopIteration:
        return {'msj': 'User not found'}, 404


def updateUser(email, requestBody):
    '''
    Update user by email

    Parameters:
    ----
    :param str email: email of the user

    :param {name: str, email: str} requestBody: request accepted

    Return:
    ----
    :return Tuple[json, int]: json response and status
    '''
    local_user = User(requestBody['name'], requestBody['email'], '')
    try:
        return next(repository.update(email, local_user)), 200
    except (StopIteration, FileNotFoundError):
        {'msj': 'User not found'}, 404
