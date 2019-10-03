import json
import iterator_chain
from restrict_cloud_permissions.plugin.base import Plugin


class AwsPlugin(Plugin):
    def __init__(self, application_context):
        super(AwsPlugin, self).__init__(application_context)
        self._cloudtrail_client = self._application_context.cloud_sdk().client('cloudtrail')
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

    def create_permission_model(self):
        resources_actions = iterator_chain.from_iterable(self._events) \
            .map(lambda item: json.loads(item['CloudTrailEvent'])) \
            .filter(lambda event: 'errorCode' not in event) \
            .map(self._parse_event) \
            .reduce(self._cumulate_by_resource)

        permission_model = {
            'Version': '2012-10-17',
            'Statement': [],
        }

        sid_counter = _IncrementInt(0)

        iterator_chain.from_iterable(resources_actions) \
            .for_each(lambda resource: permission_model['Statement'].append({
                'Sid': 'RestrictCloudPermission{}'.format(sid_counter),
                'Effect': 'Allow',
                'Actions': list(resources_actions[resource]),
                'Resource': [resource]
            }))

        return json.dumps(permission_model, indent=4)

    def _cumulate_by_resource(self, cumulator, event):
        if cumulator.get('action', None) is not None:
            # it is the first item
            event0 = cumulator
            cumulator = {}
            # Add the event0's action to the set that belongs to each resource
            iterator_chain.from_iterable(event0['resources']) \
                .for_each(lambda resource: cumulator.setdefault(resource, set()).add(event['action']))

        # Add the event's action to the set that belongs to each resource
        iterator_chain.from_iterable(event['resources']) \
            .for_each(lambda resource: cumulator.setdefault(resource, set()).add(event['action']))

        return cumulator

    def _parse_event(self, event):
        action = self._create_action(event['eventSource'], event['eventName'])
        # This only goes so far.  There are other actions that require a resource, but the event doesn't provide a 'resource' key.  Do I need to somehow parse 'requestParameters'?
        resources = iterator_chain.from_iterable(event.get('resources', [])).map(
            lambda resource: resource['ARN']).list()

        return {
            'action': action,
            'resources': resources,
        }

    def _create_action(self, event_source, event_name):
        return '{}:{}'.format(event_source.split('.')[0], event_name)

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


class _IncrementInt:
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        self._value += 1
        return str(self._value)

