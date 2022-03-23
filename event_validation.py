import pandas as pd


def _time_delta_to_HH_MM(timedelta) -> str:
    """

    :param timedelta:
    :return: string representation in HH:mm format of time delta , e.g. 10:05
    """
    seconds = timedelta.seconds

    hours = seconds // 3600
    minutes = (seconds // 60) % 60

    if minutes < 10:
        return str(hours) + ":0" + str(minutes)

    return str(hours) + ":" + str(minutes)


def validate(serving_events_filepath: str = "output/serving_events.csv",
             user_events_filepath: str = "output/user_events.csv") -> pd.DataFrame:
    """

    :param serving_events_filepath: location for serving events csv file
    :param user_events_filepath:  location for user events csv file
    :return: cleaned and deduplicated merged file by following rules as described inside code
    """
    # load generated files
    se_df = pd.read_csv(serving_events_filepath)
    ue_df = pd.read_csv(user_events_filepath)

    # Validated user events have the following conditions met:
    #   a. parentEventId matches an eventId in the server events.

    ue_df = ue_df[ue_df["parentEventId"].isin(se_df["eventId"])]

    #   b. userId in both event types are equal
    #   lets merge these two
    combined_df = ue_df.merge(
        se_df, left_on=[
            "userId", "parentEventId"], right_on=[
            "userId", "eventId"], suffixes=(
                '_ue', '_se'))

    # c. eventTimestamp in server events occur before event timestamp of user
    # event

    # first convert eventTimestamps to time delta so we can compare
    combined_df["eventTimestamp_ue"] = pd.to_timedelta(
        combined_df.eventTimestamp_ue + ':00')
    combined_df["eventTimestamp_se"] = pd.to_timedelta(
        combined_df.eventTimestamp_se + ':00')

    # make sure that server event was before user event
    combined_df = combined_df[combined_df["eventTimestamp_se"]
                              < combined_df["eventTimestamp_ue"]]

    #   d. Dedupe for parentEventId and the event type. That is, the output shouldn’t
    #       contain multiple events with the same parentEventId and eventType.
    #   e. Pick the earliest eventTimestamp of the user events while deduping

    combined_df.sort_values(by="eventTimestamp_ue", inplace=True)

    combined_df = combined_df.drop_duplicates(
        subset=["parentEventId_ue", 'eventType_ue'], keep='first')

    # convert back to HH:MM format as in assignment example
    combined_df.eventTimestamp_ue = combined_df.eventTimestamp_ue.map(
        _time_delta_to_HH_MM)

    # Enrich the valid user event, augmenting with the advertiserId and price fields from the
    # matching server event.
    combined_df = combined_df[  # NOTE: taking advertiserId_se and price_se from server event
        ["eventId_ue", "eventTimestamp_ue", "eventType_ue", "parentEventId_ue", "userId", "advertiserId_se",
         "deviceId_ue", "price_se"]]

    # fix the column names
    combined_df.columns = [
        "eventId",
        "eventTimestamp",
        "eventType",
        "parentEventId",
        "userId",
        "advertiserId",
        "deviceId",
        "price"]

    return combined_df


if __name__ == '__main__':
    combined_df = validate()
    combined_df.to_csv("output/validated_events.csv", index=False)
