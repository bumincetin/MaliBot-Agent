from typing import Dict, Any
import re

class KDVCalculator:
    def __init__(self):
        self.kdv_rates = {
            1: 0.01,  # %1
            8: 0.08,  # %8
            10: 0.10, # %10
            18: 0.18, # %18
            20: 0.20  # %20
        }
    
    async def calculate(self, message: str) -> str:
        """Calculate KDV based on the message."""
        # Extract amount and rate from message
        amount_match = re.search(r'\b(\d+(?:\.\d{2})?)\b', message)
        rate_match = re.search(r'%?(\d+)\s*(?:kdv|KDV)', message)
        
        if not amount_match or not rate_match:
            return "Lütfen tutarı ve KDV oranını belirtin. Örnek: '1000 TL için %18 KDV hesapla'"
        
        amount = float(amount_match.group(1))
        rate = int(rate_match.group(1))
        
        if rate not in self.kdv_rates:
            return f"Geçersiz KDV oranı. Geçerli oranlar: {', '.join(map(str, self.kdv_rates.keys()))}%"
        
        kdv_amount = amount * self.kdv_rates[rate]
        total_amount = amount + kdv_amount
        
        return f"""
KDV Hesaplama Sonucu:
- Matrah: {amount:.2f} TL
- KDV Oranı: %{rate}
- KDV Tutarı: {kdv_amount:.2f} TL
- Toplam: {total_amount:.2f} TL
"""
    
    def _determine_rate(self, message: str) -> float:
        """Determine which KDV rate to use based on message content."""
        message = message.lower()
        
        if "indirimli" in message or "düşük" in message:
            return self.kdv_rates["2"]
        elif "özel" in message or "istisna" in message:
            return self.kdv_rates["3"]
        else:
            return self.kdv_rates["1"] 