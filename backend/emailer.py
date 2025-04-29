# emailer.py
import smtplib
from email.message import EmailMessage
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "yourcompany@gmail.com"
EMAIL_PASSWORD = "your-app-password"  # Use app-specific password

def send_demo_email(data: dict):
    recipient = data.get("to")
    business_name = data.get("name", "Your Business")
    preview_url = data.get("preview_url", "#")
    contact_name = data.get("contact_name", "there")

    if not recipient or not preview_url:
        return {"error": "Missing recipient email or preview URL."}

    subject = f"{business_name} - Your Website Demo is Ready!"
    body = f"""
Hi {contact_name},

We noticed {business_name} doesn’t have an online presence yet, so we went ahead and designed a sample one-page website for you.

🔗 Click below to view your live demo site:
{preview_url}

This is just a preview — you can fully customize it. If you're interested in a full build, simply reply to this email or call us.

💸 Pricing starts from R1499, with hosting, email setup, and mobile support included.

Looking forward to helping you get online!

Best,  
WebPulse AI Team  
"""

    # Compose the email
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = recipient
    msg.set_content(body)

    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        return {"message": "Demo email sent successfully"}
    except Exception as e:
        return {"error": f"Failed to send email: {str(e)}"}
