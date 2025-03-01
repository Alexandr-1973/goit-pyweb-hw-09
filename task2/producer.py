import pika
import faker
import random
from contact_model import Contact
import connect

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

fake=faker.Faker()

def main(number_contacts):
    contacts_to_insert = []
    for _ in range(number_contacts):
        contact = Contact(fullname=fake.name(), email=fake.email(), phone=random.randint(1000000000, 9999999999), delivery=random.choice(["sms", "email"]))
        contacts_to_insert.append(contact)
    Contact.objects.insert(contacts_to_insert)
    [channel.basic_publish(exchange='', routing_key=f'{c.delivery}_queue', body=str(c.id)) for c in contacts_to_insert]
    connection.close()


if __name__ == '__main__':
    main(10)


