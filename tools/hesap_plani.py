from typing import Dict, List
import PyPDF2
import re

class HesapPlaniProcessor:
    def __init__(self):
        self.hesap_plani = {}
        self._load_hesap_plani()
    
    def _load_hesap_plani(self):
        """Load Tek Düzen Hesap Planı from PDF."""
        try:
            with open("memory/hesap_plani.pdf", 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                # Parse account codes and descriptions
                pattern = r'(\d{3})\s+([^\n]+)'
                matches = re.finditer(pattern, text)
                for match in matches:
                    code = match.group(1)
                    description = match.group(2).strip()
                    self.hesap_plani[code] = description
        except Exception as e:
            print(f"Hesap planı yüklenirken hata: {str(e)}")
    
    async def search_account(self, query: str) -> str:
        """Search for accounts based on code or description."""
        results = []
        query = query.lower()
        
        for code, desc in self.hesap_plani.items():
            if query in code or query in desc.lower():
                results.append(f"{code} - {desc}")
        
        if not results:
            return "Hesap bulunamadı."
        
        return "\n".join(results)
    
    async def get_account_info(self, account_code: str) -> str:
        """Get detailed information about a specific account."""
        if account_code in self.hesap_plani:
            return f"Hesap Kodu: {account_code}\nAçıklama: {self.hesap_plani[account_code]}"
        return "Hesap bulunamadı." 