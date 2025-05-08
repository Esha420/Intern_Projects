from fastapi import FastAPI
from app.routes import wallet
from fastapi.middleware.cors import CORSMiddleware
import logging


app = FastAPI()

# Enable CORS if your GUI or frontend is running separately (e.g., on a browser or another port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify allowed origins like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the wallet router under the /wallet prefix
app.include_router(wallet.router, prefix="/wallet", tags=["wallet"])

@app.get("/")
def root():
    return {"message": "Wallet API is running"}

logging.basicConfig(level=logging.DEBUG)
