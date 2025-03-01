import pika
import sys
from bson import ObjectId
from contact_model import Contact
import connect

def send_sms(phone):
    print(f'Send sms {phone}')

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='sms_queue')

    def callback(ch, method, properties, body):
        contact=Contact.objects.get(id=ObjectId(body.decode()))
        send_sms(contact.phone)
        contact.update(set__done=True)

    channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
