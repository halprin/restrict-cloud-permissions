from restrict_cloud_permissions.plugin.base import Plugin


class AwsPlugin(Plugin):
    def create_tracking_infrastructure(self):
        pass

    def delete_tracking_infrastructure(self):
        pass

    def _create_cloud_trail(self):
        pass

    def _delete_cloud_trail(self):
        pass
