from restrict_cloud_permissions.context.application_context import ApplicationContext
from restrict_cloud_permissions.plugin.test import TestPlugin


class TestApplicationContext(ApplicationContext):
    def __init__(self, environment_variables):
        self._environment_variables = environment_variables
        self._plugin = TestPlugin()

    def environment_variables(self):
        return self._environment_variables

    def cloud_plugin(self):
        return self._plugin
