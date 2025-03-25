from typing import Dict, List, Any
from datetime import datetime, timedelta
import json
import os

class DeadlineTracker:
    def __init__(self):
        self.data_dir = "./data/deadlines"
        os.makedirs(self.data_dir, exist_ok=True)
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
    
    def _load_deadlines(self) -> List[Dict]:
        """Load deadlines from file."""
        deadlines_file = os.path.join(self.data_dir, "deadlines.json")
        
        if not os.path.exists(deadlines_file):
            # Create default deadlines
            deadlines = [
                {
                    "name": "KDV Beyannamesi",
                    "date": (datetime.now() + timedelta(days=7)).strftime("%d.%m.%Y"),
                    "period": "monthly"
                },
                {
                    "name": "Muhtasar Beyanname",
                    "date": (datetime.now() + timedelta(days=14)).strftime("%d.%m.%Y"),
                    "period": "monthly"
                },
                {
                    "name": "Geçici Vergi Beyannamesi",
                    "date": (datetime.now() + timedelta(days=30)).strftime("%d.%m.%Y"),
                    "period": "quarterly"
                },
                {
                    "name": "Kurumlar Vergisi Beyannamesi",
                    "date": (datetime.now() + timedelta(days=60)).strftime("%d.%m.%Y"),
                    "period": "yearly"
                }
            ]
            
            # Save to file
            with open(deadlines_file, "w", encoding="utf-8") as f:
                json.dump(deadlines, f, ensure_ascii=False, indent=2)
        
        else:
            # Load from file
            with open(deadlines_file, "r", encoding="utf-8") as f:
                deadlines = json.load(f)
        
        return deadlines
    
    async def check(self, message: str) -> str:
        """Check deadlines based on the message."""
        # Extract period from message
        period = self._extract_period(message)
        
        # Get relevant deadlines
        deadlines = self._get_deadlines(period)
        
        if not deadlines:
            return "Bu dönem için yaklaşan beyanname tarihi bulunamadı."
        
        # Format response
        response = "Yaklaşan Beyanname Tarihleri:\n\n"
        for deadline in deadlines:
            days_left = (deadline["date"] - datetime.now()).days
            status = "⚠️ ACİL" if days_left <= 3 else "✓ Normal"
            
            response += f"""
{status}
- Beyanname: {deadline['name']}
- Son Tarih: {deadline['date'].strftime('%d.%m.%Y')}
- Kalan Gün: {days_left} gün
"""
        
        return response
    
    def _extract_period(self, message: str) -> str:
        """Extract period from message."""
        message = message.lower()
        if "yıllık" in message:
            return "yearly"
        elif "aylık" in message:
            return "monthly"
        elif "3" in message or "üç" in message:
            return "quarterly"
        else:
            return "all"
    
    def _get_deadlines(self, period: str) -> List[Dict]:
        """Get deadlines for the specified period."""
        now = datetime.now()
        deadlines = []
        
        for deadline in self.deadlines:
            deadline_date = datetime.strptime(deadline["date"], "%d.%m.%Y")
            if deadline_date < now:
                continue
            
            if period == "all" or deadline["period"] == period:
                deadlines.append({
                    "name": deadline["name"],
                    "date": deadline_date,
                    "period": deadline["period"]
                })
        
        return sorted(deadlines, key=lambda x: x["date"])
    
    def _list_all_deadlines(self) -> str:
        """List all available deadlines."""
        result = "Mevcut Beyanname Son Tarihleri:\n\n"
        for tax_type, periods in self.common_deadlines.items():
            result += f"{tax_type}:\n"
            for period, deadline in periods.items():
                result += f"- {period}: {deadline}\n"
            result += "\n"
        return result 