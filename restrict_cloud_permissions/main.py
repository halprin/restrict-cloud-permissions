from restrict_cloud_permissions.context.cli_context import CliApplicationContext


if __name__ == '__main__':
    application_context = CliApplicationContext()
    print(application_context.environment_variables())
