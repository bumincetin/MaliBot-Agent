import pypdf
import re
from typing import Dict, Any
import os

class PDFParser:
    def __init__(self):
        self.supported_types = ["efatura", "hesap_plani", "beyanname"]
    
    async def process(self, message: str, file_path: str = None) -> str:
        """Process PDF file based on the message."""
        if not file_path:
            return "Lütfen bir PDF dosyası yükleyin."
        
        if not os.path.exists(file_path):
            return f"Dosya bulunamadı: {file_path}"
        
        try:
            # Determine document type
            doc_type = self._determine_type(message)
            
            # Parse PDF based on type
            if doc_type == "efatura":
                return await self._parse_efatura(file_path)
            elif doc_type == "hesap_plani":
                return await self._parse_hesap_plani(file_path)
            elif doc_type == "beyanname":
                return await self._parse_beyanname(file_path)
            else:
                return "Desteklenmeyen belge türü."
            
        except Exception as e:
            return f"PDF işlenirken bir hata oluştu: {str(e)}"
    
    def _determine_type(self, message: str) -> str:
        """Determine the type of document from the message."""
        message = message.lower()
        if "fatura" in message or "e-fatura" in message:
            return "efatura"
        elif "hesap" in message and "plan" in message:
            return "hesap_plani"
        elif "beyanname" in message:
            return "beyanname"
        return "unknown"
    
    async def _parse_efatura(self, file_path: str) -> str:
        """Parse e-fatura PDF."""
        # Basic implementation - you would want to make this more sophisticated
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Extract basic information
        info = {
            "tarih": self._extract_date(text),
            "tutar": self._extract_amount(text),
            "kdv": self._extract_vat(text),
            "firma": self._extract_company(text)
        }
        
        return f"""
E-Fatura Bilgileri:
- Tarih: {info['tarih']}
- Firma: {info['firma']}
- Tutar: {info['tutar']} TL
- KDV: {info['kdv']} TL
"""
    
    async def _parse_hesap_plani(self, file_path: str) -> str:
        """Parse hesap planı PDF."""
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Basic implementation - you would want to make this more sophisticated
        return "Hesap planı işlendi."
    
    async def _parse_beyanname(self, file_path: str) -> str:
        """Parse beyanname PDF."""
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Basic implementation - you would want to make this more sophisticated
        return "Beyanname işlendi."
    
    def _extract_date(self, text: str) -> str:
        """Extract date from text."""
        date_match = re.search(r'\d{2}[./]\d{2}[./]\d{4}', text)
        return date_match.group(0) if date_match else "Bulunamadı"
    
    def _extract_amount(self, text: str) -> str:
        """Extract amount from text."""
        amount_match = re.search(r'(?:TOPLAM|TUTAR)[^\d]*(\d+(?:\.\d{2})?)', text)
        return amount_match.group(1) if amount_match else "Bulunamadı"
    
    def _extract_vat(self, text: str) -> str:
        """Extract VAT amount from text."""
        vat_match = re.search(r'KDV[^\d]*(\d+(?:\.\d{2})?)', text)
        return vat_match.group(1) if vat_match else "Bulunamadı"
    
    def _extract_company(self, text: str) -> str:
        """Extract company name from text."""
        company_match = re.search(r'(?:SAYIN|FİRMA)[^\n]*\n([^\n]+)', text)
        return company_match.group(1).strip() if company_match else "Bulunamadı" 