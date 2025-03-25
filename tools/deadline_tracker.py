from typing import Dict, List, Any
from datetime import datetime, timedelta
import json
import os

class DeadlineTracker:
    def __init__(self):
        self.deadlines_file = "data/deadlines.json"
        self.deadlines = self._load_deadlines()
        
        # Common tax declaration deadlines
        self.common_deadlines = {
            "KDV": {
                "monthly": "Ayın 26'sı",
                "quarterly": "Çeyreğin son gününden itibaren 26 gün"
            },
            "Gelir Vergisi": {
                "monthly": "Ayın 26'sı",
                "quarterly": "Çeyreğin son gününden itibaren 26 gün",
                "annual": "Mart ayının son günü"
            },
            "Kurumlar Vergisi": {
                "quarterly": "Çeyreğin son gününden itibaren 26 gün",
                "annual": "Nisan ayının son günü"
            }
        }
    
    def _load_deadlines(self) -> Dict[str, Any]:
        """Load deadlines from JSON file."""
        if os.path.exists(self.deadlines_file):
            with open(self.deadlines_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_deadlines(self):
        """Save deadlines to JSON file."""
        os.makedirs(os.path.dirname(self.deadlines_file), exist_ok=True)
        with open(self.deadlines_file, 'w', encoding='utf-8') as f:
            json.dump(self.deadlines, f, ensure_ascii=False, indent=2)
    
    async def check(self, message: str) -> str:
        """Check deadlines based on user query."""
        try:
            # Extract tax type and period from message
            tax_type = self._extract_tax_type(message)
            period = self._extract_period(message)
            
            if not tax_type:
                return self._list_all_deadlines()
            
            if tax_type in self.common_deadlines:
                deadline_info = self.common_deadlines[tax_type]
                if period in deadline_info:
                    return f"{tax_type} {period} beyanname son tarihi: {deadline_info[period]}"
                else:
                    return f"{tax_type} için mevcut son tarihler:\n" + "\n".join(
                        f"- {p}: {d}" for p, d in deadline_info.items()
                    )
            else:
                return f"{tax_type} için son tarih bilgisi bulunamadı."
                
        except Exception as e:
            return f"Son tarih kontrolü sırasında bir hata oluştu: {str(e)}"
    
    def _extract_tax_type(self, message: str) -> str:
        """Extract tax type from message."""
        message = message.lower()
        for tax_type in self.common_deadlines.keys():
            if tax_type.lower() in message:
                return tax_type
        return ""
    
    def _extract_period(self, message: str) -> str:
        """Extract period from message."""
        message = message.lower()
        if "aylık" in message or "ay" in message:
            return "monthly"
        elif "yıllık" in message or "yıl" in message:
            return "annual"
        elif "çeyreklik" in message or "çeyrek" in message:
            return "quarterly"
        return ""
    
    def _list_all_deadlines(self) -> str:
        """List all available deadlines."""
        result = "Mevcut Beyanname Son Tarihleri:\n\n"
        for tax_type, periods in self.common_deadlines.items():
            result += f"{tax_type}:\n"
            for period, deadline in periods.items():
                result += f"- {period}: {deadline}\n"
            result += "\n"
        return result 