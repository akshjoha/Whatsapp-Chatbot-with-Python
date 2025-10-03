import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

app = Flask(__name__)

# --- WhatsApp Cloud API Config ---
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")


# --- Helper: Convert Google Drive link ---
def convert_google_drive_link(link):
    """
    Converts a Google Drive share link into a direct download link
    """
    if "drive.google.com" in link and "/file/d/" in link:
        try:
            file_id = link.split("/file/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        except Exception:
            return link
    return link


# --- Function to send text messages ---
def send_message(to, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Message response:", response.json())
    return response.json()


# --- Function to send PDF documents ---
def send_pdf(to, pdf_url, filename="file.pdf"):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "document",
        "document": {"link": pdf_url, "filename": filename},
    }
    response = requests.post(url, headers=headers, json=payload)
    print("PDF response:", response.json())
    return response.json()


# --- Function to send service menu ---
def send_service_menu(to):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": "📋 Here are the available services:\n\nPlease select one:"},
            "action": {
                "button": "View Services",
                "sections": [
                    {
                        "title": "Our Services",
                        "rows": [
                            {"id": "service1", "title": "Service 1", "description": "Description for Service 1"},
                            {"id": "service2", "title": "Service 2", "description": "Description for Service 2"},
                            {"id": "service3", "title": "Service 3", "description": "Description for Service 3"},
                            {"id": "service4", "title": "Service 4", "description": "Description for Service 4"},
                            {"id": "service5", "title": "Service 5", "description": "Description for Service 5"},
                            {"id": "service6", "title": "Service 6", "description": "Description for Service 6"},
                            {"id": "service7", "title": "Service 7", "description": "Description for Service 7"},
                        ],
                    }
                ],
            },
        },
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Menu response:", response.json())
    return response.json()


# --- Basic reply for general queries ---
def get_reply(user_text):
    user = user_text.lower()
    if any(g in user for g in ["hi", "hello", "hey"]):
        return (
            "Hi, how are you? 👋 This is the WhatsApp bot.\n\n"
            "You can use this chatbot to:\n"
            "- Ask about our services by typing 'services'\n"
            "- Get our contact number, email, or address\n"
            "- Request brochures for services\n\n"
            "Just type what you want to know or select a service from the menu when prompted!\n"
            "Or connect to a live agent for assistance."
        )
    elif "name" in user:
        return "Our company name is Example Company."
    elif "phone" in user or "contact number" in user:
        return "📞 You can reach us at +1234567890."
    elif "email" in user:
        return "📧 You can email us at example@example.com."
    elif "website" in user:
        return "🌐 Check out our website: https://example.com"
    elif "address" in user or "location" in user:
        return "📍 123 Business Street, City, Country."
    elif "hours" in user or "working hours" in user:
        return "🕒 Our working hours: Monday to Saturday, 08:00 AM - 06:00 PM. Sunday closed."
    elif "services" in user:
        return None
    else:
        return "This is an automated bot. Please ask about our services, contact, or location."


# --- Webhook Verification + Message Handling ---
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Invalid verification token"

    elif request.method == "POST":
        data = request.get_json()
        print("Webhook received:", data)

        try:
            change = data["entry"][0]["changes"][0]["value"]
            bot_number = change["metadata"]["display_phone_number"]

            if "messages" in change:
                msg = change["messages"][0]
                from_number = msg["from"]

                if from_number == bot_number:
                    return "ok", 200

                if msg["type"] == "text":
                    user_text = msg["text"]["body"]

                    if "services" in user_text.lower():
                        send_service_menu(from_number)
                    else:
                        reply_text = get_reply(user_text)
                        if reply_text:
                            send_message(from_number, reply_text)

                elif msg["type"] == "interactive":
                    service_id = msg["interactive"]["list_reply"]["id"]

                    # Send text details
                    services_details = {
                        "service1": "✅ Details for Service 1.",
                        "service2": "✅ Details for Service 2.",
                        "service3": "✅ Details for Service 3.",
                        "service4": "✅ Details for Service 4.",
                        "service5": "✅ Details for Service 5.",
                        "service6": "✅ Details for Service 6.",
                        "service7": "✅ Details for Service 7.",
                    }
                    reply_text = services_details.get(service_id, "❌ Sorry, I didn’t recognize that service.")
                    send_message(from_number, reply_text)

                    # Send PDF individually
                    if service_id == "service1":
                        pdf_url = "https://drive.google.com/file/d/xxxx/view?usp=share_link"
                        direct_pdf_url = convert_google_drive_link(pdf_url)
                        send_pdf(from_number, direct_pdf_url, filename="Service_1_Brochure.pdf")
                    elif service_id == "service2":
                        pdf_url = "https://drive.google.com/file/d/xxxx/view?usp=share_link"
                        direct_pdf_url = convert_google_drive_link(pdf_url)
                        send_pdf(from_number, direct_pdf_url, filename="Service_2_Brochure.pdf")
                    elif service_id == "service3":
                        pdf_url = "https://drive.google.com/file/d/xxxx/view?usp=share_link"
                        direct_pdf_url = convert_google_drive_link(pdf_url)
                        send_pdf(from_number, direct_pdf_url, filename="Service_3_Brochure.pdf")
                    elif service_id == "service4":
                        pdf_url = "https://drive.google.com/file/d/xxxx/view?usp=share_link"
                        direct_pdf_url = convert_google_drive_link(pdf_url)
                        send_pdf(from_number, direct_pdf_url, filename="Service_4_Brochure.pdf")
                    elif service_id == "service5":
                        pdf_url = "https://drive.google.com/file/d/xxxx/view?usp=share_link"
                        direct_pdf_url = convert_google_drive_link(pdf_url)
                        send_pdf(from_number, direct_pdf_url, filename="Service_5_Brochure.pdf")
                    elif service_id == "service6":
                        pdf_url = "https://drive.google.com/file/d/xxxx/view?usp=share_link"
                        direct_pdf_url = convert_google_drive_link(pdf_url)
                        send_pdf(from_number, direct_pdf_url, filename="Service_6_Brochure.pdf")
                    elif service_id == "service7":
                        pdf_url = "https://drive.google.com/file/d/xxxx/view?usp=share_link"
                        direct_pdf_url = convert_google_drive_link(pdf_url)
                        send_pdf(from_number, direct_pdf_url, filename="Service_7_Brochure.pdf")

        except Exception as e:
            print("Error:", e)

        return "ok", 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
