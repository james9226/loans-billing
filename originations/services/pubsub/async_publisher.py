from datetime import datetime
import json
import asyncio
from google.cloud import pubsub_v1
from originations.config.config import settings
from originations.services.logging import log_handler
from typing import Any, Optional


def nullable(type: str, value: Optional[Any] = None) -> Optional[dict]:
    if not value:
        return value
    else:
        return {type: value}


async def publish_message(
    message_json: dict, topic_id: str, project_id: str = settings.project_id
) -> None:
    # Create a publisher client
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

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
                log_handler.error(f"Publishing {data} raised an exception: {e}")

        return callback

    # Publish the message asynchronously
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, publisher.publish, topic_path, message_data)
    future.add_done_callback(get_callback(future, message_data))

    # Wait for the message to be sent
    await future


async def publish_batch_messages(
    messages_json: list[dict], topic_id: str, project_id: str = settings.project_id
) -> None:
    # Create a publisher client
    publisher = pubsub_v1.PublisherClient(
        batch_settings=pubsub_v1.types.BatchSettings()
    )
    topic_path = publisher.topic_path(project_id, topic_id)

    # Encode the messages as JSON strings
    message_data_list = [
        json.dumps(
            msg
            | {
                "event_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
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
                log_handler.error(f"Publishing {data} raised an exception: {e}")

        return callback

    # Publish the messages asynchronously in a batch
    futures = []
    loop = asyncio.get_event_loop()
    for message_data in message_data_list:
        future = loop.run_in_executor(None, publisher.publish, topic_path, message_data)
        future.add_done_callback(get_callback(future, message_data))
        futures.append(future)

    # Wait for all messages to be sent
    await asyncio.gather(*futures)
