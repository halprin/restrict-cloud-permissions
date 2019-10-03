class Plugin:
    def __init__(self, application_context):
        self._application_context = application_context

    def create_tracking_infrastructure(self):
        raise NotImplementedError

    def delete_tracking_infrastructure(self):
        raise NotImplementedError

    def record_events(self, entity, from_datetime, to_datetime):
        raise NotImplementedError

    def create_permission_model(self):
        raise NotImplementedError
