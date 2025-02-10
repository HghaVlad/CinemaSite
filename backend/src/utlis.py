from schemas.Payment import UserPayment
from models.payments import PaymentStatus
from random import randint


def process_payment(payment: UserPayment) -> PaymentStatus:
    if payment.cvv == 123 and payment.card_number == "1234567890123456" and payment.card_holder == "John Doe":
        return PaymentStatus.SUCCESS
    elif payment.cvv == 000 or len(payment.card_number) < 16 or payment.card_number == "0000000000000000" or len(payment.card_holder) < 3:
        return PaymentStatus.ERROR

    if randint(0, 1) == 0:
        return PaymentStatus.NOT_ENOUGH_MONEY

    return PaymentStatus.FAILED

