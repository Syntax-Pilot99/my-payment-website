from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="AI Content Creator Kit API",
    version="1.0.0"
)

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route
@app.get("/")
async def home():
    return {
        "status": "System Online",
        "product": "AI Content Creator Kit API"
    }

# Payment Webhook
@app.post("/payment-webhook")
async def payment_webhook(request: Request):
    try:
        payload = await request.json()

        if payload.get("event") == "payment.captured":
            payment = payload.get("payload", {}).get("payment", {}).get("entity", {})

            customer_email = payment.get("email", "No Email")

            print(f"SUCCESS: Sending product to {customer_email}")

            return {
                "status": "success",
                "message": f"Product link triggered for {customer_email}"
            }

        return {
            "status": "ignored",
            "message": "Event is not payment.captured"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Webhook Error: {str(e)}"
        )

# Run Server
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
