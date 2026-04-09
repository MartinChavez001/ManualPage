import os
import dotenv
import stripe

# config env

dotenv.load_dotenvS()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

stripe.api_key = STRIPE_SECRET_KEY

def create_payment_method():
    payment_method = stripe.PaymentMethod.create(
        type="card",
        card={"token": "tok_visa"}
    )
    return payment_method.id

def create_payment(payment_method_id):
    payment = stripe.PaymentIntent.create(
        amount= 5 * 100
        currency="usd"
        payment_method=payment_method_id
        confirm=True
    )