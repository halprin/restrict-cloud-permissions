import os
from restrict_cloud_permissions.context.application_context import ApplicationContext


class CliApplicationContext(ApplicationContext):
    def environment_variables(self):
        return os.environ
