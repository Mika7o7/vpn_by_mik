import yookassa
from yookassa import Payment
import uuid
from config import YOOKASSA_ID, YOOKASSA_API

yookassa.Configuration.account_id = YOOKASSA_ID
yookassa.Configuration.secret_key = YOOKASSA_API

def create(amount, chat_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            'value': amount,
            'currency': "RUB"
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': 'https://t.me/WhiteRa661tBot'
        },
        'capture': True,
        'metadata': {
            'chat_id': chat_id
        },
        'description': f'Пополнение баланса бота на сумму {amount}'
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id

def check(payment_id):
    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == 'succeeded':
        return payment.amount.value
    else:
        return False