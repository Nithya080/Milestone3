import smtplib
from email.mime.text import MIMEText

def send_email(results, url, score):
    # Filter High & Critical
    high_critical = [r for r in results if r["severity"] in ["High", "Critical"]]

    # 🔥 TEMP: force email for testing (REMOVE LATER)
    # if not high_critical:
    #     return

    html = f"""
    <h2 style="color:red;">🚨 Vulnerability Alert</h2>
    <p><b>Target:</b> {url}</p>
    <p><b>Risk Score:</b> {score}</p>

    <table border="1" cellpadding="5">
        <tr>
            <th>Name</th>
            <th>Severity</th>
        </tr>
    """

    # If no high/critical, show all (for testing)
    display_data = high_critical if high_critical else results

    for r in display_data:
        html += f"<tr><td>{r['name']}</td><td>{r['severity']}</td></tr>"

    html += "</table>"

    html += """
    <p><b>Recommended Action:</b> Fix vulnerabilities immediately.</p>
    <p><i>This is an automated alert.</i></p>
    """

    msg = MIMEText(html, "html")

    # 🔴 CHANGE THIS
    msg["From"] = "nithyasripunugoti@gmail.com"
    msg["To"] = "nithyasripunugoti@gmail.com"   # send to yourself
    msg["Subject"] = f"🚨 ALERT: {url}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        print("Logging in...")

       
        server.login(
            "nithyasripunugoti@gmail.com",      
            "jeavejheejydmbcu"         
        )

        print("Sending email...")

        server.send_message(msg)
        server.quit()

        print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ Email failed:", e)