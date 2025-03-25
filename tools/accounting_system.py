from typing import Dict, Any
import pyautogui
import time
import json
import os

class AccountingSystem:
    def __init__(self):
        self.config_file = "memory/system_config.json"
        self.config = self._load_config()
    
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
        """Enter transaction into accounting system."""
        try:
            if system.lower() == "dbs":
                return await self._enter_dbs_transaction(data)
            elif system.lower() == "zirve":
                return await self._enter_zirve_transaction(data)
            else:
                return "Desteklenmeyen muhasebe sistemi."
        except Exception as e:
            return f"İşlem sırasında hata: {str(e)}"
    
    async def _enter_dbs_transaction(self, data: Dict[str, Any]) -> str:
        """Enter transaction into DBS."""
        # Focus DBS window
        pyautogui.getWindowsWithTitle(self.config["dbs"]["window_title"])
        time.sleep(1)
        
        # Enter transaction details
        pyautogui.hotkey(self.config["dbs"]["shortcuts"]["yeni_kayit"])
        time.sleep(0.5)
        
        # Fill in transaction details
        pyautogui.write(data.get("account_code", ""))
        pyautogui.press("tab")
        pyautogui.write(data.get("amount", ""))
        pyautogui.press("tab")
        pyautogui.write(data.get("description", ""))
        
        # Save transaction
        pyautogui.hotkey(self.config["dbs"]["shortcuts"]["kaydet"])
        
        return "İşlem başarıyla kaydedildi."
    
    async def _enter_zirve_transaction(self, data: Dict[str, Any]) -> str:
        """Enter transaction into Zirve Nova."""
        # Focus Zirve window
        pyautogui.getWindowsWithTitle(self.config["zirve"]["window_title"])
        time.sleep(1)
        
        # Enter transaction details
        pyautogui.hotkey(self.config["zirve"]["shortcuts"]["yeni_kayit"])
        time.sleep(0.5)
        
        # Fill in transaction details
        pyautogui.write(data.get("account_code", ""))
        pyautogui.press("tab")
        pyautogui.write(data.get("amount", ""))
        pyautogui.press("tab")
        pyautogui.write(data.get("description", ""))
        
        # Save transaction
        pyautogui.hotkey(self.config["zirve"]["shortcuts"]["kaydet"])
        
        return "İşlem başarıyla kaydedildi." 