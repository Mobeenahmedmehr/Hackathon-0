import base64
import html
from bs4 import BeautifulSoup


def parse_email_payload(payload):
    """
    Extract clean message text from Gmail API payload.

    Args:
        payload: Gmail API payload object

    Returns:
        Clean text content of the email
    """
    body_text = ""

    # Handle different payload structures
    if 'parts' in payload:
        # Email with parts (multipart)
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                # Plain text part
                data = part['body']['data']
                decoded_data = base64.urlsafe_b64decode(data.encode('ASCII'))
                body_text += decoded_data.decode('utf-8')
                break  # Take the first plain text part
            elif part['mimeType'] == 'text/html':
                # HTML part - convert to plain text
                data = part['body']['data']
                decoded_data = base64.urlsafe_b64decode(data.encode('ASCII'))
                html_content = decoded_data.decode('utf-8')

                # Parse HTML and extract text
                soup = BeautifulSoup(html_content, 'html.parser')
                body_text += soup.get_text()
                break  # Take the first HTML part if no plain text found
    else:
        # Simple message with no parts
        if 'body' in payload and 'data' in payload['body']:
            data = payload['body']['data']
            decoded_data = base64.urlsafe_b64decode(data.encode('ASCII'))
            body_text = decoded_data.decode('utf-8')

            # If the body looks like HTML, convert it to plain text
            if '<html>' in body_text.lower() or '<body>' in body_text.lower():
                soup = BeautifulSoup(body_text, 'html.parser')
                body_text = soup.get_text()

    # Clean up the text
    # Remove extra whitespace and newlines
    body_text = '\n'.join(line.strip() for line in body_text.split('\n') if line.strip())

    # Unescape HTML entities
    body_text = html.unescape(body_text)

    return body_text