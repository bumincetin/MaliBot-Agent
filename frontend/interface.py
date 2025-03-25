import gradio as gr
from typing import List, Dict
from chat.assistant import MaliBotAssistant

def create_gradio_interface(assistant: MaliBotAssistant):
    """Create and return the Gradio interface."""
    
    with gr.Blocks(title="MaliBot - Mali Müşavir Asistanı", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# MaliBot - Mali Müşavir Asistanı")
        gr.Markdown("""
        MaliBot, mali müşavirler için geliştirilmiş yapay zeka destekli bir asistan uygulamasıdır.
        Aşağıdaki özellikleri kullanabilirsiniz:
        
        - KDV Hesaplama
        - Vergi Mevzuatı Sorgulama
        - E-Fatura Analizi
        - Resmi Yazışma Oluşturma
        - Beyanname Takibi
        """)
        
        with gr.Row():
            with gr.Column(scale=4):
                chatbot = gr.Chatbot(
                    [],
                    elem_id="chatbot",
                    bubble_full_width=False,
                    avatar_images=(None, "assets/malibot.png"),
                    height=600
                )
                txt = gr.Textbox(
                    show_label=False,
                    placeholder="Mesajınızı yazın...",
                    container=False
                )
                with gr.Row():
                    submit_btn = gr.Button("Gönder", variant="primary")
                    clear_btn = gr.Button("Temizle")
            
            with gr.Column(scale=1):
                with gr.Group():
                    gr.Markdown("### Dosya Yükleme")
                    pdf_upload = gr.File(
                        label="PDF Dosyası Yükle",
                        file_types=[".pdf"]
                    )
                    upload_btn = gr.Button("Yükle")
        
        async def user(user_message, history):
            history = history or []
            history.append([user_message, None])
            return "", history
        
        async def bot(history):
            user_message = history[-1][0]
            bot_message = await assistant.process_message(user_message, history)
            history[-1][1] = bot_message
            return history
        
        async def upload_file(file):
            if file is None:
                return "Lütfen bir dosya seçin."
            # Here you would implement file processing logic
            return f"Dosya yüklendi: {file.name}"
        
        submit_btn.click(
            user,
            [txt, chatbot],
            [txt, chatbot]
        ).then(
            bot,
            chatbot,
            chatbot
        )
        
        clear_btn.click(lambda: None, None, chatbot, queue=False)
        upload_btn.click(
            upload_file,
            pdf_upload,
            chatbot
        )
    
    return interface 