import os
import boto3
from restrict_cloud_permissions.context.application_context import ApplicationContext
from restrict_cloud_permissions.plugin.aws import AwsPlugin


class CliApplicationContext(ApplicationContext):
    def __init__(self, cloud_platform):
        if cloud_platform == 'aws':
            self._sdk = boto3
            self._plugin = AwsPlugin(self)
        else:
            self._sdk = None
            self._plugin = None

    def environment_variables(self):
        return os.environ

    def cloud_plugin(self):
        return self._plugin

    def cloud_sdk(self):
        return self._sdk
