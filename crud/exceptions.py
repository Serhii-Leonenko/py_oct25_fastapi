class UserError(Exception):
    pass


class UserAlreadyExist(UserError):
    pass


class OwnerNotFoundError(Exception):
    pass


class ProjectNotFoundError(Exception):
    pass


class TaskNotFoundError(Exception):
    pass


class AssigneeNotFoundError(Exception):
    pass


class TaskAlreadyExist(Exception):
    pass
