import re
from typing import Dict, List
import json
import os

class HesapPlaniProcessor:
    def __init__(self):
        self.data_dir = "./data/hesap_plani"
        os.makedirs(self.data_dir, exist_ok=True)
        self.accounts = self._load_accounts()
    
    async def search_account(self, message: str) -> str:
        """Search for account based on the message."""
        # Extract search criteria
        code = self._extract_code(message)
        keywords = self._extract_keywords(message)
        
        if not code and not keywords:
            return "Lütfen bir hesap kodu veya anahtar kelime belirtin."
        
        # Search accounts
        results = []
        for account in self.accounts:
            if code and account["code"].startswith(code):
                results.append(account)
            elif keywords:
                if any(kw.lower() in account["name"].lower() for kw in keywords):
                    results.append(account)
        
        if not results:
            return "Hesap bulunamadı."
        
        # Format response
        response = "Bulunan Hesaplar:\n\n"
        for account in results:
            response += f"""
{account['code']} - {account['name']}
Tür: {account['type']}
Grup: {account['group']}
"""
        
        return response
    
    def _extract_code(self, message: str) -> str:
        """Extract account code from message."""
        code_match = re.search(r'\b(\d{1,3})\b', message)
        return code_match.group(1) if code_match else ""
    
    def _extract_keywords(self, message: str) -> List[str]:
        """Extract search keywords from message."""
        # Remove common words and punctuation
        message = message.lower()
        message = re.sub(r'hesap|planı|bul|ara|lütfen|[^\w\s]', '', message)
        
        # Split into words and remove empty strings
        return [word.strip() for word in message.split() if word.strip()]
    
    def _load_accounts(self) -> List[Dict]:
        """Load account definitions."""
        accounts_file = os.path.join(self.data_dir, "accounts.json")
        
        if not os.path.exists(accounts_file):
            # Create default accounts
            accounts = [
                {
                    "code": "100",
                    "name": "KASA",
                    "type": "Bilanço Hesabı",
                    "group": "Dönen Varlıklar"
                },
                {
                    "code": "102",
                    "name": "BANKALAR",
                    "type": "Bilanço Hesabı",
                    "group": "Dönen Varlıklar"
                },
                {
                    "code": "120",
                    "name": "ALICILAR",
                    "type": "Bilanço Hesabı",
                    "group": "Dönen Varlıklar"
                },
                {
                    "code": "320",
                    "name": "SATICILAR",
                    "type": "Bilanço Hesabı",
                    "group": "Kısa Vadeli Yabancı Kaynaklar"
                },
                {
                    "code": "391",
                    "name": "HESAPLANAN KDV",
                    "type": "Bilanço Hesabı",
                    "group": "Kısa Vadeli Yabancı Kaynaklar"
                },
                {
                    "code": "600",
                    "name": "YURTİÇİ SATIŞLAR",
                    "type": "Gelir Tablosu Hesabı",
                    "group": "Gelir Tablosu Hesapları"
                },
                {
                    "code": "191",
                    "name": "İNDİRİLECEK KDV",
                    "type": "Bilanço Hesabı",
                    "group": "Dönen Varlıklar"
                }
            ]
            
            # Save to file
            with open(accounts_file, "w", encoding="utf-8") as f:
                json.dump(accounts, f, ensure_ascii=False, indent=2)
        
        else:
            # Load from file
            with open(accounts_file, "r", encoding="utf-8") as f:
                accounts = json.load(f)
        
        return accounts 