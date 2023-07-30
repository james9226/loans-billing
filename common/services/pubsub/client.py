from google.cloud import pubsub_v1
import threading


async def setup_pub_sub_subscription(project_id, subscription_id, callback):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        future.result()
    except Exception as e:
        future.cancel()
        print(f"Subscription cancelled due to {e}.")

    thread = threading.Thread(target=setup_pub_sub_subscription)
    thread.start()
