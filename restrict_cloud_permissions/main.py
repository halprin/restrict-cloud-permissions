from restrict_cloud_permissions.context.cli_context import CliApplicationContext


if __name__ == '__main__':
    application_context = CliApplicationContext('aws')
    print(application_context.environment_variables())
    print(application_context.cloud_plugin())
