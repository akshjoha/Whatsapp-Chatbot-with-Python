# Whatsapp-Chatbot-with-Python
Automated Whatsapp Chatbot with Python 

A WhatsApp bot built with **Flask** and **WhatsApp Cloud API** that allows users to interact with your services and receive brochures directly on WhatsApp. This version features **generic services** named `Service 1` → `Service 7`.

---

## Features

- Automatic replies to greetings and common queries (phone, email, address, working hours, etc.)
- Interactive **services menu** with 7 generic services.
- Sends PDF brochures for each service individually.
- Converts Google Drive share links into direct download links for PDF delivery.
- Ready to deploy on any server running Python 3.8+ with ngrok.
---

## Prerequisites

- Python 3.8+
- pip
- ngrok (for local testing)
- WhatsApp Cloud API credentials

---
## Installation 

# Install all required Python packages using pip:
pip install Flask requests python-dotenv

## 2️⃣ Setup Environment Variables

Obtain WhatsApp Cloud API Credentials

To interact with WhatsApp Cloud API, you need:

Access Token (Authorization Code)

Phone Number ID (Developer Code)

Webhook Verification Token (you can create any string)

Steps:

Go to Meta for Developers

Create an app and set up WhatsApp Cloud API.

Copy the Access Token (Authorization Code) and Phone Number ID (Developer Code) from your WhatsApp app settings.

Paste it in this part of the code: 
{
WHATSAPP_ACCESS_TOKEN= your_access_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
WHATSAPP_VERIFY_TOKEN=your_verify_token_here
}

3️⃣ Run the Bot Locally

Start the Flask server:
python Python whatsapp bot.py

The bot will run on:
http://localhost:5000








