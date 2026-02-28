import aio_pika
import json
from app.config import settings

async def publish_task(queue_name: str, message: dict):
    """Publish a task to RabbitMQ."""
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=queue.name,
        )
    return True

async def consume_tasks(queue_name: str, callback):
    """Start consuming tasks from RabbitMQ."""
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.consume(callback)
    return connection
