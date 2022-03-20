# Event Processing Pipeline

[![Continuous Integration](https://github.com/milosjava/event_processing_pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/milosjava/event_processing_pipeline/actions/workflows/ci.yml)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![poetry](https://img.shields.io/badge/maintained%20with-poetry-rgb(30%2041%2059).svg)](https://python-poetry.org/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)


A Take-Home Programming Exercise

# Introduction

Full text of this exercise is explained in docs/AEP programming challenge.pdf

There are two parts of this assignment. First, called **Event Collector** is a REST API, receiving HTTP GET requests,
classifying events and creating two types of csv files: one for user events and another for server events.

Second part, called **Event Validator** analyzes results from previous step, cleans, deduplicate, merge these 2 data
sets and merge data as described in requirements with validated events data set as a final result.

## Event Collector REST API

----
This is classic HTTP GET request REST API

* **Method:**

  event_collector

  `GET`

* **URL Params**

  All parameters have default value empty string. Call has built in procedure to deal with invalid events

* **Optional:**

    `eventId=[string]`
* 
    `eventTimestamp=[string]`
* 
    `eventType=[string]`
* 
    `parentEventId=[string]`
* 
    `userId=[string]`
* 
    `advertiserId=[string]`
* 
    `deviceId=[string]`
* 
    `price=[string]`

* **Success Response:**

  Successfull response will store the events in either server or user events csv file. 

    * **Code:** 200 <br />

* **Error Response:**

    * **Code:** 200 <br />

    We could try some other code here but for simplicity returned code is still HTTP 200 but error message describes type of issue with sent values.

* **Sample Call:**

  http://127.0.0.1:5000/event_collector?eventId=event1&eventTimestamp=10:00&parentEventId=&userId=user1&advertiserId=adv1&deviceId=&price=10


## Set up and run project

----

First thing is set up docker image and run the REST API:

After cloning up project , make sure that you have docker installed. Then enter the cloned project and type:

`make docker`

This will create a docker image with all code and necessary dependencies.

Command:

`make run-docker`

Will start Event Processing REST API server running and waiting for events.

Now you can either run you own client script (in new terminal) that sends events to the Event Collector server or you can run script called `development_client.py` which will create some sample requests to server. 
If you want to run provided script first please find out the docker instance name with:

`docker ps`

And find the **NAMES** value.

Run from you host systemdocker :

`docker exec <NAME> python development_client.py`

Which will send some sample events (from task assignment) to server and 2 files: serving_events.csv and user_events.csv will be created in **output** folder.

If you want to retrieve these files , please type from your terminal(host system , not in docker instance):

`docker cp <NAME>:/output/serving_events.csv .`

`docker cp <NAME>:/output/user_events.csv .`

### Generate validated_events.csv

From your host system please run:

`docker exec <NAME> python event_validation.py`


And retrieve resulting csv file with:

`docker cp <NAME>:/output/validated_events.csv .`


# TESTS

Tests are located in **tests** folder. Through github actions with every push to branch both unity and integration tests will be run. 

| Module  | statements   | missing |    excluded | coverage  |
|---|---------------------|----------|-----|---|
| event_validation.py  | 25                  | 2        | 0   |  92% |
| event_collector_server.py  | 34                  | 6        | 0   | 82%  |
|  Total | 59                  | 8        | 0   |  86% |

Tests can be run by invoking:

`make test`

This will generate a codecov file from which it is possible to generate (coverage html) html file.







