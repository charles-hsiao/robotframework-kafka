from pykafka import KafkaClient, exceptions
import logging, time
from robot.api import logger
import re

logging.basicConfig()
# RobotFramework.logger: http://robot-framework.readthedocs.org/en/2.9.2/_modules/robot/api/logger.html


# Print message to RobotFramework console & python output
def msg_print(msg):
    print('[Lib_Kafka] ' + msg)
    logger.info('[Lib_Kafka] ' + msg)


def event_consumer(host_kafka, host_zookeeper, topic, assertion_event_content, match_partially=False, timeout_sec=20):
    try:
        client = KafkaClient(hosts=host_kafka, socket_timeout_ms=10000)
        topic = client.topics[str(topic)]

        consumer = topic.get_balanced_consumer(consumer_group='Group-Lib_Kafka',
                                               auto_commit_enable=True,
                                               zookeeper_connect=host_zookeeper,
                                               consumer_timeout_ms=100)

        msg_print('Consumer started!')
        if not match_partially:
            msg_print('Search with method: Match All')
        else:
            msg_print('Search with method: Match Partially')

        timeout = time.time() + int(timeout_sec)  # timeout seconds from now
        got_msg = False
        while True:
            msg = consumer.consume()
            if msg is not None:
                msg_print('Got event:' + str(msg.offset) + ' - ' + msg.value)
                if not match_partially:
                    if msg.value == assertion_event_content:
                        got_msg = True
                        break
                else:
                    if re.search(assertion_event_content, msg.value):
                        got_msg = True
                        break
            if time.time() > timeout:
                break

        consumer.stop()
        if got_msg:
            return_result = 'GotEvent'
        else:
            return_result = 'Timeout'
    except exceptions.KafkaException:
        return_result = 'KafkaConnectFailed'

    msg_print('Consumer stopped! ' + return_result)
    return return_result


def event_consumer_multiple_match_partially(host_kafka, host_zookeeper, topic, assertion_event_content_arr, timeout_sec=20):
    try:
        client = KafkaClient(hosts=host_kafka, socket_timeout_ms=10000)
        topic = client.topics[str(topic)]

        consumer = topic.get_balanced_consumer(consumer_group='Group-Lib_Kafka',
                                               auto_commit_enable=True,
                                               zookeeper_connect=host_zookeeper,
                                               consumer_timeout_ms=100)

        msg_print('Consumer started!')

        timeout = time.time() + int(timeout_sec)  # timeout seconds from now
        got_msg = False
        while True:
            msg = consumer.consume()
            if msg is not None:
                msg_print('Got event:' + str(msg.offset) + ' - ' + msg.value)
                expect_assertion_count = len(assertion_event_content_arr)
                got_assertion_count = 0
                for assertion in assertion_event_content_arr:
                    if re.search(assertion, msg.value):
                        msg_print('Got assertion:' + assertion)
                        got_assertion_count += 1
                if got_assertion_count == expect_assertion_count:
                    got_msg = True
                    break
            if time.time() > timeout:
                break

        consumer.stop()
        if got_msg:
            return_result = 'GotEvent'
        else:
            return_result = 'Timeout'
    except exceptions.KafkaException:
        return_result = 'KafkaConnectFailed'

    msg_print('Consumer stopped! ' + return_result)
    return return_result


def event_single_consumer(host_kafka, host_zookeeper, topic, timeout_sec=20):
    try:
        client = KafkaClient(hosts=host_kafka, socket_timeout_ms=10000)
        topic = client.topics[str(topic)]

        consumer = topic.get_balanced_consumer(consumer_group='Group-Lib_Kafka',
                                               auto_commit_enable=True,
                                               zookeeper_connect=host_zookeeper,
                                               consumer_timeout_ms=100)

        timeout = time.time() + int(timeout_sec)  # timeout seconds from now
        got_msg = False
        event = ''
        while True:
            msg = consumer.consume()
            if msg is not None:
                msg_print('Got event:' + str(msg.offset) + ' - ' + msg.value)
                event = msg.value
                got_msg = True
                break
            if time.time() > timeout:
                break

        consumer.stop()
        if got_msg:
            return_result = 'GotEvent'
        else:
            return_result = 'Timeout'
    except exceptions.KafkaException:
        return_result = 'KafkaConnectFailed'

    r = {'result': return_result, 'event': event}
    return r


def event_consume_to_latest(host_kafka, host_zookeeper, topic):
    try:
        client = KafkaClient(hosts=host_kafka, socket_timeout_ms=10000)
        topic = client.topics[str(topic)]

        consumer = topic.get_balanced_consumer(consumer_group='Group-Lib_Kafka',
                                               auto_commit_enable=True,
                                               zookeeper_connect=host_zookeeper,
                                               consumer_timeout_ms=100)

        msg_print('Consume to latest offset started!')
        consume_done = False
        while True:
            msg = consumer.consume()
            if msg is not None:
                msg_print('Got event:' + str(msg.offset) + ' - ' + msg.value)
            else:
                consume_done = True
                break

        consumer.stop()
        if consume_done:
            return_result = 'ConsumeDone'
        else:
            return_result = 'Error'
    except exceptions.KafkaException:
        return_result = 'KafkaConnectFailed'

    msg_print('Consumer stopped! ' + return_result)
    return return_result


def event_producer(host_kafka, topic, event_content_arr, wait_ack=False):

    event_num = len(event_content_arr)
    event_sent = 0

    msg_print('Producer started!')

    try:
        client = KafkaClient(hosts=host_kafka, socket_timeout_ms=10000)
        topic = client.topics[str(topic)]

        if bool(wait_ack):
            msg_print('Waiting for ack mode!')
            with topic.get_sync_producer() as producer:  # Waiting for ack
                for event_content in event_content_arr:
                    producer.produce(str(event_content))
                    msg_print('Send event:' + event_content)
                    event_sent += 1
        else:
            msg_print('No waiting for ack mode!')
            with topic.get_producer(delivery_reports=True) as producer: # No waiting for ack
                for event_content in event_content_arr:
                    producer.produce(str(event_content))
                    msg_print('Send event in index ' + str(event_sent) + ' success')
                    event_sent += 1

        if event_num == event_sent:
            return_result = 'SendSuccess'
        else:
            return_result = 'SendFailed'
    except exceptions.KafkaException:
        return_result = 'KafkaConnectFailed'

    msg_print('Producer stopped! ' + return_result)
    return return_result
