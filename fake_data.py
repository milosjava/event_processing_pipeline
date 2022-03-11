from faker import Faker

faker = Faker(locale='en_US')

if __name__ == '__main__':
    # eventId = "event1"
    #eventTimestamp = "10:00"
    eventType = ""
    parentEventId = ""
    userId = "user1"
    advertiserId = "adv1"
    deviceId = ""
    price = 10

    ###
    samples = 10

    # eventId
    eventId = [i for i in range(1, samples + 1)]

    # eventTimestamp
    for _ in range(5):
        print(faker.time(pattern='%H:%M'))

    eventTimestamp = [faker.time(pattern='%H:%M') for _ in range(0, 10)]


    # userId

    print("hello")
