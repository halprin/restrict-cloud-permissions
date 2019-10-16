from datetime import datetime
from restrict_cloud_permissions.context.cli_context import CliApplicationContext


if __name__ == '__main__':
    application_context = CliApplicationContext('aws')
    application_context.cloud_plugin().record_events('halprin', datetime(2019, 9, 28), datetime(2019, 9, 29))
    permissions = application_context.cloud_plugin().create_permission_model()
    print(permissions)
