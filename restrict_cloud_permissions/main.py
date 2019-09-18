from datetime import datetime
from restrict_cloud_permissions.context.cli_context import CliApplicationContext


if __name__ == '__main__':
    application_context = CliApplicationContext('aws')
    application_context.cloud_plugin().record_events('halprin', datetime(2019, 9, 13), datetime(2019, 9, 14))
