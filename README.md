# MaliBot - AI-Powered Accounting Assistant

MaliBot is an intelligent accounting assistant that helps with various accounting tasks, including KDV calculations, PDF parsing, email writing, and deadline tracking. It integrates with popular accounting systems like DBS and Zirve Nova.

## Features

### 1. KDV Calculator
- Calculate KDV (VAT) for any amount
- Support for different KDV rates
- Detailed breakdown of calculations

### 2. PDF Parser
- Parse e-fatura (e-invoice) documents
- Extract information from hesap planı (account plan)
- Process beyanname (tax declaration) documents
- Automatic data extraction and organization

### 3. Email Writer
- Generate professional emails for:
  - Tax notices
  - Invoice notices
  - Payment reminders
- Auto-fill based on extracted information
- Multiple language support

### 4. Deadline Tracker
- Track beyanname (tax declaration) deadlines
- Monitor upcoming deadlines
- Status tracking and notifications
- Calendar integration

### 5. Hesap Planı Search
- Search by account code
- Search by keywords
- Detailed account information display
- Account type and group categorization

### 6. Accounting System Integration
- DBS integration
- Zirve Nova integration
- Automated transaction entry
- Data synchronization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/malibot.git
cd malibot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Ollama:
- Download from: https://ollama.ai/download
- Install the application
- Pull the Mistral model:
```bash
ollama pull mistral
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Open your web browser and navigate to:
```
http://localhost:7860
```

3. Interact with MaliBot through the chat interface:
- Type messages to ask questions
- Upload PDFs for processing
- Use the various tools through the interface

## Project Structure

```
malibot/
├── chat/
│   ├── assistant.py
│   └── tools/
│       ├── kdv_calculator.py
│       ├── pdf_parser.py
│       ├── email_writer.py
│       ├── deadline_tracker.py
│       ├── hesap_plani.py
│       └── accounting_system.py
├── frontend/
│   └── interface.py
├── memory/
│   └── vector_store.py
├── main.py
└── requirements.txt
```

## Requirements

- Python 3.8+
- Ollama
- Mistral model
- Dependencies listed in requirements.txt

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ollama for providing the AI model infrastructure
- The open-source community for various libraries used in this project 