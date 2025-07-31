import imaplib
import email
from email.header import decode_header
from datetime import datetime, timezone

def check_account(account, query):
    result = []
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(account["email"], account["password"])

        for folder in ["INBOX", "[Gmail]/Spam"]:
            mail.select(folder)
            _, data = mail.search(None, "ALL")
            ids = data[0].split()[-10:]  # Last 10 emails
            for eid in reversed(ids):
                _, msg_data = mail.fetch(eid, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode(errors="ignore")
                from_ = msg.get("From", "")
                date = email.utils.parsedate_to_datetime(msg["Date"])
                age_seconds = int((datetime.now(timezone.utc) - date).total_seconds())

                if query.lower() in subject.lower() or query.lower() in from_.lower():
                    result.append({
                        "subject": subject,
                        "from": from_,
                        "folder": "Inbox" if "INBOX" in folder else "Spam",
                        "age_seconds": age_seconds,
                        "age_human": f"{age_seconds // 60}m ago"
                    })
        mail.logout()
    except Exception as e:
        print("ERROR:", e)
    return result
