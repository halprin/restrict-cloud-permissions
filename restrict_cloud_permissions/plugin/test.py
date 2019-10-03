from restrict_cloud_permissions.plugin.base import Plugin


class TestPlugin(Plugin):
    def __init__(self, application_context):
        super(TestPlugin, self).__init__(application_context)

    def create_tracking_infrastructure(self):
        pass

    def delete_tracking_infrastructure(self):
        pass

    def record_events(self, entity, from_datetime, to_datetime):
        pass

    def create_permission_model(self):
        pass
