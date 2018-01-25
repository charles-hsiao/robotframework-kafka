*** Settings ***
Library           ../Lib/Lib_Kafka.py    WITH NAME    Kafka
Resource          Config.robot

*** Test Cases ***
Kafka_Producer
    [Documentation]    *Produce event/events to Kafka*
    ...
    ...    event_producer(host_kafka, topic, event_content_arr, wait_ack=False)
    ${Event.Arr}=    Create List    Event_A    Event_B,A    DDDDC,A,"B"
    ${Topic.Produce}=    Set Variable    test
    ${WaitAck}=    Set Variable    FALSE
    ${ProduceResult}=    Kafka.event_producer    ${Kafka.Host}    ${Topic.Produce}    ${Event.Arr}    ${WaitAck}
    Log    Produce result: ${ProduceResult}

Kafka_Consumer_MatchAll
    [Documentation]    *Consume event from kafka/zookeeper, waiting for the event content assertion partially match*
    ...
    ...    event_consumer(host_kafka, host_zookeeper, topic, assertion_event_content, match_partially=False, timeout_sec=20)
    ${Topic.Consume}=    Set Variable    test
    ${Event.ContentAssertion}=    Set Variable    Event_A
    ${MatchPartially}=    Set Variable    ${FALSE}    # Python False
    ${Timeout}=    Set Variable    20
    ${ConsumeResult}=    Kafka.event_consumer    ${Kafka.Host}    ${Zookeeper.Host}    ${Topic.Consume}    ${Event.ContentAssertion}    ${MatchPartially}
    ...    ${Timeout}
    Log    Consume result: ${ConsumeResult}
    Should Be Equal As Strings    ${ConsumeResult}    GotEvent

Kafka_Consumer_MatchPartially
    [Documentation]    *Consume event from kafka/zookeeper, waiting for the event content assertion match all*
    ...
    ...    event_consumer(host_kafka, host_zookeeper, topic, assertion_event_content, match_partially=False, timeout_sec=20)
    ${Topic.Consume}=    Set Variable    test
    ${Event.ContentAssertion}=    Set Variable    B
    ${MatchPartially}=    Set Variable    ${TRUE}    # Python True
    ${Timeout}=    Set Variable    20
    ${ConsumeResult}=    Kafka.event_consumer    ${Kafka.Host}    ${Zookeeper.Host}    ${Topic.Consume}    ${Event.ContentAssertion}    ${MatchPartially}
    ...    ${Timeout}
    Log    Consume result: ${ConsumeResult}
    Should Be Equal As Strings    ${ConsumeResult}    GotEvent

Kafka_Consumer_Multiple_MatchPartially
    [Documentation]    *Consume event from kafka/zookeeper, waiting for the event content assertion match all the array list*
    ...
    ...    event_consumer_multiple_match_partially(host_kafka, host_zookeeper, topic, assertion_event_content_arr, timeout_sec=20)
    ${Topic.Consume}=    Set Variable    test
    ${Assertion_Arr}=    Create List    A    B    C
    ${Timeout}=    Set Variable    20
    ${ConsumeResult}=    Kafka.event_consumer_multiple_match_partially    ${Kafka.Host}    ${Zookeeper.Host}    ${Topic.Consume}    ${Assertion_Arr}    ${Timeout}
    Log    Consume result: ${ConsumeResult}
    Should Be Equal As Strings    ${ConsumeResult}    GotEvent

Kafka_Consume_ToLatest
    [Documentation]    *Consume event from kafka/zookeeper to the latest offset*
    ...
    ...    event_consume_to_latest(host_kafka, host_zookeeper, topic)
    ${Topic.Consume}=    Set Variable    test
    ${ConsumeResult}=    Kafka.event_consume_to_latest    ${Kafka.Host}    ${Zookeeper.Host}    ${Topic.Consume}
    Log    Consume result: ${ConsumeResult}
    Should Be Equal As Strings    ${ConsumeResult}    ConsumeDone
