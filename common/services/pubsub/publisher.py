import asyncio
from datetime import datetime
import json
from logging import Logger
from google.cloud import pubsub_v1

pub_sub_publisher = None


def initialize_pub_sub_publisher(project_id: str, logger: Logger):
    global pub_sub_publisher
    pub_sub_publisher = PubSubPublisher(project_id, logger)


def get_pub_sub_publisher():
    if pub_sub_publisher is None:
        raise Exception("PubSubPublisher has not been initialized.")
    return pub_sub_publisher


class PubSubPublisher:
    def __init__(self, project_id: str, logger):
        self.project_id = project_id
        self.logger = logger
        self.publisher = pubsub_v1.PublisherClient()

    def publish_message_sync(self, message_json: dict, topic_id: str) -> None:
        topic_path = self.publisher.topic_path(self.project_id, topic_id)

        # Encode the message as a JSON string
        message_json["event_time"] = (
            datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        )

        message_data = json.dumps(message_json).encode("utf-8")
        future = self.publisher.publish(topic_path, message_data)
        future.result()

    async def publish_message_async(self, message_json: dict, topic_id: str) -> None:
        # Create a publisher client
        topic_path = self.publisher.topic_path(self.project_id, topic_id)

        # Encode the message as a JSON string
        message_json["event_time"] = (
            datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        )

        message_data = json.dumps(message_json).encode("utf-8")

        # Define the callback function for async publishing
        def get_callback(future, data):
            def callback(future):
                try:
                    pass
                except Exception as e:
                    self.logger.error(f"Publishing {data} raised an exception: {e}")

            return callback

        # Publish the message asynchronously
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(
            None, self.publisher.publish, topic_path, message_data
        )
        future.add_done_callback(get_callback(future, message_data))

        # Wait for the message to be sent
        await future

    async def publish_batch_messages_async(
        self, messages_json: list[dict], topic_id: str
    ) -> None:
        topic_path = self.publisher.topic_path(self.project_id, topic_id)

        # Encode the messages as JSON strings
        message_data_list = [
            json.dumps(
                msg
                | {
                    "event_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[
                        :-3
                    ]
                    + "Z"
                }
            ).encode("utf-8")
            for msg in messages_json
        ]

        # Define the callback function for async publishing
        def get_callback(future, data):
            def callback(future):
                try:
                    pass
                except Exception as e:
                    self.logger.error(f"Publishing {data} raised an exception: {e}")

            return callback

        # Publish the messages asynchronously in a batch
        futures = []
        loop = asyncio.get_event_loop()
        for message_data in message_data_list:
            future = loop.run_in_executor(
                None, self.publisher.publish, topic_path, message_data
            )
            future.add_done_callback(get_callback(future, message_data))
            futures.append(future)

        # Wait for all messages to be sent
        await asyncio.gather(*futures)
