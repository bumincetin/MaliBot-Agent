from typing import Dict, Any
import re

class KDVCalculator:
    def __init__(self):
        self.kdv_rates = {
            "1": 0.18,  # Genel KDV oranı
            "2": 0.08,  # İndirimli KDV oranı
            "3": 0.01   # Özel KDV oranı
        }
    
    async def calculate(self, message: str) -> str:
        """Calculate KDV based on user input."""
        try:
            # Extract numbers from the message
            numbers = re.findall(r'\d+(?:\.\d+)?', message)
            if not numbers:
                return "Lütfen bir tutar giriniz."
            
            amount = float(numbers[0])
            
            # Determine KDV rate based on message content
            rate = self._determine_rate(message)
            
            # Calculate KDV
            kdv_amount = amount * rate
            total_amount = amount + kdv_amount
            
            return (
                f"KDV Hesaplama Sonuçları:\n"
                f"Tutar: {amount:,.2f} TL\n"
                f"KDV Oranı: %{rate*100:.0f}\n"
                f"KDV Tutarı: {kdv_amount:,.2f} TL\n"
                f"Toplam Tutar: {total_amount:,.2f} TL"
            )
            
        except Exception as e:
            return f"Hesaplama sırasında bir hata oluştu: {str(e)}"
    
    def _determine_rate(self, message: str) -> float:
        """Determine which KDV rate to use based on message content."""
        message = message.lower()
        
        if "indirimli" in message or "düşük" in message:
            return self.kdv_rates["2"]
        elif "özel" in message or "istisna" in message:
            return self.kdv_rates["3"]
        else:
            return self.kdv_rates["1"] 