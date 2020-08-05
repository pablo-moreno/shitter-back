from channels.db import database_sync_to_async


class PermissionMixin(object):
    permission_classes = ()

    async def websocket_connect(self, message):
        scope = message.scope

        try:
            await self.check_permissions(scope)
            await super().websocket_connect(message)
        except PermissionError:
            await self.close()

    @database_sync_to_async
    def check_permissions(self, scope):
        has_permission = all(
            cls(scope).has_permission() for cls in self.permission_classes
        )
        if not has_permission:
            raise PermissionError('Permission denied')

        return has_permission
