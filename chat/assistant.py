from typing import List, Dict, Any
import ollama
from memory.vector_store import VectorStore
from tools.kdv_calculator import KDVCalculator
from tools.pdf_parser import PDFParser
from tools.email_writer import EmailWriter
from tools.deadline_tracker import DeadlineTracker
from tools.hesap_plani import HesapPlaniProcessor
from tools.accounting_system import AccountingSystem
import re

class MaliBotAssistant:
    def __init__(self):
        self.model = "mistral"  # or any other model you prefer
        self.vector_store = VectorStore()
        self.tools = {
            "kdv_calculator": KDVCalculator(),
            "pdf_parser": PDFParser(),
            "email_writer": EmailWriter(),
            "deadline_tracker": DeadlineTracker(),
            "hesap_plani": HesapPlaniProcessor(),
            "accounting_system": AccountingSystem()
        }
        
    async def process_message(self, message: str, history: List[Dict[str, str]] = None) -> str:
        """Process user message and generate response using appropriate tools."""
        # Analyze message intent and determine which tool to use
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": "Sen MaliBot, Türkiye'deki mali müşavirler için geliştirilmiş bir AI asistansın. Kullanıcının mesajını analiz et ve hangi aracı kullanman gerektiğine karar ver."},
                {"role": "user", "content": message}
            ]
        )
        
        # Process the response and use appropriate tools
        message_lower = message.lower()
        
        if "kdv" in message_lower:
            return await self.tools["kdv_calculator"].calculate(message)
        elif "pdf" in message_lower or "fatura" in message_lower:
            return await self.tools["pdf_parser"].process(message)
        elif "e-posta" in message_lower or "mail" in message_lower:
            return await self.tools["email_writer"].generate(message)
        elif "beyanname" in message_lower or "son tarih" in message_lower:
            return await self.tools["deadline_tracker"].check(message)
        elif "hesap" in message_lower and "plan" in message_lower:
            return await self.tools["hesap_plani"].search_account(message)
        elif "dbs" in message_lower or "zirve" in message_lower:
            # Extract transaction details from message
            data = self._extract_transaction_data(message)
            system = "dbs" if "dbs" in message_lower else "zirve"
            return await self.tools["accounting_system"].enter_transaction(system, data)
        else:
            # Use vector store for general knowledge queries
            relevant_docs = self.vector_store.search(message)
            return await self._generate_contextual_response(message, relevant_docs)
    
    async def _generate_contextual_response(self, message: str, context: List[str]) -> str:
        """Generate response using context from vector store."""
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": "Sen MaliBot, Türkiye'deki mali müşavirler için geliştirilmiş bir AI asistansın. Verilen bağlamı kullanarak kullanıcının sorusunu yanıtla."},
                {"role": "user", "content": f"Bağlam: {' '.join(context)}\n\nSoru: {message}"}
            ]
        )
        return response['message']['content']
    
    def _extract_transaction_data(self, message: str) -> Dict[str, Any]:
        """Extract transaction details from message."""
        # This is a simple implementation - you might want to make it more sophisticated
        data = {
            "account_code": "",
            "amount": "",
            "description": ""
        }
        
        # Extract account code (assuming it's a 3-digit number)
        account_match = re.search(r'\b\d{3}\b', message)
        if account_match:
            data["account_code"] = account_match.group(0)
        
        # Extract amount (assuming it's a number with decimal point)
        amount_match = re.search(r'\b\d+(?:\.\d{2})?\b', message)
        if amount_match:
            data["amount"] = amount_match.group(0)
        
        # Extract description (everything after the amount)
        if amount_match:
            data["description"] = message[amount_match.end():].strip()
        
        return data 