from restrict_cloud_permissions.context.cli_context import CliApplicationContext


if __name__ == '__main__':
    application_context = CliApplicationContext('aws')
    print(application_context.environment_variables())
    response = application_context.cloud_plugin().create_tracking_infrastructure()
    print(response)
