import os
from datetime import datetime
from fpdf import FPDF

class FileGenerator:
    def create_text_file(self, transcript_content, session_name):
        try:
            text_folder = 'assets/transcripts/text'
            os.makedirs(text_folder, exist_ok=True)
            
            current_time = datetime.now()
            timestamp = current_time.strftime('%Y%m%d_%H%M%S')
            text_filename = f"{text_folder}/transcript_{timestamp}_{session_name}.txt"
            
            header_content = self.build_transcript_header(session_name, current_time)
            complete_content = header_content + transcript_content
            
            with open(text_filename, 'w', encoding='utf-8') as text_file:
                text_file.write(complete_content)
            
            return text_filename
            
        except Exception as error:
            print(f"Failed to create text file: {error}")
            return None
    
    def create_pdf_file(self, transcript_content, session_name):
        try:
            pdf_folder = 'assets/transcripts/pdf'
            os.makedirs(pdf_folder, exist_ok=True)
            
            current_time = datetime.now()
            timestamp = current_time.strftime('%Y%m%d_%H%M%S')
            pdf_filename = f"{pdf_folder}/transcript_{timestamp}_{session_name}.pdf"
            
            pdf_document = FPDF()
            pdf_document.add_page()
            
            self.add_pdf_header(pdf_document, current_time, session_name)
            self.add_pdf_content(pdf_document, transcript_content)
            
            pdf_document.output(pdf_filename)
            return pdf_filename
            
        except Exception as error:
            print(f"Failed to create PDF file: {error}")
            return None
    
    def build_transcript_header(self, session_name, creation_time):
        formatted_date = creation_time.strftime('%Y-%m-%d %H:%M:%S')
        
        header = f"""Meeting Transcript
Generated: {formatted_date}
Session: {session_name}
{'='*60}

"""
        return header
    
    def add_pdf_header(self, pdf_doc, creation_time, session_name):
        pdf_doc.set_font("Arial", "B", 16)
        pdf_doc.cell(0, 10, "Meeting Transcript", ln=True, align='C')
        pdf_doc.ln(3)
        
        pdf_doc.set_font("Arial", size=10)
        pdf_doc.cell(0, 8, f"Generated: {creation_time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf_doc.cell(0, 8, f"Session: {session_name}", ln=True)
        pdf_doc.ln(8)
    
    def add_pdf_content(self, pdf_doc, transcript_text):
        pdf_doc.set_font("Arial", size=11)
        text_lines = transcript_text.split('\n')
        
        for line in text_lines:
            if pdf_doc.get_y() > 270:
                pdf_doc.add_page()
            
            clean_line = line.encode('latin-1', 'replace').decode('latin-1')
            display_line = clean_line[:85] if len(clean_line) > 85 else clean_line
            pdf_doc.cell(0, 6, display_line, ln=True)
