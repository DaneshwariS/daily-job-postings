# -*- coding: utf-8 -*-
"""
LinkedIn Job Fetch – Automated Daily Job Alerts (1-2 YOE, Bangalore)
"""

import feedparser
import pandas as pd
from datetime import datetime
import pytz
import os
import smtplib
from email.message import EmailMessage

# ------------------------------
# Step 1: Define RSS Feed URL
# ------------------------------
rss_url = "https://news.google.com/rss/search?q=Data+Scientist+1-2+years+Bangalore+site:linkedin.com/jobs"
feed = feedparser.parse(rss_url)

# ------------------------------
# Step 2: Filter Jobs by Today
# ------------------------------
india_time = datetime.now(pytz.timezone("Asia/Kolkata"))
today_str = india_time.strftime('%a, %d %b %Y')  # Format like: 'Mon, 16 Jun 2025'

job_list = []
for entry in feed.entries:
    if entry.published.startswith(today_str):
        job_list.append({
            "Title": entry.title,
            "Link": entry.link,
            "Published Date": entry.published
        })

# ------------------------------
# Step 3: Save to Excel
# ------------------------------
df = pd.DataFrame(job_list)
output_file = f"LinkedIn_DataScientist_Jobs_Bangalore_{india_time.strftime('%Y-%m-%d')}.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Saved {len(df)} job(s) posted today ({today_str}) to '{output_file}'")

# ------------------------------
# Step 4: Send Email with Excel
# ------------------------------
def send_email_with_attachment(subject, body, to_email, attachment_path):
    EMAIL_ADDRESS = os.environ.get("EMAIL_SENDER")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise Exception("❌ Missing email credentials. Set them in GitHub Secrets.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print(f"📧 Email sent to {to_email} with attachment '{attachment_path}'")

# 🔁 Call the email function
send_email_with_attachment(
    subject="📋 Your Daily LinkedIn Job Feed (Bangalore – 1–2 YOE)",
    body="Hi,\n\nAttached is your daily LinkedIn job listing for Data Scientist roles (1-2 years experience) in Bangalore.\n\nRegards,\nGitHub Bot 🤖",
    to_email="your_email@gmail.com",   # 🔁 REPLACE with your actual email
    attachment_path=output_file
)
