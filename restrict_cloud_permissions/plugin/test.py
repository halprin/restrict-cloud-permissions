from restrict_cloud_permissions.plugin.base import Plugin


class TestPlugin(Plugin):
    def create_tracking_infrastructure(self):
        pass

    def delete_tracking_infrastructure(self):
        pass

    def record_events(self, entity, from_datetime, to_datetime):
        pass
