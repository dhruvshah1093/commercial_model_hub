import pytest
from unittest.mock import patch, MagicMock
from core.kafka_utils.producer import KafkaProducerWrapper
from core.kafka_utils.consumer import KafkaConsumerWrapper


@patch("core.kafka_utils.producer.Producer")
def test_kafka_producer_send(mock_producer_class):
    mock_producer = MagicMock()
    mock_producer_class.return_value = mock_producer

    producer = KafkaProducerWrapper()
    producer.send("test_topic", key="123", value="hello")

    mock_producer.produce.assert_called_once()
    mock_producer.flush.assert_called_once()

@patch("core.kafka_utils.consumer.Consumer")
def test_kafka_consumer_callback_called(mock_consumer_class):
    mock_consumer = MagicMock()
    mock_msg = MagicMock()
    mock_msg.key.return_value = b"test-key"
    mock_msg.value.return_value = b"test-value"
    mock_msg.error.return_value = None

    mock_consumer.poll.side_effect = [mock_msg, None, KeyboardInterrupt()]
    mock_consumer_class.return_value = mock_consumer

    received = {}

    def callback(key, value):
        received["key"] = key
        received["value"] = value

    consumer = KafkaConsumerWrapper("test_topic", group_id="group-test")
    consumer.consume_messages(callback)

    assert received == {"key": "test-key", "value": "test-value"}

