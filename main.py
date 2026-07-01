from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
import os
import webbrowser
from threading import Timer

app = FastAPI()

def get_frontend_html():
    html_path = "/storage/emulated/0/Download/index.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: Download folder me index.html nahi mili! Check karein ki file Download folder me hi saved hai na?</h1>"

@app.get("/", response_class=HTMLResponse)
def home():
    return get_frontend_html()

@app.post("/payment-webhook")
async def payment_webhook(request: Request):
    payload = await request.json()
    if payload.get("event") == "payment.captured":
        payment_entity = payload["payload"]["payment"]["entity"]
        customer_email = payment_entity.get("email", "")
        customer_name = payment_entity.get("notes", {}).get("name", "Customer")
        
        print(f"📧 Sending premium product to {customer_email}...")
        print(f"Hey {customer_name}, here is your download link: https://yoursecurestorage.com/download/ultimate-ai-kit.zip")
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Invalid Event")

# Auto browser open karne ke liye function
def open_browser():
    webbrowser.open("http://localhost:8000/")

if __name__ == "__main__":
    # Server chalu hone ke 2 second baad automatic browser khulega
    Timer(2, open_browser).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
