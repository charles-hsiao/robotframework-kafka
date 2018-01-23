## Lib_Kafka
### Introduction
Lib_Kafka is a python library for Robotframework to test Kafka. It's based on open source project [pykafka](https://github.com/Parsely/pykafka).

The goal of LibKafka contains:
* Producer: Produce the specific events to Kafka.
* Consumer: Wait the specific event assertion from Kafka.

### Get Started
#### How to use?
```
1. pip install pykafka
2. Including the Lib_Kafka.py in Robotframework script. And start to call the following keyword function from Robotframework.
```
#### Functions - event_consumer
Waiting to get event from Kafka for a period of time from specific topic.

```
String event_consumer(host_kafka, host_zookeeper, topic, assertion_event_content, match_partially=False, timeout_sec=20)
```

#### Parameters
Required | Parameters              | Description                                 | Default Value | Example
-------- | ----------------------- | ------------------------------------------- | ------------- | ------------- 
   O     | host_kafka              | Kafka broker host:IP                        | N/A           | 10.1.1.1:9092
   O     | host_zookeeper          | Zookeeper host:IP                           | N/A           | 10.1.1.1:2181
   O     | topic                   | Topic name for receiving events             | N/A           | test_topic
   O     | assertion_event_content | Specific event content assertion            | N/A           | Stop_event
   X     | match_partially         | Match partially/all event content assertion | False         | True 
   X     | timeout_sec             | Timeout seconds                             | 20            | 30

#### Return Values
Values             | Description
------------------ | -------------------------------------------------------------------
GotEvent           | Got the specific event content from specific topic before timeout
Timeout            | Didn't received specific event content from specific topic timeout
KafkaConnectFailed | Can't connect to specific Kafka host



#### Functions - event_consumer_multiple_match_partially
Waiting to get multiple event assertion of single event from Kafka for a period of time from specific topic.

```
String event_consumer_multiple_match_partially(host_kafka, host_zookeeper, topic, assertion_event_content_arr, timeout_sec=20)
```

#### Parameters
Required | Parameters                  | Description                                 | Default Value | Example
-------- | --------------------------- | ------------------------------------------- | ------------- | ------------- 
   O     | host_kafka                  | Kafka broker host:IP                        | N/A           | 10.1.1.1:9092
   O     | host_zookeeper              | Zookeeper host:IP                           | N/A           | 10.1.1.1:2181
   O     | topic                       | Topic name for receiving events             | N/A           | test_topic
   O     | assertion_event_content_arr | Specific event content assertion            | N/A           | [Stop_event, A, B]
   X     | timeout_sec                 | Timeout seconds                             | 20            | 30

#### Return Values
Values             | Description
------------------ | -------------------------------------------------------------------
GotEvent           | Got all assertion of specific event content from specific topic before timeout
Timeout            | Didn't received specific event content or part of the assertion didn't match from specific topic and reached timeout_sec
KafkaConnectFailed | Can't connect to specific Kafka host



#### Functions - event_single_consumer
Waiting to get single event from Kafka for a period of time from specific topic.

```
String event_single_consumer(host_kafka, host_zookeeper, topic, timeout_sec=20)
```

#### Parameters
Required | Parameters              | Description                                 | Default Value | Example
-------- | ----------------------- | ------------------------------------------- | ------------- | ------------- 
   O     | host_kafka              | Kafka broker host:IP                        | N/A           | 10.1.1.1:9092
   O     | host_zookeeper          | Zookeeper host:IP                           | N/A           | 10.1.1.1:2181
   O     | topic                   | Topic name for receiving events             | N/A           | test_topic
   X     | timeout_sec             | Timeout seconds                             | 20            | 30

#### Return Values
Values             | Description
------------------ | -------------------------------------------------------------------
GotEvent           | Got the specific event content from specific topic before timeout
Timeout            | Didn't received specific event content from specific topic timeout
KafkaConnectFailed | Can't connect to specific Kafka host


#### Functions - event_consume_to_latest
Consume the event from specific topic to latest offset

```
String event_consume_to_latest(host_kafka, host_zookeeper, topic)
```

#### Parameters
Required | Parameters              | Description                                 | Default Value | Example
-------- | ----------------------- | ------------------------------------------- | ------------- | ------------- 
   O     | host_kafka              | Kafka broker host:IP                        | N/A           | 10.1.1.1:9092
   O     | host_zookeeper          | Zookeeper host:IP                           | N/A           | 10.1.1.1:2181
   O     | topic                   | Topic name for receiving events             | N/A           | test_topic

#### Return Values
Values             | Description
------------------ | -------------------------------------------------------------------
ConsumeDone        | Consume the event to the latest offset
Error              | Error when consuming event
KafkaConnectFailed | Can't connect to specific Kafka host


#### Functions - event_producer
Produce the events to Kafka.

```
String event_producer(host_kafka, topic, event_content_arr, wait_ack=False)
```

#### Parameters
Required | Parameters              | Description                                               | Default Value | Example
-------- | ----------------------- | --------------------------------------------------------- | ------------- | ------------- 
   O     | host_kafka              | Kafka broker host:IP                                      | N/A           | 10.1.1.1:9092
   O     | topic                   | Topic name for sending events                             | N/A           | test_topic
   O     | event_content_arr       | Event content array                                       | N/A           | A B C Stop_event
   X     | wait_ack                | While sending the events, should wait for the ack or not. | False         | True 

#### Return Values
Values             | Description
------------------ | -------------------------------------------------------------------
SendSuccess        | All the events is send successfully
SendFailed         | Part of/All of the events send failed
KafkaConnectFailed | Can't connect to specific Kafka host
