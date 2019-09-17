import os
from restrict_cloud_permissions.context.application_context import ApplicationContext
from restrict_cloud_permissions.plugin.aws import AwsPlugin


class CliApplicationContext(ApplicationContext):
    def __init__(self, cloud_platform):
        if cloud_platform == 'aws':
            self._plugin = AwsPlugin()
        else:
            self._plugin = None

    def environment_variables(self):
        return os.environ

    def cloud_plugin(self):
        return self._plugin
