import os
import gradio as gr
from chat.assistant import MaliBotAssistant
from frontend.interface import create_gradio_interface

def main():
    # Initialize the MaliBot assistant
    assistant = MaliBotAssistant()
    
    # Create and launch the Gradio interface
    interface = create_gradio_interface(assistant)
    interface.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main() 