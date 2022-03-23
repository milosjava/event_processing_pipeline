from flask_testing import TestCase
from event_collector_server import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app


class ServerIntegrationTest(BaseTestCase):
    def test_send_invalid_request(self):
        # no parameters at all
        response = self.client.get('/event_collector')
        self.assertTrue("Invalid event" in str(response.data))

    def test_send_valid_request(self):
        # no parameters at all
        response = self.client.get('/event_collector')
        self.assertTrue("Invalid event" in str(response.data))

    def test_unparsable_event(self):

        eventId = "event1"
        eventTimestamp = "10:00"
        eventType = ""
        parentEventId = "121221"
        userId = "user1"
        advertiserId = "adv1"
        deviceId = ""
        price = 10

        response = self.client.get(
            "/event_collector?eventId={}&eventTimestamp={}&eventType={}&parentEventId={}&userId={}&advertiserId={}&deviceId={}&price={}".format(
                eventId,
                eventTimestamp,
                eventType,
                parentEventId,
                userId,
                advertiserId,
                deviceId,
                price))

        self.assertTrue("unparsable event" in str(response.data))
