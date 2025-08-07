import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
from .storage import get_job
from PIL import Image

class PDFExporter(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Contact & Social Media Extraction Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

def export_csv(job_id):
    """Export results to CSV format"""
    job = get_job(job_id)
    if not job or job['status'] != 'completed':
        return None
    
    data = []
    for url, result in job['results'].items():
        row = {
            'URL': url,
            'Emails': ', '.join(result['emails']),
            'Facebook': ', '.join(result['facebook']),
            'Instagram': ', '.join(result['instagram']),
            'TikTok': ', '.join(result['tiktok']),
            'Screenshot': result['screenshots'].get('homepage', '')
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    path = f"/tmp/{job_id}.csv"
    df.to_csv(path, index=False)
    return path

def export_excel(job_id):
    """Export results to Excel format"""
    job = get_job(job_id)
    if not job or job['status'] != 'completed':
        return None
    
    data = []
    for url, result in job['results'].items():
        row = {
            'URL': url,
            'Emails': '\n'.join(result['emails']),
            'Facebook': '\n'.join(result['facebook']),
            'Instagram': '\n'.join(result['instagram']),
            'TikTok': '\n'.join(result['tiktok']),
            'Screenshot': result['screenshots'].get('homepage', '')
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    path = f"/tmp/{job_id}.xlsx"
    df.to_excel(path, index=False)
    return path

def export_pdf(job_id):
    """Export results to PDF format with screenshots"""
    job = get_job(job_id)
    if not job or job['status'] != 'completed':
        return None
    
    pdf = PDFExporter()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    
    for url, result in job['results'].items():
        # Add URL header
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, url, 0, 1)
        pdf.set_font('Arial', '', 10)
        
        # Add emails
        pdf.cell(40, 8, 'Emails:', 0, 0)
        pdf.multi_cell(0, 8, ', '.join(result['emails']) or 'None', 0, 1)
        
        # Add social links
        pdf.cell(40, 8, 'Facebook:', 0, 0)
        pdf.multi_cell(0, 8, '\n'.join(result['facebook']) or 'None', 0, 1)
        
        pdf.cell(40, 8, 'Instagram:', 0, 0)
        pdf.multi_cell(0, 8, '\n'.join(result['instagram']) or 'None', 0, 1)
        
        pdf.cell(40, 8, 'TikTok:', 0, 0)
        pdf.multi_cell(0, 8, '\n'.join(result['tiktok']) or 'None', 0, 1)
        
        # Add screenshot if available
        screenshot = result['screenshots'].get('homepage')
        if screenshot and os.path.exists(screenshot):
            try:
                # Resize image to fit PDF
                img = Image.open(screenshot)
                img.thumbnail((150, 150))
                temp_path = f"/tmp/{os.path.basename(screenshot)}"
                img.save(temp_path)
                
                pdf.cell(40, 8, 'Screenshot:', 0, 1)
                pdf.image(temp_path, x=10, w=80)
                os.remove(temp_path)
            except Exception as e:
                pdf.cell(0, 8, f'Screenshot error: {str(e)}', 0, 1)
        
        pdf.ln(5)
    
    path = f"/tmp/{job_id}.pdf"
    pdf.output(path)
    return path
