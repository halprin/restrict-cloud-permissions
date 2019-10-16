class ApplicationContext:
    def environment_variables(self):
        raise NotImplementedError

    def cloud_plugin(self):
        raise NotImplementedError

    def cloud_sdk(self):
        raise NotImplementedError
