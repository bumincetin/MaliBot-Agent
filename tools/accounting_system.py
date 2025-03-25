from typing import Dict, Any
import pyautogui
import time
import json
import os
import re

class AccountingSystem:
    def __init__(self):
        self.config_file = "memory/system_config.json"
        self.config = self._load_config()
        self.systems = {
            "dbs": {
                "new_entry": ["alt", "y"],  # Alt+Y for new entry
                "account_field": "tab",      # Tab to account field
                "amount_field": "tab",       # Tab to amount field
                "save": ["ctrl", "s"]        # Ctrl+S to save
            },
            "zirve": {
                "new_entry": ["ctrl", "n"],  # Ctrl+N for new entry
                "account_field": "tab",      # Tab to account field
                "amount_field": "tab",       # Tab to amount field
                "save": ["ctrl", "s"]        # Ctrl+S to save
            }
        }
        
        # Set pyautogui settings
        pyautogui.PAUSE = 0.5  # 0.5 second pause between actions
        pyautogui.FAILSAFE = True  # Move mouse to upper-left corner to abort
    
    def _load_config(self) -> Dict[str, Any]:
        """Load system configuration."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "dbs": {
                "window_title": "DBS",
                "shortcuts": {
                    "yeni_kayit": "F3",
                    "kaydet": "F12",
                    "iptal": "ESC"
                }
            },
            "zirve": {
                "window_title": "Zirve Nova",
                "shortcuts": {
                    "yeni_kayit": "F3",
                    "kaydet": "F12",
                    "iptal": "ESC"
                }
            }
        }
    
    async def enter_transaction(self, system: str, data: Dict[str, Any]) -> str:
        """Enter a transaction into the accounting system."""
        if system not in self.systems:
            return f"Desteklenmeyen muhasebe sistemi: {system}"
        
        if not self._validate_data(data):
            return "Eksik veya geçersiz işlem bilgileri."
        
        try:
            # Get system shortcuts
            shortcuts = self.systems[system]
            
            # New entry
            pyautogui.hotkey(*shortcuts["new_entry"])
            time.sleep(1)  # Wait for window/form to open
            
            # Enter account code
            pyautogui.press(shortcuts["account_field"])
            pyautogui.write(data["account_code"])
            
            # Enter amount
            pyautogui.press(shortcuts["amount_field"])
            pyautogui.write(data["amount"])
            
            # Enter description if available
            if data.get("description"):
                pyautogui.press("tab")
                pyautogui.write(data["description"])
            
            # Save entry
            pyautogui.hotkey(*shortcuts["save"])
            
            return f"""
İşlem Kaydedildi:
- Sistem: {system.upper()}
- Hesap: {data['account_code']}
- Tutar: {data['amount']} TL
- Açıklama: {data.get('description', 'Belirtilmedi')}
"""
            
        except Exception as e:
            return f"İşlem sırasında bir hata oluştu: {str(e)}"
    
    def _validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate transaction data."""
        # Check required fields
        if not data.get("account_code") or not data.get("amount"):
            return False
        
        # Validate account code (3 digits)
        if not re.match(r'^\d{3}$', data["account_code"]):
            return False
        
        # Validate amount (number with optional decimal)
        if not re.match(r'^\d+(\.\d{2})?$', str(data["amount"])):
            return False
        
        return True 