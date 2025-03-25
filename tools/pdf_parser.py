from typing import Dict, Any, List
import PyPDF2
import re
from datetime import datetime

class PDFParser:
    def __init__(self):
        self.einvoice_patterns = {
            "invoice_no": r"Fatura No\s*:\s*([A-Z0-9-]+)",
            "date": r"Tarih\s*:\s*(\d{2}\.\d{2}\.\d{4})",
            "amount": r"Toplam Tutar\s*:\s*([\d,\.]+)\s*TL",
            "kdv_amount": r"KDV Tutarı\s*:\s*([\d,\.]+)\s*TL",
            "company_name": r"Ünvan\s*:\s*([^\n]+)",
            "tax_number": r"VKN/TCKN\s*:\s*(\d+)",
            "invoice_type": r"Fatura Türü\s*:\s*([^\n]+)",
            "currency": r"Para Birimi\s*:\s*([^\n]+)",
            "payment_terms": r"Ödeme Koşulları\s*:\s*([^\n]+)",
            "items": r"(\d+)\s+([^\n]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)"
        }
        
        self.hesap_plani_patterns = {
            "account_code": r"(\d{3})\s+([^\n]+)",
            "account_type": r"Hesap Türü\s*:\s*([^\n]+)",
            "account_group": r"Hesap Grubu\s*:\s*([^\n]+)"
        }
    
    async def process(self, file_path: str) -> str:
        """Process a PDF file and extract relevant information."""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Extract text from all pages
                for page in reader.pages:
                    text += page.extract_text()
                
                # Try to identify document type and process accordingly
                if "E-FATURA" in text:
                    return self._process_einvoice(text)
                elif "TEK DÜZEN HESAP PLANI" in text:
                    return self._process_hesap_plani(text)
                else:
                    return self._process_general_document(text)
                
        except Exception as e:
            return f"PDF işleme sırasında bir hata oluştu: {str(e)}"
    
    def _process_einvoice(self, text: str) -> str:
        """Extract information from e-invoice."""
        info = {}
        for key, pattern in self.einvoice_patterns.items():
            match = re.search(pattern, text)
            if match:
                info[key] = match.group(1)
        
        if not info:
            return "E-fatura bilgileri bulunamadı."
        
        # Extract line items
        items = []
        for match in re.finditer(self.einvoice_patterns["items"], text):
            items.append({
                "quantity": match.group(1),
                "description": match.group(2),
                "unit_price": match.group(3),
                "amount": match.group(4),
                "kdv_rate": match.group(5),
                "kdv_amount": match.group(6)
            })
        
        result = (
            f"E-Fatura Bilgileri:\n"
            f"Fatura No: {info.get('invoice_no', 'Bulunamadı')}\n"
            f"Tarih: {info.get('date', 'Bulunamadı')}\n"
            f"Fatura Türü: {info.get('invoice_type', 'Bulunamadı')}\n"
            f"Para Birimi: {info.get('currency', 'TL')}\n"
            f"Ödeme Koşulları: {info.get('payment_terms', 'Bulunamadı')}\n"
            f"Toplam Tutar: {info.get('amount', 'Bulunamadı')} TL\n"
            f"KDV Tutarı: {info.get('kdv_amount', 'Bulunamadı')} TL\n"
            f"Firma: {info.get('company_name', 'Bulunamadı')}\n"
            f"VKN/TCKN: {info.get('tax_number', 'Bulunamadı')}\n\n"
            f"Kalemler:\n"
        )
        
        for item in items:
            result += (
                f"- {item['quantity']} adet {item['description']}\n"
                f"  Birim Fiyat: {item['unit_price']} TL\n"
                f"  Tutar: {item['amount']} TL\n"
                f"  KDV Oranı: %{item['kdv_rate']}\n"
                f"  KDV Tutarı: {item['kdv_amount']} TL\n\n"
            )
        
        return result
    
    def _process_hesap_plani(self, text: str) -> str:
        """Extract information from Tek Düzen Hesap Planı."""
        accounts = []
        for match in re.finditer(self.hesap_plani_patterns["account_code"], text):
            accounts.append({
                "code": match.group(1),
                "description": match.group(2)
            })
        
        if not accounts:
            return "Hesap planı bilgileri bulunamadı."
        
        result = "Tek Düzen Hesap Planı Bilgileri:\n\n"
        for account in accounts:
            result += f"{account['code']} - {account['description']}\n"
        
        return result
    
    def _process_general_document(self, text: str) -> str:
        """Process general tax documents."""
        return "Genel belge analizi yapılıyor..." 