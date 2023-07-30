from fastapi import FastAPI
from google.cloud import pubsub_v1
from starlette.background import BackgroundTasks
import threading

app = FastAPI()

project_id = "your-project-id"
subscription_id = "your-subscription-id"
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


async def setup_pub_sub_subscription(callback: function):
    future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        future.result()
    except Exception as e:
        future.cancel()
        print(f"Subscription cancelled due to {e}.")

    thread = threading.Thread(target=setup_pub_sub_subscription)
    thread.start()
