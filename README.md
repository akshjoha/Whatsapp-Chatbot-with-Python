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

4️⃣ Expose Local Server with ngrok (for WhatsApp webhook)

# Register on ngrok

1. Go to https://ngrok.com/
2. Click Sign Up and create a free account.
3. Verify your email and log in to your ngrok dashboard.
4. Download and install ngrok: https://ngrok.com/download
5. Unzip the file and place the ngrok executable in a folder accessible via your system PATH.
6.In your ngrok dashboard, go to Auth section to get your Authtoken.
7.Run the following command in your terminal: ngrok config add-authtoken YOUR_AUTHTOKEN_HERE -This links ngrok to your account so you can use advanced features like static domains.
8. Go to your ngrok dashboard → Domain / Static Domains.
9. Copy the static domain URL provided by ngrok (e.g., https://mybot.ngrok-free.app)- This URL will remain the same even after restarting ngrok, unlike the temporary URL.
10. Set this static URL as your WhatsApp Cloud API webhook:
11. https://mybot.ngrok-free.app/webhook
12. Go to your ngrok dashboard → Connections to see live tunnels.
13. Now open terminal or Cmd and type this ngrok http 5000 --domain your-domain.ngrok-free.app
14. ✅ After this, your Flask bot is publicly accessible, and WhatsApp can send messages to your webhook.



