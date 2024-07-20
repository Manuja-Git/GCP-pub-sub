from google.cloud import pubsub_v1
import psycopg2
import os

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
subscription_name = "my-subscription"

def callback(message):
    message_data = message.data.decode("utf-8")

    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=5432,
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (content) VALUES (%s)", (message_data,))
    connection.commit()

    message.ack()

if __name__ == "__main__":
    credentials_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    subscriber.subscribe(subscription_path, callback=callback)

    while True:
        pass
