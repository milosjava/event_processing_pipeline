from flask import request, Flask
import pandas as pd
import os

app = Flask(__name__)


# check if both fields are populated
def is_valid_event(eventId: str, eventTimestamp: str) -> bool:
    """
    Checks if event is valid
    :param eventId:
    :param eventTimestamp:
    :return: True if event is valid , false if it is not valid
    """
    return eventId != "" and eventTimestamp != ""


def identify_event(eventType: str, parentEventId: str) -> str:
    """
    Identifies type of event. It can be serving event, user event or unparsable event
    :param eventType:
    :param parentEventId:
    :return: type of event
    """
    if eventType == "" and parentEventId == "":
        return "serving_event"
    if (eventType == "impression" or eventType ==
            "click") and parentEventId != "":
        return "user_event"
    return "unparsable_event"


@app.route('/event_collector', methods=['GET'])
def parse_request():
    """
    This is REST API end point which saves valid events in separate csv files depending on their type
    :return: message regarding outcome
    """
    # 1  retrieve data

    eventId = request.args.get("eventId", default="")
    eventTimestamp = request.args.get("eventTimestamp", default="")
    parentEventId = request.args.get("parentEventId", default="")
    eventType = request.args.get("eventType", default="")
    userId = request.args.get("userId", default="")
    advertiserId = request.args.get("advertiserId", default="")
    deviceId = request.args.get("deviceId", default="")
    price = request.args.get("price", default="")

    # 2 check if this is valid event
    if not is_valid_event(eventId, eventTimestamp):
        return "Invalid event, both eventId and eventTimestamp must have values"

    # 3 check type of event
    type_of_event = identify_event(eventType, parentEventId)

    if type_of_event == "unparsable_event":
        return "unparsable event"

    # 4  save to corresponding file

    df = pd.DataFrame([{
        "eventId": eventId,
        "eventTimestamp": eventTimestamp,
        "eventType": eventType,
        "parentEventId": parentEventId,
        "userId": userId,
        "advertiserId": advertiserId,
        "deviceId": deviceId,
        "price": price
    }])

    if type_of_event == "serving_event":
        df.to_csv('output/serving_events.csv', mode='a', index=False,
                  header=not os.path.exists('output/serving_events.csv'))
    else:
        df.to_csv('output/user_events.csv', mode='a', index=False,
                  header=not os.path.exists('output/user_events.csv'))

    return "event saved"


if __name__ == "__main__":
    app.run()
