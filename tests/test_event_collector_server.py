import unittest
from event_collector_server import is_valid_event, identify_event


class EPPTestCase(unittest.TestCase):

    def test_is_valid_event(self):
        # 1 good
        event_id = "some_id"
        eventTimestamp = "some_time_stamp"

        result = is_valid_event(event_id, eventTimestamp)
        self.assertTrue(result)

        # bad combinations

        event_id = ""
        eventTimestamp = "some_time_stamp"

        result = is_valid_event(event_id, eventTimestamp)
        self.assertFalse(result)

        event_id = "some_event_id"
        eventTimestamp = ""

        result = is_valid_event(event_id, eventTimestamp)
        self.assertFalse(result)

        event_id = ""
        eventTimestamp = ""

        result = is_valid_event(event_id, eventTimestamp)
        self.assertFalse(result)

    def test_identify_event(self):

        # serving event
        eventType = ""
        parentEventId = ""
        res = identify_event(eventType, parentEventId)
        self.assertEqual("serving_event", res)

        # user event - click
        eventType = "click"
        parentEventId = "121212"
        res = identify_event(eventType, parentEventId)
        self.assertEqual("user_event", res)

        # user event - impression
        eventType = "impression"
        parentEventId = "121212"
        res = identify_event(eventType, parentEventId)
        self.assertEqual("user_event", res)

        # now few problematic ones, has a parentEventId but no eventType.
        eventType = ""
        parentEventId = "121212"
        res = identify_event(eventType, parentEventId)
        self.assertEqual("unparsable_event", res)

        # has correct eventtypy but no parentEventId.
        eventType = "click"
        parentEventId = ""
        res = identify_event(eventType, parentEventId)
        self.assertEqual("unparsable_event", res)

        # has wrong eventtypy parentEventId.
        eventType = "something_else"
        parentEventId = "12121"
        res = identify_event(eventType, parentEventId)
        self.assertEqual("unparsable_event", res)


if __name__ == '__main__':
    unittest.main()
