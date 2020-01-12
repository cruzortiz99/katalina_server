from ..domain.repositories import user as repository
from ..domain.entities.users.user import User


def save_user(requestBody):
    '''
    Logical process to save a user
    Parameters:
    ----
    - requestBody: User , user entity
    '''
    local_user = User(requestBody['name'],
                      requestBody['email'], requestBody['password'])
    try:
        return next(repository.save(local_user)), 200
    except StopIteration:
        return {}, 400
    except PermissionError:
        return {}, 403


def login(requestBody):
    '''
    Logical process to get a user
    Parameters:
    ----
    - requestBody:{email:str, password:str}, user email and password
    '''
    try:
        user_dic = next(repository.get_by_id(requestBody['email']))
    except StopIteration:
        return {}, 400
    if user_dic['password'] != requestBody['password']:
        return {}, 403
    '''
    - name: str
    '''
    name = user_dic['name']
    email = user_dic['email']
    password = user_dic['password']
    token = f'{name}{email}{password}'
    user_dic_with_token = dict()
    user_dic_with_token.update(user_dic)
    user_dic_with_token.update(token=token)
    return user_dic_with_token, 200


def getUser(email):
    try:
        return next(repository.get_by_id(email)), 200
    except StopIteration:
        return {}, 404


def updateUser(email, requestBody):
    local_user = User(requestBody['name'], requestBody['email'], '')
    try:
        return next(repository.update(email, local_user)), 200
    except StopIteration:
        {}, 404
    except FileNotFoundError:
        {}, 404
