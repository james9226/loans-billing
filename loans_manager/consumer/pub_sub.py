from google.cloud.pubsub_v1.subscriber.message import Message


def consume_loan_event(message: Message):
    print(f"Received {message}.")
    message.ack()
