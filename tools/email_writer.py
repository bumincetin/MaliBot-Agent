from typing import Dict, Any
import ollama
from datetime import datetime

class EmailWriter:
    def __init__(self):
        self.model = "mistral"  # or any other model you prefer
    
    async def generate(self, message: str) -> str:
        """Generate an official email based on user input."""
        try:
            # Extract key information from user message
            prompt = f"""
            Aşağıdaki bilgilere dayanarak resmi bir e-posta taslağı oluştur:
            
            Kullanıcı İsteği: {message}
            
            Lütfen aşağıdaki formatta bir e-posta oluştur:
            1. Saygıdeğer [Ad Soyad/Ünvan]
            2. Konu satırı
            3. Giriş paragrafı
            4. Ana metin
            5. Kapanış
            6. Saygılarımla
            """
            
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Sen profesyonel bir mali müşavir asistanısın. Resmi yazışmalarda kullanılmak üzere Türkçe e-postalar oluşturuyorsun."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            email_draft = response['message']['content']
            
            return (
                f"E-posta Taslağı:\n\n"
                f"{email_draft}\n\n"
                f"Not: Bu taslağı kendi ihtiyaçlarınıza göre düzenleyebilirsiniz."
            )
            
        except Exception as e:
            return f"E-posta oluşturulurken bir hata oluştu: {str(e)}"
    
    def _extract_key_info(self, message: str) -> Dict[str, Any]:
        """Extract key information from user message."""
        # Add logic to extract recipient, subject, and other key information
        return {
            "recipient": "",
            "subject": "",
            "content_type": "",
            "urgency": "normal"
        } 