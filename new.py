import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- WhatsApp Cloud API Config ---
ACCESS_TOKEN = "xxxxxx"
PHONE_NUMBER_ID = "xxxxxx"
VERIFY_TOKEN = "xxxx"

# --- Helper: Convert Google Drive link ---
def convert_google_drive_link(link):
    """
    Converts a Google Drive share link into a direct download link
    """
    if "drive.google.com" in link and "/file/d/" in link:
        try:
            file_id = link.split("/file/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        except:
            return link  # fallback
    return link

# --- Function to send text messages ---
def send_message(to, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Message response:", response.json())
    return response.json()

# --- Function to send PDF documents ---
def send_pdf(to, pdf_url, filename="file.pdf"):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "document",
        "document": {
            "link": pdf_url,
            "filename": filename
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    print("PDF response:", response.json())
    return response.json()

# --- Function to send service menu ---
def send_service_menu(to):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {
                "text": "📋 Here are the services offered by Company *:\n\nPlease select one:"
            },
            "action": {
                "button": "View Services",
                "sections": [
                    {
                    "title": "Our Services",
                    "rows": [
                        {"id": "large_format", "title": "Large Format", "description": "Banners, posters, and graphics"},
                        {"id": "digital_offset", "title": "Digital/Offset", "description": "Business cards, flyers, brochures"},
                        {"id": "vehicle_branding", "title": "Vehicle Branding", "description": "Custom car wraps and branding"},
                        {"id": "signage", "title": "Signage", "description": "Lightboxes, banners, hoardings"},
                        {"id": "events", "title": "Events & Exhibitions", "description": "Event & exhibition branding"},
                        {"id": "packaging", "title": "Packaging", "description": "Custom packaging production"},
                        {"id": "carpentry_acrylic", "title": "Carpentry & Acrylic", "description": "Stands, display carpentry & acrylic works"}
                        ]
                    }
                ]
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Menu response:", response.json())
    return response.json()

# --- Basic reply for general queries ---
def get_reply(user_text):
    user = user_text.lower()
    if any(g in user for g in ["hi", "hello", "hey"]):
        return (
            "Hi, how are you? 👋 This is Al Sharjah Neon & Printing Press LLC WhatsApp bot.\n\n"
            "You can use this chatbot to:\n"
            "- Ask about our services by typing 'services'\n"
            "- Get our contact number, email, or address\n"
            "- Request brochures for services like Signage, Vehicle Branding, or Carpentry & Acrylic Display\n\n"
            "Just type what you want to know or select a service from the menu when prompted!"
            "Or connect to a live agent for assistance."
        )
    elif "name" in user:
        return "Our company name is Al Sharjah Neon & Printing Press LLC."
    elif "phone" in user or "contact number" in user:
        return "📞 You can reach us at +971-4-2676568."
    elif "email" in user:
        return "📧 You can email us at sales@sharjahadvertising.com or support@sharjahadvertising.com."
    elif "website" in user:
        return "🌐 Check out our website: www.sharjahadvertising.com"
    elif "address" in user or "location" in user:
        return "📍 We are located at Al Ghusais, Industrial Area 3, near Mashreq Bank, Dubai, UAE (P.O. Box 111109)."
    elif "hours" in user or "working hours" in user:
        return "🕒 Our working hours: Monday to Saturday, 08:00 AM - 06:00 PM. Sunday closed."
    elif "services" in user:
        return None  # Trigger interactive menu
    else:
        return "This is Al Sharjah Neon & Printing Press LLC bot. Please ask about our services, contact, or location."

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

                # ✅ Avoid replying to itself
                if from_number == bot_number:
                    return "ok", 200

                if msg["type"] == "text":
                    user_text = msg["text"]["body"]

                    # If user asks for services, show menu
                    if "services" in user_text.lower():
                        send_service_menu(from_number)
                    else:
                        reply_text = get_reply(user_text)
                        if reply_text:
                            send_message(from_number, reply_text)

                elif msg["type"] == "interactive":
                    service_id = msg["interactive"]["list_reply"]["id"]

                    services_details = {
                       "large_format": "✅ Large Format Printing: High-quality banners, posters, and graphics.",
                        "digital_offset": "✅ Digital & Offset Printing: Business cards, flyers, brochures, and more.",
                        "vehicle_branding": "✅ Vehicle Branding: Custom car wraps and graphics for all types of vehicles.",
                        "signage": "✅ Signage: Lightboxes, banners, hoardings, and more.",
                        "events": "✅ Event & Exhibition Production: Complete event branding & production.",
                        "packaging": "✅ Packaging Solutions: Custom packaging design & production.",
                        "carpentry_acrylic": "✅ Carpentry & Acrylic Display: Creative carpentry for stands & displays, plus acrylic fabrication and signage."
                    }

                    reply_text = services_details.get(service_id, "❌ Sorry, I didn’t recognize that service.")
                    send_message(from_number, reply_text)

                    # 📎 Special case: if Signage, also send PDF
                    if service_id == "signage":
                        pdf_url = "xxxxxx"  # replace with your real GDrive link
                        direct_pdf_url = convert_google_drive_link(pdf_url)
                        send_pdf(from_number, direct_pdf_url, filename="Signage_Brochure.pdf")
                    
                    if service_id == "vehicle_branding":
                        pdf_url = "xxxx"  # Vehicle branding brochure
                        direct_pdf_url = convert_google_drive_link(pdf_url)
                        send_pdf(from_number, direct_pdf_url, filename="Vehicle_Branding_Brochure.pdf")

                    if service_id == "carpentry_acrylic":
                        pdf_url = "xxxxxx"
                        direct_pdf_url = convert_google_drive_link(pdf_url)
                        send_pdf(from_number, direct_pdf_url, filename="Carpentry_Acrylic_Brochure.pdf")
    # 📎 Events & Exhibitions PDF
                if service_id == "events":
                    pdf_url = "xxxxx"
                    direct_pdf_url = convert_google_drive_link(pdf_url)
                    send_pdf(from_number, direct_pdf_url, filename="Events_Brochure.pdf")
                if service_id == "large_format":
                    pdf_url = "xxxxx"
                    direct_pdf_url = convert_google_drive_link(pdf_url)
                    send_pdf(from_number, direct_pdf_url, filename="Large_Format_Brochure.pdf")
                if service_id == "digital_offset":
                    pdf_url = "xxxxx"
                    direct_pdf_url = convert_google_drive_link(pdf_url)
                    send_pdf(from_number, direct_pdf_url, filename="Digital_Offset_Brochure.pdf")
                if service_id == "packaging":
                    pdf_url = "xxxx"
                    direct_pdf_url = convert_google_drive_link(pdf_url)
                    send_pdf(from_number,direct_pdf_url, filename="Packaging_Brochure.pdf")
        except Exception as e:
            print("Error:", e)

        return "ok", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
