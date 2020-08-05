class Permission(object):
    def __init__(self, scope):
        self.scope = scope

    def has_permission(self, *args, **kwargs):
        raise NotImplementedError('You must implement has_permission method!')


class Any(Permission):
    def has_permission(self, *args, **kwargs):
        return True
