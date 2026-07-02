import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import stripe

# Stripe key ko env se read karna
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    email: str

@app.post("/create-checkout-session")
async def create_checkout_session(item: Item):
    try:
        # Asli Stripe checkout session banana
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Ultimate Digital Toolkit',
                    },
                    'unit_amount': 39900, # ₹399.00 (paise me)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://digital-toolkit-frontend.vercel.app',
            cancel_url='https://digital-toolkit-frontend.vercel.app',
            customer_email=item.email
        )
        return {"id": session.id}
    except Exception as e:
        return {"error": str(e)}
