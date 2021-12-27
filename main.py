import pika

host = "myrtle-white-bonobo.rmq2.cloudamqp.com"
user = "ldjhoazs"
password = "RuExar1Jwk-8jILvZrRkbKVu_uQt5T6e"
# queue_dlq = ""
queues: [] = ['pp.payments.braspag.create',
              'pp.payments.braspag.create_fail',
              'pp.payments.braspag.created',
              'pp.payments.braspag.created_fail',
              'pp.payments.braspag.cancel',
              'pp.payments.braspag.cancel_fail',
              'pp.payments.braspag.canceled',
              'pp.payments.braspag.canceled_fail']
credentials = pika.PlainCredentials(user, password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host,
        virtual_host="/",
        heartbeat=600,
        blocked_connection_timeout=300,
        credentials=credentials,
    )
)
for item in queues:
    exchange = f"e.{item}"
    queue = f"q.{item}"

    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type="fanout", durable=True)
    # channel.queue_declare(queue=queue_dlq, durable=True, arguments={"x-queue-type": "classic"})
    channel.queue_declare(
        queue=queue,
        durable=True,
        arguments={
            "x-queue-type": "classic",
            # "x-dead-letter-exchange": "",
            # "x-dead-letter-routing-key": queue_dlq,
        },
    )
    channel.queue_bind(exchange=exchange, queue=queue)
