import json
import requests
import pandas as pd


def send_event(eventId: str, eventTimestamp: str, eventType: str,
               parentEventId: str, userId: str, advertiserId: str,
               deviceId: str, price: str):
    # api-endpoint
    URL = "http://127.0.0.1:5000/event_collector?eventId={}&eventTimestamp={}&eventType={}&parentEventId={}&userId={" \
          "}&advertiserId={}&deviceId={}&price={}".format(
              eventId, eventTimestamp, eventType,
              parentEventId, userId, advertiserId,
              deviceId, price)

    r = requests.get(url=URL)

    if r.status_code == 200:

        urlData = r.content
        print(urlData)

    else:
        print("error scrape auth ")
        print(r.content)


if __name__ == '__main__':

    server_events = [["event1", "10:00", "", "", "user1", "adv1", "deviceId1", "10"],
                     ["event2", "10:01", "", "", "user2", "adv2", "deviceId2", "12"]]

    user_events = [["event3", "10:05", "impression", "event1", "user1", "adv1", "deviceId1", "10"],  # real event
                   ["event4", "10:08", "impression", "event1",
                       "user1", "adv1", "deviceId1", "10"],
                   # event, duplicate / late
                   ["event5", "9:00", "click", "event1", "user1",
                       "adv1", "deviceId1", "10"],  # fake event
                   ["event6", "10:30", "click", "event1", "user1",
                       "adv1", "deviceId1", "10"],  # real event
                   ["event7", "10:05", "impression", "event1", "user2", "adv1", "deviceId1",
                    "10"]]  # //fake user, user 2 doesn’t have event1

    df_server_events = pd.DataFrame(
        server_events,
        columns=[
            "eventId",
            "eventTimestamp",
            "eventType",
            "parentEventId",
            "userId",
            "advertiserId",
            "deviceId",
            "price"])

    df_user_events = pd.DataFrame(
        user_events,
        columns=[
            "eventId",
            "eventTimestamp",
            "eventType",
            "parentEventId",
            "userId",
            "advertiserId",
            "deviceId",
            "price"])

    df = pd.concat([df_server_events, df_user_events])

    rows = df.to_json(orient='records', lines=True).splitlines()

    for params in rows:
        send_event(**json.loads(params))
