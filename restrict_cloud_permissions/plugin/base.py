class Plugin:
    def create_tracking_infrastructure(self):
        raise NotImplementedError

    def delete_tracking_infrastructure(self):
        raise NotImplementedError

    def record_events(self, entity, from_datetime, to_datetime):
        raise NotImplementedError
