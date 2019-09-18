import boto3
from restrict_cloud_permissions.plugin.base import Plugin


class AwsPlugin(Plugin):
    def __init__(self):
        self._cloudtrail_client = boto3.client('cloudtrail')
        self._events = []

    def create_tracking_infrastructure(self):
        pass

    def delete_tracking_infrastructure(self):
        pass

    def record_events(self, entity, from_datetime, to_datetime):
        events = self._lookup_events(entity, from_datetime, to_datetime)
        self._events += events['Events']

        while events.get('NextToken', None) is not None:
            events = self._lookup_events(entity, from_datetime, to_datetime, next_token=events['NextToken'])
            self._events += events['Events']

    def _lookup_events(self, entity, from_datetime, to_datetime, next_token=None):
        if next_token:
            events = self._cloudtrail_client.lookup_events(
                StartTime=from_datetime,
                EndTime=to_datetime,
                LookupAttributes=[{
                    'AttributeKey': 'Username',
                    'AttributeValue': entity
                }],
                NextToken=next_token
            )
        else:
            events = self._cloudtrail_client.lookup_events(
                StartTime=from_datetime,
                EndTime=to_datetime,
                LookupAttributes=[{
                    'AttributeKey': 'Username',
                    'AttributeValue': entity
                }]
            )

        return events
