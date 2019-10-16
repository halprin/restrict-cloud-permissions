from datetime import datetime
from restrict_cloud_permissions.context.test_context import TestApplicationContext
from restrict_cloud_permissions.plugin.aws import AwsPlugin


test_application_context = TestApplicationContext({})


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def test_record_events():
    lookup_events_calls = 3
    lookup_events_call_counter = lookup_events_calls
    static_set_of_events = ['Moof', 'DogCow']

    def call_lookup_events(*args, **kwargs):
        nonlocal lookup_events_call_counter
        nonlocal static_set_of_events
        events = {
            'Events': static_set_of_events,
            'NextToken': 'yes there are more',
        }
        if lookup_events_call_counter == 1:
            del events['NextToken']

        lookup_events_call_counter -= 1
        return events

    test_application_context._sdk = AttrDict({
        'client': lambda client: AttrDict({
            'lookup_events': call_lookup_events,
        }),
    })
    plugin_under_test = AwsPlugin(test_application_context)

    plugin_under_test.record_events('PageSetup', datetime(2019, 9, 28), datetime(2019, 9, 29))

    assert plugin_under_test._events == lookup_events_calls * static_set_of_events
