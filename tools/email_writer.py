import re
from typing import Dict, Any
import json
import os

class EmailWriter:
    def __init__(self):
        self.templates_dir = "./data/email_templates"
        os.makedirs(self.templates_dir, exist_ok=True)
        self.templates = self._load_templates()
    
    async def generate(self, message: str) -> str:
        """Generate an email based on the message."""
        # Extract email type and key information
        email_type = self._determine_type(message)
        info = self._extract_info(message)
        
        # Get template
        template = self.templates.get(email_type, self.templates["default"])
        
        # Fill template with information
        email = template.format(**info)
        
        return f"""
Oluşturulan E-posta:

Konu: {info['subject']}

{email}

Saygılarımla,
{info['sender']}
"""
    
    def _determine_type(self, message: str) -> str:
        """Determine the type of email to generate."""
        message = message.lower()
        if "vergi" in message or "beyanname" in message:
            return "tax_notice"
        elif "fatura" in message:
            return "invoice_notice"
        elif "hatırlatma" in message or "ödeme" in message:
            return "payment_reminder"
        else:
            return "default"
    
    def _extract_info(self, message: str) -> Dict[str, str]:
        """Extract key information from the message."""
        info = {
            "recipient": "Sayın İlgili",
            "subject": "Bilgilendirme",
            "sender": "Mali Müşavir",
            "date": "",
            "amount": "",
            "deadline": ""
        }
        
        # Extract recipient
        recipient_match = re.search(r'(?:için|to|kime)[:\s]+([^,\n]+)', message, re.I)
        if recipient_match:
            info["recipient"] = recipient_match.group(1).strip()
        
        # Extract subject
        subject_match = re.search(r'(?:konu|subject)[:\s]+([^,\n]+)', message, re.I)
        if subject_match:
            info["subject"] = subject_match.group(1).strip()
        
        # Extract date
        date_match = re.search(r'\d{2}[./]\d{2}[./]\d{4}', message)
        if date_match:
            info["date"] = date_match.group(0)
        
        # Extract amount
        amount_match = re.search(r'(\d+(?:\.\d{2})?)\s*(?:TL|USD|EUR)', message)
        if amount_match:
            info["amount"] = amount_match.group(1)
        
        # Extract deadline
        deadline_match = re.search(r'(?:son|deadline)[:\s]+(\d{2}[./]\d{2}[./]\d{4})', message, re.I)
        if deadline_match:
            info["deadline"] = deadline_match.group(1)
        
        return info
    
    def _load_templates(self) -> Dict[str, str]:
        """Load email templates."""
        templates = {
            "default": """
Sayın {recipient},

{subject} hakkında size bilgi vermek istiyorum.

""",
            "tax_notice": """
Sayın {recipient},

{date} tarihli vergi bildirimi hakkında sizi bilgilendirmek istiyorum.

Beyanname son gönderim tarihi: {deadline}

""",
            "invoice_notice": """
Sayın {recipient},

{date} tarihli ve {amount} TL tutarındaki faturanız hakkında bilgilendirme.

""",
            "payment_reminder": """
Sayın {recipient},

{date} vadeli {amount} TL tutarındaki ödemeniz hakkında hatırlatma.

Son ödeme tarihi: {deadline}

"""
        }
        
        # Save templates to disk
        template_file = os.path.join(self.templates_dir, "templates.json")
        if not os.path.exists(template_file):
            with open(template_file, "w", encoding="utf-8") as f:
                json.dump(templates, f, ensure_ascii=False, indent=2)
        
        return templates 