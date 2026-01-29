class UserError(Exception):
    pass


class UserAlreadyExist(UserError):
    pass


class UserNotFound(UserError):
    pass