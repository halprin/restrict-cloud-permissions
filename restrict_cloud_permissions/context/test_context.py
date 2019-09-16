from restrict_cloud_permissions.context.application_context import ApplicationContext


class TestApplicationContext(ApplicationContext):
    def __init__(self, environment_variables):
        self._environment_variables = environment_variables

    def environment_variables(self):
        return self._environment_variables
