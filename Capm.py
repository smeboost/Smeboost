import streamlit as st
from openai import OpenAI
import datetime
import re
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, NextPageTemplate
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import datetime
import re
import os
import uuid
from reportlab.platypus import Frame, PageTemplate, BaseDocTemplate, PageBreak
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, NextPageTemplate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import ssl
import logging
import xlsxwriter
EMAIL_SENDER = "smeboost@ceaiglobal.com"
EMAIL_PASSWORD = "MyFinB2024123#"
SMTP_SERVER = "mail.ceaiglobal.com"  # Changed to hostinger server
SMTP_PORT = 465
# Set up logging
context = ssl.create_default_context()
# Constants
BUSINESS_OPTIONS = {
    "Business Valuation": "I want to assess my company's worth, helping me make informed decisions and gain investor trust.",
    "Financial Healthcheck": "I want to review my finances, checking assets, debts, cash flow, and overall stability",
    "Business Partnering": "I want to build partnerships to grow, sharing strengths and resources with others for mutual benefit.",
    "Fund Raising": "I want to secure funds from investors to expand, innovate, or support my business operations.",
    "Bankability and Leverage": "I want to evaluate my creditworthiness, improving access to financing and managing debt effectively.",
    "Mergers and Acquisitions": "I want to pursue growth by combining my business with others, expanding resources and market reach.",
    "Budget and Resourcing": "I want to allocate resources wisely to achieve my goals efficiently and boost productivity.",
    "Business Remodelling": "I want to reshape my operations to stay relevant and seize new market opportunities.",
    "Succession Planning": "I want to prepare for future leadership transitions, ensuring the right people continue my business legacy."
}
def generate_excel_report(session_state):
    """
    Generate an Excel report from the session state data
    Returns a bytes buffer containing the Excel file
    """
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    
    # Create formats
    header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#4B5563',
        'font_color': 'white',
        'border': 1
    })
    
    cell_format = workbook.add_format({
        'align': 'left',
        'valign': 'vcenter',
        'border': 1
    })
    
    # Personal Profile Sheet
    if 'personal_profile' in session_state:
        ws_personal = workbook.add_worksheet('Personal Profile')
        personal_data = session_state['personal_profile']
        
        headers = ['Field', 'Value']
        ws_personal.write_row(0, 0, headers, header_format)
        
        fields = [
            ('Full Name', 'full_name'),
            ('Email', 'email'),
            ('Phone', 'phone'),
            ('Timestamp', 'timestamp')
        ]
        
        for i, (label, key) in enumerate(fields):
            ws_personal.write(i+1, 0, label, cell_format)
            ws_personal.write(i+1, 1, personal_data.get(key, 'N/A'), cell_format)
        
        ws_personal.set_column(0, 0, 20)
        ws_personal.set_column(1, 1, 40)
    
    # Business Profile Sheet
    if 'business_profile' in session_state:
        ws_business = workbook.add_worksheet('Business Profile')
        business_data = session_state['business_profile']
        
        headers = ['Field', 'Value']
        ws_business.write_row(0, 0, headers, header_format)
        
        row = 1
        for key, value in business_data.items():
            field_name = key.replace('_', ' ').title()
            ws_business.write(row, 0, field_name, cell_format)
            if isinstance(value, dict):
                ws_business.write(row, 1, str(value), cell_format)
            else:
                ws_business.write(row, 1, value, cell_format)
            row += 1
        
        ws_business.set_column(0, 0, 20)
        ws_business.set_column(1, 1, 50)
    
    # Business Priorities Sheet
    if 'business_priorities' in session_state:
        ws_priorities = workbook.add_worksheet('Business Priorities')
        priorities_data = session_state['business_priorities']
        
        headers = ['Priority']
        ws_priorities.write_row(0, 0, headers, header_format)
        
        if isinstance(priorities_data, dict):
            ws_priorities.write(1, 0, priorities_data.get('business_priorities', 'N/A'), cell_format)
        else:
            ws_priorities.write(1, 0, str(priorities_data), cell_format)
        
        ws_priorities.set_column(0, 0, 60)
    
    # Business Options Sheet
    if 'business_options' in session_state:
        ws_options = workbook.add_worksheet('Business Options')
        options_data = session_state['business_options']
        
        headers = ['Selected Options']
        ws_options.write_row(0, 0, headers, header_format)
        
        for i, option in enumerate(options_data):
            ws_options.write(i+1, 0, option, cell_format)
        
        ws_options.set_column(0, 0, 40)
    
    # Working Capital Sheet
    if 'working_capital' in session_state:
        ws_capital = workbook.add_worksheet('Working Capital')
        capital_data = session_state['working_capital']
        
        headers = ['Field', 'Value']
        ws_capital.write_row(0, 0, headers, header_format)
        
        row = 1
        for key, value in capital_data.items():
            field_name = key.replace('_', ' ').title()
            ws_capital.write(row, 0, field_name, cell_format)
            if isinstance(value, dict):
                ws_capital.write(row, 1, str(value), cell_format)
            else:
                ws_capital.write(row, 1, str(value), cell_format)
            row += 1
        
        ws_capital.set_column(0, 0, 20)
        ws_capital.set_column(1, 1, 50)
    
    # Strategic Planning Sheet
    if 'strategic_planning' in session_state:
        ws_planning = workbook.add_worksheet('Strategic Planning')
        planning_data = session_state['strategic_planning']
        
        headers = ['Question', 'Selected Options']
        ws_planning.write_row(0, 0, headers, header_format)
        
        row = 1
        for question, answers in planning_data.items():
            ws_planning.write(row, 0, question, cell_format)
            if isinstance(answers, list):
                ws_planning.write(row, 1, ', '.join(answers), cell_format)
            else:
                ws_planning.write(row, 1, str(answers), cell_format)
            row += 1
        
        ws_planning.set_column(0, 0, 40)
        ws_planning.set_column(1, 1, 50)
    
    # Growth Projections Sheet
    if 'growth_projections' in session_state:
        ws_projections = workbook.add_worksheet('Growth Projections')
        projections_data = session_state['growth_projections']
        
        headers = ['Field', 'Value']
        ws_projections.write_row(0, 0, headers, header_format)
        
        ws_projections.write(1, 0, 'Growth Rate', cell_format)
        ws_projections.write(1, 1, projections_data.get('growth_rate', 'N/A'), cell_format)
        
        ws_projections.set_column(0, 0, 20)
        ws_projections.set_column(1, 1, 30)

    # Taxation Planning Sheet
    if 'taxation_module' in session_state:
        ws_tax = workbook.add_worksheet('Taxation Planning')
        tax_data = session_state['taxation_module']
        
        headers = ['Section', 'Question', 'Response']
        ws_tax.write_row(0, 0, headers, header_format)
        
        row = 1
        tax_sections = {
            'Strategic Tax Planning': 'strategic_tax_planning',
            'Tactical Tax Planning': 'tactical_tax_planning',
            'Compliance Tax Planning': 'compliance_tax_planning',
            'Investment Tax Planning': 'investment_tax_planning',
            'Deductions and Exemptions': 'deductions_exemptions',
            'Income Structuring': 'income_structuring',
            'Tax Incentives': 'tax_incentives',
            'Global Tax Planning': 'global_tax_planning',
            'Deferral Strategies': 'deferral_strategies',
            'Estate Planning': 'estate_planning'
        }
        
        for section_name, section_key in tax_sections.items():
            if section_key in tax_data:
                section_data = tax_data[section_key]
                for question, answer in section_data.items():
                    ws_tax.write(row, 0, section_name, cell_format)
                    ws_tax.write(row, 1, question.replace('_', ' ').title(), cell_format)
                    ws_tax.write(row, 2, str(answer), cell_format)
                    row += 1
        
        # Set column widths
        ws_tax.set_column(0, 0, 25)  # Section column
        ws_tax.set_column(1, 1, 40)  # Question column
        ws_tax.set_column(2, 2, 50)  # Response column
    
    workbook.close()
    output.seek(0)
    return output
def create_custom_styles():
    base_styles = getSampleStyleSheet()
    
    try:
        pdfmetrics.registerFont(TTFont('Lato', 'fonts/Lato-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('Lato-Bold', 'fonts/Lato-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('Lato-Italic', 'fonts/Lato-Italic.ttf'))
        pdfmetrics.registerFont(TTFont('Lato-BoldItalic', 'fonts/Lato-BoldItalic.ttf'))
        base_font = 'Lato'
        bold_font = 'Lato-Bold'
    except:
        base_font = 'Helvetica'
        bold_font = 'Helvetica-Bold'

    custom_styles = {}
    
    # Normal style (both capitalized and lowercase versions)
    custom_styles['Normal'] = ParagraphStyle(
        'Normal',
        parent=base_styles['Normal'],
        fontSize=10,
        leading=12,
        fontName=base_font,
        alignment=TA_JUSTIFY
    )
    
    custom_styles['normal'] = custom_styles['Normal']  # Add lowercase version
    
    # TOC style
    custom_styles['TOCEntry'] = ParagraphStyle(
        'TOCEntry',
        parent=base_styles['Normal'],
        fontSize=12,
        leading=16,
        leftIndent=20,
        fontName=base_font,
        alignment=TA_JUSTIFY
    )
    
    custom_styles['toc'] = custom_styles['TOCEntry']  # Add lowercase version
    
    # Title style
    custom_styles['title'] = ParagraphStyle(
        'CustomTitle',
        parent=custom_styles['Normal'],  # Changed parent to our custom Normal
        fontSize=24,
        textColor=colors.HexColor('#2B6CB0'),
        alignment=TA_CENTER,
        spaceAfter=30,
        fontName=bold_font,
        leading=28.8
    )
    
    # Heading style
    custom_styles['heading'] = ParagraphStyle(
        'CustomHeading',
        parent=custom_styles['Normal'],  # Changed parent to our custom Normal
        fontSize=26,
        textColor=colors.HexColor('#1a1a1a'),
        spaceBefore=20,
        spaceAfter=15,
        fontName=bold_font,
        leading=40.5,
        alignment=TA_JUSTIFY
    )
    
    # Subheading style
    custom_styles['subheading'] = ParagraphStyle(
        'CustomSubheading',
        parent=custom_styles['Normal'],  # Changed parent to our custom Normal
        fontSize=12,
        textColor=colors.HexColor('#4A5568'),
        spaceBefore=15,
        spaceAfter=10,
        fontName=bold_font,
        leading=18.2,
        alignment=TA_JUSTIFY
    )
    
    # Content style
    custom_styles['content'] = ParagraphStyle(
        'CustomContent',
        parent=custom_styles['Normal'],  # Changed parent to our custom Normal
        fontSize=10,
        textColor=colors.HexColor('#1a1a1a'),
        alignment=TA_JUSTIFY,
        spaceBefore=6,
        spaceAfter=6,
        fontName=base_font,
        leading=15.4
    )
    
    # Bullet style
    custom_styles['bullet'] = ParagraphStyle(
        'CustomBullet',
        parent=custom_styles['Normal'],  # Changed parent to our custom Normal
        fontSize=10,
        textColor=colors.HexColor('#1a1a1a'),
        leftIndent=20,
        firstLineIndent=0,
        fontName=base_font,
        leading=15.4,
        alignment=TA_JUSTIFY
    )
    
    # Add any additional required style variations
    custom_styles['BodyText'] = custom_styles['Normal']
    custom_styles['bodytext'] = custom_styles['Normal']
    
    return custom_styles
def clean_text(text):
    """Clean and format text by removing HTML tags and normalizing line breaks"""
    if not text:
        return ""
    
    # Remove HTML tags while preserving line breaks
    text = re.sub(r'<br\s*/?>', '\n', text)  # Convert <br> to newlines
    text = re.sub(r'<para>', '', text)        # Remove <para> tags
    text = re.sub(r'</para>', '', text)       # Remove </para> tags
    text = re.sub(r'<[^>]+>', '', text)       # Remove any other HTML tags
    
    # Remove style tags
    text = re.sub(r'<userStyle>.*?</userStyle>', '', text)
    
    # Remove Markdown formatting while preserving structure
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    text = re.sub(r'_(.*?)_', r'\1', text)        # Underscore
    
    # Improve spacing around punctuation
    text = re.sub(r':(?!\s)', ': ', text)         # Add space after colons
    text = re.sub(r'\s+([.,;!?])', r'\1', text)   # Remove space before punctuation
    text = re.sub(r'([.,;!?])(?!\s)', r'\1 ', text)  # Add space after punctuation
    
    # Handle multiple newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Normalize multiple newlines to double
    text = text.replace('\r\n', '\n')         # Normalize Windows line endings
    
    # Handle bullet points and dashes
    lines = text.split('\n')
    processed_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith(('-', '•', '*')):
            line = '• ' + line[1:].strip()  # Normalize bullet points
        processed_lines.append(line)
    
    text = '\n'.join(processed_lines)
    
    return text.strip()

def process_content(content, styles, elements):
    """Process content with improved handling of lists and formatting"""
    if not content:
        return
    
    # Clean the content first
    content = clean_text(content)
    
    # Split content into sections
    sections = content.split('\n')
    current_paragraph = []
    
    i = 0
    while i < len(sections):
        line = sections[i].strip()
        
        # Skip empty lines
        if not line:
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                elements.append(Paragraph(para_text, styles['content']))
                elements.append(Spacer(1, 0.1*inch))
                current_paragraph = []
            i += 1
            continue
        
        # Handle headings
        if line.startswith('###') and not line.startswith('####'):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                elements.append(Paragraph(para_text, styles['content']))
                current_paragraph = []
            
            heading_text = line.replace('###', '').strip()
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph(heading_text, styles['subheading']))
            elements.append(Spacer(1, 0.15*inch))
            
        elif line.startswith('####'):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                elements.append(Paragraph(para_text, styles['content']))
                current_paragraph = []
            
            subheading_text = line.replace('####', '').strip()
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(subheading_text, styles['subheading']))
            elements.append(Spacer(1, 0.1*inch))
            
        # Handle bullet points
        elif line.startswith('•'):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                elements.append(Paragraph(para_text, styles['content']))
                current_paragraph = []
            
            bullet_text = line[1:].strip()
            elements.append(Paragraph(bullet_text, styles['bullet']))
            
        # Handle tables
        elif '|' in line:
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                elements.append(Paragraph(para_text, styles['content']))
                current_paragraph = []
            
            # Collect table lines
            table_lines = [line]
            while i + 1 < len(sections) and '|' in sections[i + 1]:
                i += 1
                table_lines.append(sections[i].strip())
            
            # Process table
            if table_lines:
                process_table_content(table_lines, styles, elements)
                
        else:
            # Handle bold text and normal content
            processed_line = line
            if '**' in processed_line:
                processed_line = re.sub(r'\*\*(.*?)\*\*', lambda m: f'<b>{m.group(1)}</b>', processed_line)
            
            current_paragraph.append(processed_line)
        
        i += 1
    
    # Handle any remaining paragraph content
    if current_paragraph:
        para_text = ' '.join(current_paragraph)
        elements.append(Paragraph(para_text, styles['content']))
        elements.append(Spacer(1, 0.1*inch))
def create_formatted_table(table_data, styles):
    """Create a professionally formatted table with consistent styling"""
    # Ensure all rows have the same number of columns
    max_cols = max(len(row) for row in table_data)
    table_data = [row + [''] * (max_cols - len(row)) for row in table_data]
    
    # Calculate dynamic column widths based on content length
    total_width = 6.5 * inch
    col_widths = []
    
    if max_cols > 1:
        # Calculate max content length for each column
        col_lengths = [0] * max_cols
        for row in table_data:
            for i, cell in enumerate(row):
                content_length = len(str(cell))
                col_lengths[i] = max(col_lengths[i], content_length)
                
        # Distribute widths proportionally based on content length
        total_length = sum(col_lengths)
        for length in col_lengths:
            width = max((length / total_length) * total_width, inch)  # Minimum 1 inch
            col_widths.append(width)
            
        # Adjust widths to fit page
        scale = total_width / sum(col_widths)
        col_widths = [w * scale for w in col_widths]
    else:
        col_widths = [total_width]
    
    # Create table with calculated widths
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    # Define table style commands
    style_commands = [
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E5E7EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
        ('TOPPADDING', (0, 0), (-1, 0), 15),
        
        # Content styling
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        
        # Grid styling
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2B6CB0')),
        
        # Alignment
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Cell padding
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]
    
    # Apply style commands
    table.setStyle(TableStyle(style_commands))
    
    # Apply word wrapping
    wrapped_data = []
    for i, row in enumerate(table_data):
        wrapped_row = []
        for cell in row:
            if isinstance(cell, (str, int, float)):
                # Use content style for all cells except headers
                style = styles['subheading'] if i == 0 else styles['content']
                wrapped_cell = Paragraph(str(cell), style)
            else:
                wrapped_cell = cell
            wrapped_row.append(wrapped_cell)
        wrapped_data.append(wrapped_row)
    
    # Create final table with wrapped data
    final_table = Table(wrapped_data, colWidths=col_widths, repeatRows=1)
    final_table.setStyle(TableStyle(style_commands))
    
    return final_table

def create_highlight_box(text, styles):
    """Create a highlighted box with improved styling"""
    content = Paragraph(f"• {text}", styles['content'])
    
    table = Table(
        [[content]],
        colWidths=[6*inch],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BORDER', (0,0), (-1,-1), 1, colors.black),
            ('PADDING', (0,0), (-1,-1), 15),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOX', (0,0), (-1,-1), 2, colors.HexColor('#E2E8F0')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 18),
            ('TOPPADDING', (0,0), (-1,-1), 18),
        ])
    )
    
    return table

def process_table_content(lines, styles, elements):
    """Process table content with improved header handling"""
    table_data = []
    header_processed = False
    
    for line in lines:
        if '-|-' in line:  # Skip separator lines
            continue
            
        cells = [cell.strip() for cell in line.split('|')]
        cells = [cell for cell in cells if cell]
        
        if cells:
            # Handle cells with bold markers
            cells = [re.sub(r'\*\*(.*?)\*\*', r'\1', cell) for cell in cells]
            
            # Create paragraphs with appropriate styles
            if not header_processed:
                cells = [Paragraph(str(cell), styles['subheading']) for cell in cells]
                header_processed = True
            else:
                cells = [Paragraph(str(cell), styles['content']) for cell in cells]
                
            table_data.append(cells)
    
    if table_data:
        elements.append(Spacer(1, 0.2*inch))
        table = create_formatted_table(table_data, styles)
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
def create_ascii_table(headers, rows, column_widths=None):
    """Create an ASCII table for email formatting."""
    if column_widths is None:
        # Calculate column widths based on content
        column_widths = []
        for i in range(len(headers)):
            column_content = [str(row[i]) for row in rows] + [headers[i]]
            column_widths.append(max(len(str(x)) for x in column_content) + 2)

    # Create the header separator
    separator = '+' + '+'.join('-' * width for width in column_widths) + '+'

    # Create the header
    header_row = '|' + '|'.join(
        str(headers[i]).center(column_widths[i])
        for i in range(len(headers))
    ) + '|'

    # Create the rows
    data_rows = []
    for row in rows:
        data_row = '|' + '|'.join(
            str(row[i]).center(column_widths[i])
            for i in range(len(row))
        ) + '|'
        data_rows.append(data_row)

    # Combine all parts
    table = '\n'.join([
        separator,
        header_row,
        separator,
        '\n'.join(data_rows),
        separator
    ])

    return table
def send_combined_email_with_attachments(receiver_email, company_name, subject, body, pdf_buffer, excel_buffer, statistics, contact_details, tax_pdf_buffer):
    """Send email with Business PDF, Tax PDF, and Excel report attachments"""
    try:
        # Log attempt
        logging.info(f"Attempting to send email to: {receiver_email}")
        
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = receiver_email
        msg['Subject'] = f"{subject} - {company_name}"

        # Create statistics tables
        summary_headers = ['Metric', 'Input', 'Output', 'Total']
        summary_rows = [
            ['Words', 
             f"{statistics['total_input_words']:,}", 
             f"{statistics['total_output_words']:,}",
             f"{statistics['total_input_words'] + statistics['total_output_words']:,}"],
            ['Tokens', 
             f"{statistics['total_input_tokens']:,}", 
             f"{statistics['total_output_tokens']:,}",
             f"{statistics['total_input_tokens'] + statistics['total_output_tokens']:,}"]
        ]
        summary_table = create_ascii_table(summary_headers, summary_rows)

        # Create the email body with formatting
        formatted_body = f"""Dear Recipient,

{body}

{contact_details}

Company Name: {company_name}
Generated Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

ANALYSIS STATISTICS SUMMARY:
{summary_table}

Best regards,
CEAI Business Analysis Team"""

        # Attach the formatted body
        msg.attach(MIMEText(formatted_body, 'plain'))

        # Helper function to create attachments
        def create_pdf_attachment(pdf_data, filename):
            pdf_attachment = MIMEBase('application', 'octet-stream')
            pdf_attachment.set_payload(pdf_data.getvalue())
            encoders.encode_base64(pdf_attachment)
            pdf_attachment.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"'
            )
            return pdf_attachment

        # Create sanitized company name for filenames
        sanitized_company_name = "".join(x for x in company_name if x.isalnum() or x in (' ', '-', '_')).strip()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')

        # Attach Business Analysis PDF
        business_pdf_filename = f"business_analysis_{sanitized_company_name}_{timestamp}.pdf"
        msg.attach(create_pdf_attachment(pdf_buffer, business_pdf_filename))

        # Attach Tax Analysis PDF
        tax_pdf_filename = f"tax_analysis_{sanitized_company_name}_{timestamp}.pdf"
        msg.attach(create_pdf_attachment(tax_pdf_buffer, tax_pdf_filename))

        # Prepare and attach Excel
        excel_attachment = MIMEBase('application', 'octet-stream')
        excel_attachment.set_payload(excel_buffer.getvalue())
        encoders.encode_base64(excel_attachment)
        excel_filename = f"business_analysis_input_{sanitized_company_name}_{timestamp}.xlsx"
        excel_attachment.add_header(
            'Content-Disposition',
            f'attachment; filename="{excel_filename}"'
        )
        msg.attach(excel_attachment)

        # Create SSL context and send email
        context = ssl.create_default_context()
        try:
            # Try SSL first (port 465)
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                logging.info("Connected with SSL")
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
        except Exception as ssl_error:
            logging.warning(f"SSL connection failed: {str(ssl_error)}")
            logging.info("Trying TLS connection...")
            # If SSL fails, try TLS (port 587)
            with smtplib.SMTP(SMTP_SERVER, 587) as server:
                server.starttls(context=context)
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)

        st.success(f"Reports sent successfully to {receiver_email} for {company_name}.")
        logging.info(f"Email sent successfully to {receiver_email}")
        
    except Exception as e:
        error_msg = f"Error sending email: {str(e)}"
        logging.error(error_msg, exc_info=True)
        st.error(error_msg)
        print(f"Detailed email error: {str(e)}") # For debugging# For debugging
def calculate_analysis_statistics(session_state):
    """
    Calculate word and token counts for input and output separately.
    """
    statistics = {
        'total_input_words': 0,
        'total_input_tokens': 0,
        'total_output_words': 0,
        'total_output_tokens': 0,
        'input_counts': {},
        'output_counts': {}
    }
    
    # Input fields to analyze
    input_keys = [
        'business_profile',
        'business_priorities',
        'working_capital',
        'strategic_planning',
        'growth_projections'
    ]
    
    # Output fields to analyze
    output_keys = [
        'business_profile_analysis',
        'priorities_analysis',
        'executive_summary',
        'capital_analysis',
        'strategic_analysis',
        'financial_projections'
    ]
    
    def count_words(text):
        if not text:
            return 0
        if isinstance(text, dict):
            text = str(text)
        return len([word for word in str(text).split() if word.strip()])
    
    def count_tokens(text):
        if not text:
            return 0
        if isinstance(text, dict):
            text = str(text)
        words = count_words(text)
        punctuation = len([char for char in str(text) if char in '.,!?;:()[]{}""\''])
        return words + punctuation
    
    # Calculate input counts
    for key in input_keys:
        if key in session_state and session_state[key]:
            words = count_words(session_state[key])
            tokens = count_tokens(session_state[key])
            statistics['input_counts'][key] = {
                'words': words,
                'tokens': tokens
            }
            statistics['total_input_words'] += words
            statistics['total_input_tokens'] += tokens
    
    # Calculate output counts
    for key in output_keys:
        if key in session_state and session_state[key]:
            words = count_words(session_state[key])
            tokens = count_tokens(session_state[key])
            statistics['output_counts'][key] = {
                'words': words,
                'tokens': tokens
            }
            statistics['total_output_words'] += words
            statistics['total_output_tokens'] += tokens
    
    # Add selected business options analysis if present
    if 'business_options' in session_state:
        for option in session_state['business_options']:
            key = f"{option.lower().replace(' ', '_')}_analysis"
            if key in session_state and session_state[key]:
                words = count_words(session_state[key])
                tokens = count_tokens(session_state[key])
                statistics['output_counts'][key] = {
                    'words': words,
                    'tokens': tokens
                }
                statistics['total_output_words'] += words
                statistics['total_output_tokens'] += tokens
    
    return statistics


def process_paragraph(para, styles, elements):
    """Process individual paragraph with enhanced formatting"""
    clean_para = clean_text(para)
    if not clean_para:
        return
    
    # Handle bulleted lists
    if clean_para.startswith(('•', '-', '*', '→')):
        text = clean_para.lstrip('•-*→ ').strip()
        bullet_style = ParagraphStyle(
            'BulletPoint',
            parent=styles['content'],
            leftIndent=20,
            firstLineIndent=0,
            spaceBefore=6,
            spaceAfter=6,
            bulletIndent=10,
            bulletFontName='Symbol'
        )
        elements.append(Paragraph(f"• {text}", bullet_style))
        elements.append(Spacer(1, 0.05*inch))
    
    # Handle numbered points
    elif re.match(r'^\d+\.?\s+', clean_para):
        text = re.sub(r'^\d+\.?\s+', '', clean_para)
        elements.extend([
            Spacer(1, 0.1*inch),
            create_highlight_box(text, styles),
            Spacer(1, 0.1*inch)
        ])
    
    # Handle quoted text
    elif clean_para.strip().startswith('"') and clean_para.strip().endswith('"'):
        quote_style = ParagraphStyle(
            'Quote',
            parent=styles['content'],
            fontSize=11,
            leftIndent=30,
            rightIndent=30,
            spaceBefore=12,
            spaceAfter=12,
            leading=16,
            textColor=colors.HexColor('#2D3748'),
            borderColor=colors.HexColor('#E2E8F0'),
            borderWidth=1,
            borderPadding=10,
            borderRadius=5
        )
        elements.append(Paragraph(clean_para, quote_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Handle section titles
    elif re.match(r'^[A-Z][^.!?]*:$', clean_para):
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(clean_para, styles['subheading']))
        elements.append(Spacer(1, 0.1*inch))
    
    # Handle special metrics or scores
    elif "Overall Score:" in clean_para or re.match(r'^[\d.]+%|[$€£¥][\d,.]+', clean_para):
        metric_style = ParagraphStyle(
            'Metric',
            parent=styles['content'],
            fontSize=11,
            textColor=colors.HexColor('#2B6CB0'),
            spaceAfter=6
        )
        elements.append(Paragraph(clean_para, metric_style))
    
    # Regular paragraphs
    else:
        elements.append(Paragraph(clean_para, styles['content']))
        elements.append(Spacer(1, 0.05*inch))
# Utility Functions
def get_openai_response(prompt, system_content, api_key):
    """
    Function to interact with OpenAI API.
    """
    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error communicating with OpenAI API: {str(e)}")
        return None

def initialize_session_state():
    """
    Initialize the session state variables
    """
    if 'show_options' not in st.session_state:
        st.session_state.show_options = False
    if 'show_profile' not in st.session_state:
        st.session_state.show_profile = False
    if 'show_business_priority' not in st.session_state:
        st.session_state.show_business_priority = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
def render_personal_profile_form():
    """Render the personal profile form at the start of the application"""
    with st.form(key="personal_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name*", key="full_name")
            email = st.text_input("Email Address*", key="email")
        
        with col2:
            phone = st.text_input("Mobile Number*", key="phone")
        
        # Additional company information
        if 'business_profile' in st.session_state:
            company_name = st.session_state['business_profile'].get('company_name', '')
        else:
            company_name = ''

        submit = st.form_submit_button("AI Insight")
        if submit:
            # Validate required fields
            if not all([full_name, email, phone]):
                st.error("Please fill in all required fields marked with *")
                return None
            
            # Validate email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address")
                return None
            
            # Store in session state and return
            profile_data = {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "company_name": company_name,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return profile_data
    return None
def render_header():
    """Render application header"""
    col1, col2 = st.columns([3, 1])
    with col1:
        logo_path = "smeimge.jpg"
        if os.path.exists(logo_path):
            st.image(logo_path, width=100)
    with col2:
        logo_path = "finb.jpg"
        if os.path.exists(logo_path):
            st.image(logo_path, width=100)

# Form Rendering Functions
def render_business_profile_form():
    st.write("### Business Profile")
    with st.form(key="business_profile_form"):
        company_name = st.text_input("Company Name")
        
        business_model = st.text_area(
            "Describe how your company makes money (max 150 words)",
            max_chars=850
        )
        
        products_services = st.text_area(
            "Describe your products/services (max 150 words)",
            max_chars=850
        )
        
        industry = st.selectbox(
            "Select your industry",
            options=[
                "Accommodation and Food Service Activities",
                "Administrative and Support Service Activities",
                "Agriculture, Forestry, and Fishing",
                "Arts, Entertainment, and Recreation",
                "Construction",
                "Education",
                "Electricity, Gas, Steam, and Air Conditioning Supply",
                "Financial and Insurance/Takaful Activities",
                "Human Health and Social Work Activities",
                "Information and Communication",
                "Manufacturing",
                "Mining and Quarrying",
                "Professional, Scientific, and Technical Activities",
                "Public Administration and Defence; Compulsory Social Security",
                "Real Estate Activities",
                "Transportation and Storage",
                "Water Supply, Sewerage, Waste Management, and Remediation Activities",
                "Wholesale and Retail Trade; Repair of Motor Vehicles and Motorcycles",
                "Others please specify"
            ]
        )
        
        other_industry_details = None
        if industry == "Others please specify":
            other_industry_details = st.text_input("Please specify your industry")

        incorporation_status = st.radio(
            "Is your company incorporated in Malaysia with primary business operations based locally?",
            ["Yes", "No", "Others"]
        )
        
        other_incorporation_details = None
        if incorporation_status == "Others":
            other_incorporation_details = st.text_input("Please specify your incorporation status")

        primary_currency = st.selectbox(
            "Select your primary currency",
            options=[
                "Malaysian Ringgit (MYR)",
                "United States Dollar (USD)",
                "Euro (EUR)",
                "British Pound Sterling (GBP)",
                "Japanese Yen (JPY)",
                "Australian Dollar (AUD)",
                "Canadian Dollar (CAD)",
                "Swiss Franc (CHF)",
                "Chinese Yuan (CNY)",
                "Singapore Dollar (SGD)",
                "Indian Rupee (INR)",
                "New Zealand Dollar (NZD)",
                "South Korean Won (KRW)",
                "Hong Kong Dollar (HKD)",
                "Thai Baht (THB)",
                "Philippine Peso (PHP)",
                "Indonesian Rupiah (IDR)",
                "Vietnamese Dong (VND)",
                "Saudi Riyal (SAR)",
                "Emirati Dirham (AED)",
                "Turkish Lira (TRY)",
                "Brazilian Real (BRL)",
                "South African Rand (ZAR)",
                "Mexican Peso (MXN)",
                "Russian Ruble (RUB)"
            ]
        )

        revenue_size = st.radio(
            "My annual revenue size is between (choose one)",
            ["<1m", "1 - 5m", "5 - 10m", ">10 - 30m", ">30 - 50m", ">50m"]
        )

        profit_range = st.radio(
            "Company's profit range? (choose one)",
            ["<100k", "100 - 500k", ">500k - 1m", ">1 - 5m", ">5 - 10m", ">10m"]
        )

        operating_cashflow = st.radio(
            "Company's operating cashflow range? (choose one)",
            ["<0", "0 - 100k", "100 - 500k", ">500k - 1m", ">1 - 5m", ">5m"]
        )

        debt_equity_ratio = st.radio(
            "Company's Debt/Equity Ratio (Choose one)",
            ["<0.5", "0.5 - 1.0x", ">1.0 - 3x", ">3x"]
        )

        shareholders_funds = st.radio(
            "Shareholder's funds range? (Choose one)",
            ["<500k", "500k - 1m", "1 - 5m", ">5 - 10m", ">10 - 30m", ">30 - 50m", ">50m"]
        )

        staff_strength = st.radio(
            "Current staff strength (choose one)",
            ["<5", "5 - 10", ">10 - 30", ">30 - 50", ">50 - 80", ">80 - 100", ">100"]
        )

        customer_type = st.radio(
            "My current customers (choose one)",
            ["Only domestic", "Mix of domestic and foreign/off-shore", "Only off-shore"]
        )

        submit = st.form_submit_button("AI Insight")
        if submit:
            if industry == "Others please specify" and not other_industry_details:
                st.error("Please specify your industry if you selected 'Others'.")
                return None
            if incorporation_status == "Others" and not other_incorporation_details:
                st.error("Please specify your incorporation status if you selected 'Others'.")
                return None
            
            return {
                "company_name": company_name,
                "business_model": business_model,
                "products_services": products_services,
                "industry": industry if industry != "Others please specify" else other_industry_details,
                "incorporation_status": incorporation_status if incorporation_status != "Others" else other_incorporation_details,
                "primary_currency": primary_currency,
                "revenue_size": revenue_size,
                "profit_range": profit_range,
                "operating_cashflow": operating_cashflow,
                "debt_equity_ratio": debt_equity_ratio,
                "shareholders_funds": shareholders_funds,
                "staff_strength": staff_strength,
                "customer_type": customer_type
            }
    return None

def render_business_priority_form():
    st.write("### Business Priorities")
    with st.form(key="business_priority_form"):
        business_priorities = st.text_area(
            "Tell me more about your business priorities in the next 6 - 12 months (User Maximum 180 words)",
            max_chars=1080,
            height=200
        )
        
        submit = st.form_submit_button("AI Insight")
        if submit:
            if not business_priorities.strip():
                st.error("Please provide details about your business priorities.")
                return None
            return {"business_priorities": business_priorities}
    return None

def render_business_options(business_priorities, openai_api_key):
    if 'business_priority_suggestions' not in st.session_state.user_data:
        with st.spinner("Analyzing your business priorities..."):
            suggestions = business_priority(business_priorities, openai_api_key)
            if suggestions:
                st.session_state.user_data['business_priority_suggestions'] = suggestions
    
    if st.session_state.user_data.get('business_priority_suggestions'):
        with st.expander("Business Priority Suggestions", expanded=True):
            st.write("Here are some business priority suggestions based on your input:")
            st.markdown(st.session_state.user_data['business_priority_suggestions'])
    
    st.write("### Business Areas for Analysis")
    st.write("Based on your priorities, select the relevant business areas:")
    
    with st.form(key="business_options_form"):
        selected_options = {}
        cols = st.columns(3)
        
        for idx, (option, description) in enumerate(BUSINESS_OPTIONS.items()):
            col = cols[idx % 3]
            with col:
                with st.expander(f"📊 {option}", expanded=False):
                    st.markdown(f"**{description}**")
                    selected_options[option] = st.checkbox("Select this area", key=f"checkbox_{option}")
        
        submit = st.form_submit_button("💫 Generate Analysis for Selected Areas")
        if submit:
            return selected_options
    return None

def render_working_capital_form():
    st.write("### Working Capital Planning")
    with st.form(key="working_capital_form"):
        funding_amount = st.radio(
            "How much funding do you plan to set aside at present and in the future?",
            options=["<1m", "1 - 5m", "5 - 10m", ">10 - 30m", ">30 - 50m", ">50m"]
        )

        st.write("Purpose of raising funds? (Choose 1 or more)")
        purpose_options = {
            "To expand business operations.": st.checkbox("To expand business operations."),
            "To launch new products or services.": st.checkbox("To launch new products or services."),
            "To pay off existing debts.": st.checkbox("To pay off existing debts."),
            "To invest in technology upgrades.": st.checkbox("To invest in technology upgrades."),
            "To hire and train additional staff.": st.checkbox("To hire and train additional staff."),
            "To enter new markets.": st.checkbox("To enter new markets."),
            "To improve cash flow and working capital.": st.checkbox("To improve cash flow and working capital."),
            "To acquire another company.": st.checkbox("To acquire another company."),
            "To enhance marketing and branding efforts.": st.checkbox("To enhance marketing and branding efforts."),
            "To build inventory and manage supply chain demands.": st.checkbox("To build inventory and manage supply chain demands."),
            "Others please specify": st.checkbox("Others please specify")
        }

        other_purpose = None
        if purpose_options["Others please specify"]:
            other_purpose = st.text_input("Please specify other purposes")

        st.write("Debt or equity preference? (Choose 1 or more)")
        funding_types = {
            "Debt": st.checkbox("Debt", key="funding_type_debt"),
            "Equity": st.checkbox("Equity", key="funding_type_equity"),
            "Both": st.checkbox("Both", key="funding_type_both"),
            "Others please specify": st.checkbox("Others please specify", key="funding_type_others")
        }

        other_funding_type = None
        if funding_types["Others please specify"]:
            other_funding_type = st.text_input("Please specify other funding type")

        submit = st.form_submit_button("AI Insight")
        if submit:
            if purpose_options["Others please specify"] and not other_purpose:
                st.error("Please specify other purposes for raising funds.")
                return None
            if funding_types["Others please specify"] and not other_funding_type:
                st.error("Please specify other funding type.")
                return None
            
            return {
                "funding_amount": funding_amount,
                "funding_purposes": purpose_options,
                "other_purpose": other_purpose,
                "funding_types": funding_types,
                "other_funding_type": other_funding_type
            }
    return None

def render_strategic_planning_form():
    st.write("### Strategic Planning")
    with st.form(key="strategic_planning_form"):
        # Complete list of strategic questions
        strategic_questions = {
            "What best describes your business goal?": [
                "Expanding into new markets",
                "Increasing revenue or profitability",
                "Launching a new product or service",
                "Securing funding or investment"
            ],
            "What key milestone do you prioritize?": [
                "Achieving a specific revenue target",
                "Building a strong brand presence",
                "Creating operational efficiency",
                "Entering a new market"
            ],
            "How would you define your business focus?": [
                "Offering innovative products or services",
                "Meeting a specific customer need",
                "Building a trusted brand in the market",
                "Becoming a market leader in your industry"
            ],
            "What is your unique value proposition?": [
                "Providing unmatched quality",
                "Offering cost-effective solutions",
                "Delivering exceptional customer service",
                "Introducing innovative solutions"
            ],
            "Who is your primary target audience?": [
                "Young professionals or millennials",
                "Small businesses or startups",
                "Large enterprises or corporations",
                "General consumers"
            ],
            "What is your approach to competition?": [
                "Offer better quality at competitive prices",
                "Focus on niche markets competitors overlook",
                "Create superior customer experience",
                "Leverage innovation to stay ahead"
            ],
            "What best describes your organizational structure?": [
                "Flat structure for agility",
                "Hierarchical structure for clear roles",
                "Collaborative teams for innovation",
                "Outsourced or lean operations"
            ],
            "What is your management team's priority?": [
                "Driving innovation and growth",
                "Maintaining operational efficiency",
                "Fostering teamwork and collaboration",
                "Achieving financial targets"
            ],
            "What is the focus of your product/service?": [
                "Solving a specific customer pain point",
                "Offering unique features not available elsewhere",
                "Providing cost savings to customers",
                "Delivering premium quality or value"
            ],
            "What is your product/service strategy?": [
                "Continuously innovate and improve offerings",
                "Expand offerings based on customer needs",
                "Build long-term customer loyalty",
                "Focus on a specific niche market"
            ],
            "What is your primary marketing focus?": [
                "Building brand awareness",
                "Generating leads and conversions",
                "Retaining existing customers",
                "Expanding into new markets"
            ],
            "What is your sales strategy?": [
                "Focus on high-value customers",
                "Drive sales through digital channels",
                "Build relationships through personal engagement",
                "Expand through strategic partnerships"
            ],
            "What is critical to your daily operations?": [
                "Streamlining workflows with technology",
                "Ensuring customer satisfaction",
                "Managing supply chain and logistics",
                "Monitoring financial performance"
            ],
            "Where do you plan to invest operationally?": [
                "Upgrading technology and tools",
                "Expanding team and workforce",
                "Improving facilities or infrastructure",
                "Strengthening supplier relationships"
            ],
            "What is your revenue focus?": [
                "Diversify income streams",
                "Maximize profitability in core areas",
                "Balance steady income with high growth",
                "Secure funding to expand operations"
            ],
            "What is your funding requirement?": [
                "Scaling business operations",
                "Launching new products or services",
                "Expanding market presence",
                "Addressing operational challenges"
            ],
            "What do you see as your primary risk?": [
                "Market competition",
                "Financial uncertainty",
                "Operational inefficiency",
                "Customer retention"
            ],
            "How do you plan to mitigate risks?": [
                "Develop contingency plans",
                "Diversify offerings",
                "Build strong financial reserves",
                "Strengthen customer relationships"
            ]
        }

        # Collect user responses
        responses = {}
        for question, options in strategic_questions.items():
            st.write(question)
            responses[question] = []
            for option in options:
                if st.checkbox(option, key=f"{question}_{option}"):
                    responses[question].append(option)
            st.write("")  # Add spacing between questions

        # Submit button
        submit = st.form_submit_button("AI Insight")
        if submit:
            if all(len(responses[q]) > 0 for q in strategic_questions):
                return responses
            else:
                st.error("Please select at least one option for each question.")
    return None

def render_financial_projections_form():
    st.write("### Growth Rate Projections")
    with st.form(key="growth_projections_form"):
        growth_rate = st.radio(
            "What's your average expansion growth rate annually that is sustainable?",
            ["<0%", "1 - 5%", "5 - 10%", ">10 - 30%", ">30 - 50%", ">50 - 100%", ">100 - 500%"],
            key="growth_rate"
        )

        submit = st.form_submit_button("AI Insight")
        if submit:
            return {
                "growth_rate": growth_rate
            }
    return None

# GPT Processing Functions
def process_business_profile_with_gpt(form_data, api_key):
    prompt = f"""
    Analyze the whole information provided in 1500 words, supported by relevant facts and figures:

    {form_data}

    - Provide a company profile analysis:
        - Include an industry overview with supporting facts and figures, as well as relevant statistics for the industry.
        - Conduct a SWOT analysis based on the provided industry description.
        - Offer a comprehensive financial and operating summary, blending the provided data with macro analysis and the competitive environment.
        - Create an in-depth analysis of the business needs as outlined by the user.

    1..main header comes w summary for that section : 600 words. 
    2. Section header: dedicate and force 2 pages only per section.. means all the sub sections force to 2 pages for that section: 1500 words
    *Model Illustration*
   -Create a summary table with a basic explanation based on the above(must be in table format)
    """
    return get_openai_response(
        prompt,
        "You are a business consultant analyzing the business profile data to provide detailed and actionable recommendations.",
        api_key
    )

def process_business_priorities_with_gpt(form_data, api_key):
    prompt = f"""
    Expand and analyze the given points with the following requirements:

    {form_data}

    - Expand the given points and provide a detailed explanation.
    - Synthesize and organize the inputs into a coherent structure.
    - Explain with possible examples or scenarios for better understanding.
    - Provide strategic implications and their potential impact.
    - Ensure the analysis is concise, within 450 words, and supported by relevant facts and figures.

    1..main header comes w summary for that section : 600 words. 
    2. Section header: dedicate and force 2 pages only per section.. means all the sub sections force to 2 pages for that section: 1500 words
    *Model Illustration*
   -Create a summary table with a basic explanation based on the above(must be in table format)
    """
    return get_openai_response(
        prompt,
        "You are a strategic consultant providing detailed insights and recommendations based on business priorities.",
        api_key
    )

def business_priority(business_info, openai_api_key):
    prompt = f"""Based on the following business priorities:

{business_info}

Please provide a comprehensive 450-word analysis with the following structure:

1. Expanded Analysis 
   - Break down each priority into key components
   - Identify underlying objectives and goals
   - Highlight critical success factors
   - Discuss potential challenges and constraints

2. Synthesis and Organization 
   - Categorize priorities by strategic importance
   - Identify interconnections between different priorities
   - Create a logical framework for implementation
   - Establish priority hierarchy

3. Practical Examples 
   - For each major priority, provide:
     * A specific implementation example
     * Real-world success case
     * Potential adaptation strategies

4. Strategic Implications 
   - Impact on business operations
   - Resource requirements
   - Timeline considerations
   - Risk assessment
   - Success metrics

*Model Illustration*
-Create a summary table with a basic explanation based on the above(must be in table format)

Include supporting facts and figures throughout the analysis to validate recommendations and insights.
Ensure all sections include supporting facts, figures, and relevant industry statistics where applicable. 
The analysis should be data-driven and provide actionable insights.
Format all numerical examples in plain text with proper spacing no numbering point

"""

    return get_openai_response(
        prompt,
        "You are a strategic business advisor providing comprehensive priority analysis with practical insights and clear examples.",
        openai_api_key
    )

def get_specific_suggestions(business_info, suggestion_type, openai_api_key):
    prompt = f"""Based on the user's stated business priorities:
{business_info}

Provide a {suggestion_type} analysis with exactly these requirements (Maximum 500 words):

1. Explain how to focus energy and resources on activities that directly support your stated priority - give 5 examples and explain analytically and state clearly how the cmopany can learn from each case.
2. How to develop a clear plan with measurable milestones to ensure consistent progress toward your goal. Highlight and explain the importance of structured goal-setting in the specific context. 
3. Explain how to delegate tasks that do not align with your priority to maintain focus and efficiency - give examples om how to promote  prioritization and productivity.
4. Explain how to Communicate your priorities clearly to your team to ensure alignment and collective action." Provide examples on how to emphasize the value of shared understanding and collaboration.
5. Explain how to Regularly review your progress and adapt your approach to stay aligned with your desired outcomes." Give examples on how to Advocate for continuous evaluation and flexibility in this situation.

*Model Illustration*
-Create a summary table with a basic explanation based on the above(must be in table format)

Ensure all sections include supporting facts, figures, and relevant industry statistics where applicable. 
The analysis should be data-driven and provide actionable insights.
Format all numerical examples in plain text with proper spacing no numbering point

"""

    return get_openai_response(
        prompt,
        f"You are a specialized {suggestion_type} consultant responding to specific business priorities.",
        openai_api_key
    )

def process_working_capital_with_gpt(form_data, api_key):
    prompt = f"""
    Please provide a comprehensive working capital analysis (maximum 600 words) that covers the following key areas:

    1. Working Planning Requirements Summary:
    - Analyze the submitted working capital plan details, and propose the typical use of the funds based on a similar company profile operating in the same industry.
    - Provide a concise overview of the key planning elements, relative to the industry that the company is operating. Include industry dynamics with supporting facts and figures.
    {form_data}

    2. Funding Purpose Analysis:
    - Evaluate the required funding amount in relation to stated purposes and explain what are the typical uses. 
    -Propose % allocation based on the uses that are commonly applied in the similar industy. Explain the rationale. Tabulate the results. State a footnote on the table that this is a suggestion only.
    - Provide quantitative analysis of funding usage, and exlpain the cost items in more details specific to this situation.

    3. Risk Assessment:
    - Identify potential risks associated with each funding purpose
    - Analyze severity and likelihood of identified risks
    - Suggest risk mitigators for each of the risks identified.

    4. Benefits and Impact Analysis:
    - Detail potential benefits for each funding purpose
    - Quantify expected impact where possible in a table format
    - Evaluate both short-term and long-term benefits of supporting this project.

    1..main header comes w summary for that section : 1200 words. 
    2. Section header: dedicate and force 2 pages only per section.. means all the sub sections force to 2 pages for that section: 1500 words
    *Model Illustration*
    -Create a summary table with a basic explanation based on the above(must be in table format)
    """
    
    return get_openai_response(
        prompt,
        "You are a financial analyst specializing in working capital management, providing detailed analysis and recommendations based on submitted plan data.",
        api_key
    )

def process_strategic_planning_with_gpt(form_data, api_key):
    prompt = f"""
    Provide a comprehensive strategic business analysis based on the following planning data:

    {form_data}

    1. Business Strategy Assessment:
    - Analyze the alignment between stated business goals and target audience
    - Evaluate the coherence of value proposition with market positioning
    - Assess the relationship between product/service strategy and revenue focus

    2. Operational & Resource Analysis:
    - Examine the alignment of organizational structure with management priorities
    - Evaluate operational investment plans against critical daily needs
    - Analyze the connection between funding requirements and planned investments

    3. Market & Competition Strategy:
    - Assess the effectiveness of marketing and sales strategies for the target audience
    - Evaluate competitive approach in relation to unique value proposition
    - Analyze market expansion plans and potential barriers

    4. Risk Management & Sustainability:
    - Identify potential conflicts between different strategic elements
    - Evaluate the comprehensiveness of risk mitigation strategies
    - Assess the long-term sustainability of the proposed strategies

    5. Recommendations:
    - Provide specific, actionable recommendations for strategy optimization
    - Identify quick wins and long-term strategic initiatives
    - Suggest performance metrics for tracking strategic success

    1..main header comes w summary for that section : 600 words. 
    2. Section header: dedicate and force 2 pages only per section.. means all the sub sections force to 2 pages for that section: 1500 words
    *Model Illustration*
    -Create a summary table with a basic explanation based on the above(must be in table format)
    """
    
    return get_openai_response(
        prompt,
        "You are a strategic business consultant specializing in comprehensive business strategy analysis, providing detailed insights and actionable recommendations based on submitted strategic planning data.",
        api_key
    )

def process_financial_projections_with_gpt(form_data, company_data, api_key):
    """Generate 5-year financial projections"""
    prompt = f"""
    Based on the company's historical data:
    Annual Revenue Size: {company_data['business_profile'].get('revenue_size')}
    Profit Range: {company_data['business_profile'].get('profit_range')}
    Operating Cashflow Range: {company_data['business_profile'].get('operating_cashflow')}
    Debt/Equity Ratio: {company_data['business_profile'].get('debt_equity_ratio')}
    Shareholder's Funds Levels: {company_data['business_profile'].get('shareholders_funds')}
    Currency:{company_data['business_profile'].get('primary_currency')}
    Growth Rate Selected: {form_data['growth_rate']}

    Please extrapolate and provide detailed 5-year financial projections with the following requirements:
    Use these projected expansion growth rate (annually)  to extrapolate their topline and bottom line annually in the next 5 years , BASED ON THE COMPANY'S DATA PROVIDED EARLIER
    Propose a discount rate (%) and discounted cashflow analysis of the company based on the financial projections based on the fund raising amount proposed earlier.
    Derive and provide the final answer for the Net Present Value (NPV) amount from the DCF and explain narraitvely witn supporting facts and figures in 500 words.


    *Model Illustration*
    -Create a summary table with a basic explanation based on the above using qualitative and quantitative provide(must be in table format)
    Link these numbers and explain the numbers with the business strategy, neeeds and priorities of the company provided earlier.
    State and explain the growth assumptions narratively in 700 words with supporting facts, figures in % and $ terms , with reference to time frame. 
    Please add subheading  organize the contnet for each part

    """
    return get_openai_response(
        prompt,
        "You are a financial analyst creating detailed 5-year projections based on historical company data and growth assumptions.",
        api_key
    )
def process_financial_projections_with_gpt2(form_data, company_data, api_key):
    """Generate 5-year financial projections"""
    prompt = f"""
    Based on the company's historical data:
    Annual Revenue Size: {company_data['business_profile'].get('revenue_size')}
    Profit Range: {company_data['business_profile'].get('profit_range')}
    Operating Cashflow Range: {company_data['business_profile'].get('operating_cashflow')}
    Debt/Equity Ratio: {company_data['business_profile'].get('debt_equity_ratio')}
    Shareholder's Funds Levels: {company_data['business_profile'].get('shareholders_funds')}
    Growth Rate Selected: {form_data['growth_rate']}

    *Model Illustration*
    -Create a summary table with a basic explanation based on the above(must be in table format)-using both qualitative and quantitative data provided. 
    Link these numbers and explain the numbers with the business strategy, neeeds and priorities of the company provided earlier.
    State and explain the growth assumptions narratively in 700 words with supporting facts, figures in % and $ terms, with reference to time frame. 
    Please add subheading  organize the contnet for each part
    
    Based on the 5-year projections and company profile, provide a 600-word narrative analysis listing 
    List and explain at least 8 risk assumptions to the financial projections in 600 words narratively.
    Format as a narrative discussion with clear sections for each risk.




    """
    return get_openai_response(
        prompt,
        "You are a financial analyst creating detailed 5-year projections based on historical company data and growth assumptions.",
        api_key
    )
def get_business_option_summary(selected_areas, suggestions_data, openai_api_key):
    """
    Create a high-level summary of all selected business options and their suggestions.
    
    Args:
        selected_areas (list): List of selected business options
        suggestions_data (dict): Dictionary containing the detailed suggestions for each area
        openai_api_key (str): OpenAI API key for generating the summary
    
    Returns:
        str: A concise summary of all selected areas and key recommendations
    """
    # Create a consolidated view of all selected areas and their suggestions
    consolidated_info = "\n\n".join([
        f"Area: {area}\n"
        f"Description: {BUSINESS_OPTIONS[area]}\n"
        f"Detailed Analysis: {suggestions_data.get(f'{area.lower().replace(' ', '_')}_analysis', 'No analysis available')}"
        for area in selected_areas
    ])
    
    prompt = f"""Based on the following selected business areas and their detailed analyses, 
    provide a concise executive summary:

    {consolidated_info}

    Please provide a summary that includes:
    1. Overview of selected focus areas and their strategic importance
    2. Key synergies between the different areas
    3. Critical success factors across all areas
    4. Top 3-5 immediate action items
    5. Potential challenges and mitigation strategies

    1..main header is the {consolidated_info}that comes w summary for that section . 
    2. Section header must be smaller by 30% than the main header: dedicate and force 2 pages only per section.. means all the sub sections force to 2 pages for that section
    *Model Illustration*
    -Create a summary table with a basic explanation based on the above(must be in table format)
"""

    return get_openai_response(
        prompt,
        "You are a strategic business consultant best in the world, providing practical, actionable advice and solutions based on the company information. It must relate to the company's priorities, needs and takes into account the industry specific risks and opportunities. Must come with supporting facts, figures and latest statistics. 800 words.",
        openai_api_key
    )
class PDFWithTOC(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        self.personal_info = kwargs.get('personal_info', {})
        if 'personal_info' in kwargs:
            del kwargs['personal_info']
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        self.page_numbers = {}
        self.current_page = 1

    def afterPage(self):
        self.current_page += 1

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            if style == 'heading':
                text = flowable.getPlainText()
                self.page_numbers[text] = self.current_page

def generate_main_pdf(sme_data, personal_info, toc_page_numbers):
    """Generate the main business analysis PDF (up to financial projections)"""
    buffer = io.BytesIO()
    
    doc = PDFWithTOC(
        buffer,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=1.5*inch,
        bottomMargin=inch,
        personal_info=personal_info
    )
    
    templates = [
        PageTemplate(id='First', frames=[Frame(0, 0, letter[0], letter[1], leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
                    onPage=lambda canvas, doc: None),
        PageTemplate(id='Later', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')],
                    onPage=create_header_footer),
        PageTemplate(id='dis', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')],
                    onPage=create_header_footer_disclaimer)
    ]
    doc.addPageTemplates(templates)
    
    styles = create_custom_styles()
    elements = []
    
    # Cover page
    elements.append(NextPageTemplate('First'))
    if os.path.exists("smeboostfront.jpg"):
        img = Image("smeboostfront.jpg", width=letter[0], height=letter[1])
        elements.append(img)
    
    elements.append(NextPageTemplate('Later'))
    elements.append(PageBreak())
    
    # Table of Contents
    elements.append(Paragraph("Table of Contents", styles['heading']))
    
    # Section data for main PDF
    section_data = [
        ("Company Profile Analysis", sme_data['business_profile_analysis']),
        ("Business Priorities Analysis", sme_data['priorities_analysis']),
        ("Business Options Summary", sme_data['executive_summary']),
        ("Working Capital Analysis", sme_data['capital_analysis']),
        ("Strategic Planning Analysis", sme_data['strategic_analysis']),
        ("Financial Projections", sme_data['financial_projections'])
    ]
    
    # Format TOC entries
    toc_style = ParagraphStyle(
        'TOCEntry',
        parent=styles['normal'],
        fontSize=12,
        leading=20,
        leftIndent=20,
        rightIndent=30,
        spaceBefore=10,
        spaceAfter=10,
        fontName='Helvetica'
    )
    styles['toc'] = toc_style

    # Add static Personal Profile entry and other TOC entries
    static_entry = f"1. Personal Profile........................ 3"
    elements.append(Paragraph(static_entry, toc_style))
    
    for i, ((title, _), page_num) in enumerate(zip(section_data, toc_page_numbers), 2):
        dots = '.' * (50 - len(f"{i}. {title}"))
        toc_entry = f"{i}. {title} {dots} {page_num}"
        elements.append(Paragraph(toc_entry, toc_style))
    
    elements.append(PageBreak())
    
    # Personal Profile Page
    elements.extend(create_profile_page(styles, personal_info))
    elements.append(PageBreak())
    
    # Main content sections
    for i, (title, content) in enumerate(section_data):
        elements.append(Paragraph(title, styles['heading']))
        if content:
            process_content(content, styles, elements)
        if i < len(section_data) - 1:
            elements.append(PageBreak())
    
    # Disclaimer and back cover
    elements.append(NextPageTemplate('dis'))
    elements.append(PageBreak())
    create_disclaimer_page(styles, elements)
    
    elements.append(NextPageTemplate('First'))
    elements.append(PageBreak())
    if os.path.exists("smeboostback.png"):
        img = Image("smeboostback.png", width=letter[0], height=letter[1])
        elements.append(img)
    
    doc.build(elements, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer

def generate_tax_pdf(tax_data, personal_info, toc_page_numbers):
    """Generate the tax analysis PDF"""
    buffer = io.BytesIO()
    
    doc = PDFWithTOC(
        buffer,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=1.5*inch,
        bottomMargin=inch,
        personal_info=personal_info
    )
    
    templates = [
        PageTemplate(id='First', frames=[Frame(0, 0, letter[0], letter[1], leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
                    onPage=lambda canvas, doc: None),
        PageTemplate(id='Later', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')],
                    onPage=create_header_footer),
        PageTemplate(id='dis', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')],
                    onPage=create_header_footer_disclaimer)
    ]
    doc.addPageTemplates(templates)
    
    styles = create_custom_styles()
    elements = []
    
    # Cover page
    elements.append(NextPageTemplate('First'))
    if os.path.exists("smeboostfront.jpg"):
        img = Image("smeboostfront.jpg", width=letter[0], height=letter[1])
        elements.append(img)
    
    elements.append(NextPageTemplate('Later'))
    elements.append(PageBreak())
    
    # Table of Contents
    elements.append(Paragraph("Tax Analysis Contents", styles['heading']))
    
    # Tax section data
    section_data = [
        ("Strategic Tax Planning", tax_data['strategic_tax']),
        ("Tactical Tax Planning", tax_data['tactical_tax']),
        ("Tax Compliance Analysis", tax_data['compliance_tax']),
        ("Investment Tax Planning", tax_data['investment_tax']),
        ("Deductions and Exemptions", tax_data['deductions_tax']),
        ("Income Structuring", tax_data['income_tax']),
        ("Tax Incentives", tax_data['incentives_tax']),
        ("Global Tax Planning", tax_data['global_tax']),
        ("Deferral Strategies", tax_data['deferral_tax']),
        ("Estate and Succession Planning", tax_data['estate_tax'])
    ]
    
    # Format TOC entries
    for i, ((title, _), page_num) in enumerate(zip(section_data, toc_page_numbers), 1):
        dots = '.' * (50 - len(f"{i}. {title}"))
        toc_entry = f"{i}. {title} {dots} {page_num}"
        elements.append(Paragraph(toc_entry, styles['toc']))
    
    elements.append(PageBreak())
    
    # Tax content sections
    for i, (title, content) in enumerate(section_data):
        elements.append(Paragraph(title, styles['heading']))
        if content:
            process_content(content, styles, elements)
        if i < len(section_data) - 1:
            elements.append(PageBreak())
    
    # Disclaimer and back cover
    elements.append(NextPageTemplate('dis'))
    elements.append(PageBreak())
    create_disclaimer_page(styles, elements)
    
    elements.append(NextPageTemplate('First'))
    elements.append(PageBreak())
    if os.path.exists("smeboostback.png"):
        img = Image("smeboostback.png", width=letter[0], height=letter[1])
        elements.append(img)
    
    doc.build(elements, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer

def create_profile_page(styles, personal_info):
    elements = []
    elements.append(Spacer(1, 0.5*inch))
    
    title_table = Table(
        [[Paragraph("Personal Profile", styles['heading'])]],
        colWidths=[7*inch],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ])
    )
    elements.append(title_table)
    
    elements.append(Spacer(0.5, 0.1*inch))
    
    # Profile info table
    info_table = Table(
        [
            [Paragraph("Contact Information", styles['subheading'])],
            [Table(
                [
                    ["Full Name", str(personal_info.get('full_name', 'N/A'))],
                    ["Email", str(personal_info.get('email', 'N/A'))],
                    ["Phone", str(personal_info.get('phone', 'N/A'))],
                    ["Report Date", datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')],
                    ["Report ID", f"SME-{str(uuid.uuid4())[:8]}"],
                    ["Status",f"POC"]
                ],
                colWidths=[1.5*inch, 4.5*inch],
                style=TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ])
            )]
        ],
        colWidths=[6*inch],
        style=TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
    )
    
    elements.append(info_table)
    return elements
from reportlab.platypus import Frame, PageTemplate, BaseDocTemplate, PageBreak
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, NextPageTemplate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if hasattr(self, '_pageNumber'):
            self.setFont("Helvetica", 9)
            self.drawRightString(
                letter[0] - 0.5*inch,
                0.5*inch,
                f"Page {self._pageNumber} of {page_count}"
            )

def create_header_footer(canvas, doc):
    """Add header and footer with company logos and page numbers"""
    canvas.saveState()
    
    if doc.page > 1:  # Only show on pages after the first page
        # Adjust position for top-right logos
        x_start = doc.width + doc.leftMargin - 0.5 * inch  # Shift logos slightly to the right
        y_position = doc.height + doc.topMargin - 0.1 * inch
        image_width = 0.5 * inch
        image_height = 0.5 * inch

        # Draw logos
        if os.path.exists("ceai.png"):
            canvas.drawImage(
                "ceai.png", 
                x_start, 
                y_position, 
                width=image_width, 
                height=image_height, 
                mask="auto"
            )
        
        if os.path.exists("capm.png"):
            canvas.drawImage(
                "capm.png", 
                x_start - image_width - 0.1 * inch,
                y_position, 
                width=image_width, 
                height=image_height, 
                mask="auto"
            )
        
        # Get company name from business_profile if available
        if hasattr(doc, 'personal_info') and isinstance(doc.personal_info, dict):
            if 'company_name' in doc.personal_info:
                company_name = doc.personal_info['company_name']
            else:
                # Try to get from business_profile in session state
                import streamlit as st
                company_name = st.session_state.get('business_profile', {}).get('company_name', '')
        else:
            company_name = ''

        # Add Header Text
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(
            doc.leftMargin,
            doc.height + doc.topMargin - 0.1*inch,
            company_name
        )
        
        # Add line below header
        line_y_position = doc.height + doc.topMargin - 0.35 * inch
        canvas.setLineWidth(0.5)
        canvas.line(
            doc.leftMargin,
            line_y_position,
            doc.width + doc.rightMargin,
            line_y_position
        )
        
        # Footer
        canvas.setFont("Helvetica", 9)
        canvas.drawString(
            doc.leftMargin,
            0.5 * inch,
            f"Generated on {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        )
    
    canvas.restoreState()

def create_header_footer_disclaimer(canvas, doc):
    """Add header and footer for disclaimer page"""
    canvas.saveState()
    
    if doc.page > 1:  # Only show on pages after the first page
        # Header logos positioning
        x_start = doc.width + doc.leftMargin - 2.0 * inch
        y_position = doc.height + doc.topMargin - 0.2 * inch
        image_width = 2.0 * inch
        image_height = 0.5 * inch
        
        if os.path.exists("smeimge.jpg"):
            canvas.drawImage(
                "smeimge.jpg", 
                x_start, 
                y_position, 
                width=image_width, 
                height=image_height, 
                mask="auto"
            )
        
        # Header Text
        canvas.setFont("Helvetica-Bold", 27)
        canvas.drawString(
            doc.leftMargin,
            doc.height + doc.topMargin - 0.1*inch,
            "Disclaimer"
        )

        # Line below header
        canvas.setLineWidth(0.5)
        canvas.line(
            doc.leftMargin,
            doc.height + doc.topMargin - 0.30 * inch,
            doc.width + doc.rightMargin,
            doc.height + doc.topMargin - 0.30 * inch
        )

        # Footer
        canvas.setFont("Helvetica", 9)
        canvas.drawString(
            doc.leftMargin,
            0.5 * inch,
            f"Generated on {datetime.datetime.now().strftime('%B %d, %Y')}"
        )
    
    canvas.restoreState()

def create_disclaimer_page(styles, elements):
    """Create disclaimer page content"""
    try:
        pdfmetrics.registerFont(TTFont('Lato', 'fonts/Lato-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('Lato-Bold', 'fonts/Lato-Bold.ttf'))
        base_font = 'Lato'
        bold_font = 'Lato-Bold'
    except:
        base_font = 'Helvetica'
        bold_font = 'Helvetica-Bold'
    
    # Adjusted styles for more compact layout
    disclaimer_styles = {
        'section_header': ParagraphStyle(
            'SectionHeader',
            parent=styles['normal'],
            fontSize=10,  # Reduced from 14
            fontName=bold_font,
            spaceBefore=3,  # Reduced from 12
            spaceAfter=2,
            leading=12   # Reduced from 6
        ),
        'body_text': ParagraphStyle(
            'BodyText',
            parent=styles['normal'],
            fontSize=8,  # Reduced from 10
            fontName=base_font,
            leading=9,  # Reduced from 12
            alignment=TA_JUSTIFY,
            spaceBefore=0,  # Minimal space before paragraphs
            spaceAfter=1    
        )
    }

    # Introduction
    elements.append(Paragraph("Introduction", disclaimer_styles['section_header']))
    intro_text = """The increasing application of Artificial Intelligence (AI) in evaluating financial risks and business strategies reflects the growing trend towards data-driven decision-making. AI's ability to analyze vast datasets, identify patterns, and generate insights can significantly enhance the quality of financial and strategic evaluations. However, it is crucial to understand that AI tools, while powerful, have limitations and inherent risks. This disclaimer outlines the key considerations and limitations of using AI for such evaluations and clarifies the position of CapM and its advisory partners."""
    elements.append(Paragraph(intro_text.strip(), disclaimer_styles['body_text']))
    elements.append(Spacer(1, 0.04*inch))  # Reduced spacing

    # Limitations section
    elements.append(Paragraph("Limitations of AI in Financial and Strategic Evaluations", disclaimer_styles['section_header']))
    
    limitations = {
        "1. Data Dependency and Quality": "AI models rely heavily on the quality and completeness of the data fed into them. The accuracy of the analysis is contingent upon the integrity of the input data. Inaccurate, outdated, or incomplete data can lead to erroneous conclusions and recommendations. Users should ensure that the data used in AI evaluations is accurate and up-to-date.",
        "2. Algorithmic Bias and Limitations": "AI algorithms are designed based on historical data and pre-defined models. They may inadvertently incorporate biases present in the data, leading to skewed results. Additionally, AI models might not fully capture the complexity and nuances of human behavior or unexpected market changes, potentially impacting the reliability of the analysis.",
        "3. Predictive Limitations": "While AI can identify patterns and trends, it cannot predict future events with certainty. Financial markets and business environments are influenced by numerous unpredictable factors such as geopolitical events, economic fluctuations, and technological advancements. AI's predictions are probabilistic and should not be construed as definitive forecasts.",
        "4. Interpretation of Results": "AI-generated reports and analyses require careful interpretation. The insights provided by AI tools are based on algorithms and statistical models, which may not always align with real-world scenarios. It is essential to involve human expertise in interpreting AI outputs and making informed decisions.",
        "5. Compliance and Regulatory Considerations": "The use of AI in financial evaluations and business strategy formulation must comply with relevant regulations and standards. Users should be aware of legal and regulatory requirements applicable to AI applications in their jurisdiction and ensure that their use of AI tools aligns with these requirements."
    }

    for title, content in limitations.items():
        elements.append(Paragraph(title, disclaimer_styles['section_header']))
        elements.append(Paragraph(content.strip(), disclaimer_styles['body_text']))
        elements.append(Spacer(1, 0.02*inch))  # Reduced spacing

    # CapM Disclaimer section
    elements.append(Paragraph("CapM and Advisory Partners' Disclaimer", disclaimer_styles['section_header']))
    capm_intro = "CapM and its advisory partners provide AI-generated reports and insights as a tool to assist in financial and business strategy evaluations. However, the use of these AI-generated analyses is subject to the following disclaimers:"
    elements.append(Paragraph(capm_intro.strip(), disclaimer_styles['body_text']))
    elements.append(Spacer(1, 0.03*inch))  # Reduced spacing

    disclaimers = {
        "1. No Guarantee of Accuracy or Completeness": "While CapM and its advisory partners strive to ensure that the AI-generated reports and insights are accurate and reliable, we do not guarantee the completeness or accuracy of the information provided. The insights are based on the data and models used, which may not fully account for all relevant factors or changes in the market.",
        "2. Not Financial or Professional Advice": "The AI-generated reports and insights are not intended as financial, investment, legal, or professional advice. Users should consult with qualified professionals before making any financial or strategic decisions based on AI-generated reports. CapM and its advisory partners are not responsible for any decisions made based on the reports provided.",
        "3. Limitation of Liability": "CapM and its advisory partners shall not be liable for any loss or damage arising from the use of AI-generated reports and insights. This includes, but is not limited to, any direct, indirect, incidental, or consequential damages resulting from reliance on the reports or decisions made based on them.",
        "4. No Endorsement of Third-Party Tools": "The use of third-party tools and data sources in AI evaluations is at the user's discretion. CapM and its advisory partners do not endorse or guarantee the performance or accuracy of any third-party tools or data sources used in conjunction with the AI-generated reports."
    }

    for title, content in disclaimers.items():
        elements.append(Paragraph(title, disclaimer_styles['section_header']))
        elements.append(Paragraph(content.strip(), disclaimer_styles['body_text']))
        elements.append(Spacer(1, 0.02*inch))  # Reduced spacing

    # Conclusion
    elements.append(Paragraph("Conclusion", disclaimer_styles['section_header']))
    conclusion_text = "AI provides valuable insights and enhances decision-making capabilities in financial risk assessment and business strategy development. However, users must recognize the limitations and risks associated with AI applications. CapM and its advisory partners emphasize the importance of combining AI-generated insights with professional judgment and expertise. Users should carefully consider the limitations outlined in this disclaimer and seek professional advice when making significant financial or strategic decisions."
    elements.append(Paragraph(conclusion_text.strip(), disclaimer_styles['body_text']))
def render_taxation_module_form():
    """Render the complete taxation module form with all 10 sections"""
    st.write("### Taxation Module")
    
    with st.form(key="taxation_module_form"):
        # Section 6.1: Strategic Tax Planning
        st.write("#### 6.1 Strategic Tax Planning")
        
        expansion_plans = st.radio(
            "Have you recently expanded or plan to expand operations into new markets or jurisdictions?",
            options=[
                "Yes, already expanded to new markets",
                "Yes, planning to expand within 12 months",
                "No, not applicable"
            ],
            key="expansion_plans"
        )
        
        tax_friendly_jurisdiction = st.radio(
            "Are you operating or considering operating in tax-friendly jurisdictions like Labuan or Free Trade Zones?",
            options=[
                "Operating in a tax-friendly jurisdiction",
                "Yes, considering operating in Labuan/Free Trade Zones",
                "No, not applicable"
            ],
            key="tax_friendly_jurisdiction"
        )
        
        restructuring = st.radio(
            "Have you restructured or considered restructuring your business ownership in the past year?",
            options=[
                "Currently in restructuring",
                "Yes, actively restructured",
                "No, no restructuring"
            ],
            key="restructuring"
        )
        
        acquisitions = st.radio(
            "Are there planned acquisitions or mergers in the next 12 months?",
            options=[
                "Ongoing for businesses",
                "Yes, exploratory discussions ongoing",
                "No, not applicable"
            ],
            key="acquisitions"
        )
        
        capital_expenditure = st.radio(
            "Are you planning significant capital expenditure in the next fiscal year?",
            options=[
                "Yes, approved expenditure > RM 1 million",
                "Yes, considering expenditure < RM 1 million",
                "No, not applicable"
            ],
            key="capital_expenditure"
        )

        # Section 6.2: Tactical Tax Planning
        st.write("#### 6.2 Tactical Tax Planning")
        
        equipment_purchase = st.radio(
            "Did your business purchase significant equipment or assets this year?",
            options=[
                "Yes, purchased equipment > RM 1 million",
                "Yes, purchased equipment < RM 1 million",
                "No, no equipment purchased"
            ],
            key="equipment_purchase"
        )
        
        advanced_payments = st.radio(
            "Have you utilized advanced payments or pre-year-end expenses for tax deductions?",
            options=[
                "Yes, fully utilized for the current year",
                "Yes, partially utilized",
                "No, not applicable"
            ],
            key="advanced_payments"
        )
        
        operational_expenses = st.radio(
            "Did you accelerate any operational expenses to reduce taxable income?",
            options=[
                "Yes, fully aligned with tax planning",
                "Yes, but missed some opportunities",
                "No, no expenses accelerated"
            ],
            key="operational_expenses"
        )

        # Section 6.3: Compliance Tax Planning
        st.write("#### 6.3 Compliance Tax Planning")
        
        tax_filing_deadlines = st.radio(
            "Have you missed any tax filing deadlines in the past year?",
            options=[
                "Yes, multiple deadlines missed",
                "Yes, one deadline missed",
                "No, all submissions on time"
            ],
            key="tax_filing_deadlines"
        )
        
        audit_notices = st.radio(
            "Have you received any audit notices or inquiries from tax authorities?",
            options=[
                "Yes, frequently audited",
                "Yes, once in the past year",
                "No, not audited"
            ],
            key="audit_notices"
        )
        
        # Section 6.4: Investment Based Tax Planning
        st.write("#### 6.4 Investment Based Tax Planning")
        
        tax_exempt_investments = st.radio(
            "Did your business invest in tax-exempt financial instruments like sukuk bonds?",
            options=[
                "Yes, investments > RM 500,000",
                "Yes, investments < RM 500,000",
                "No such investment"
            ],
            key="tax_exempt_investments"
        )
        
        employee_retirement = st.radio(
            "Have you contributed to employee retirement funds (e.g., EPF)?",
            options=[
                "Yes, contributions meet statutory requirements",
                "Yes, partial compliance",
                "No, no contributions made"
            ],
            key="employee_retirement"
        )
        
        # Section 6.5: Deduction and Exemptions
        st.write("#### 6.5 Deduction and Exemptions")
        
        rd_deductions = st.radio(
            "Have you claimed all eligible deductions for R&D expenditures?",
            options=[
                "Yes, fully claimed",
                "Yes, partially claimed",
                "No, not applicable"
            ],
            key="rd_deductions"
        )
        
        charitable_donations = st.radio(
            "Did you make approved charitable donations?",
            options=[
                "Yes, > RM 100,000 in donations",
                "Yes, < RM 100,000 in donations",
                "No, no donations made"
            ],
            key="charitable_donations"
        )
        
        # Section 6.6: Income Splitting and Structuring
        st.write("#### 6.6 Income Splitting and Structuring")
        
        dividend_distribution = st.radio(
            "Did you distribute dividends or profits to directors or shareholders this year?",
            options=[
                "Yes, significant amounts > RM 500,000",
                "Yes, smaller amounts < RM 500,000",
                "No, no distributions made"
            ],
            key="dividend_distribution"
        )

        # Section 6.7: Tax Incentives and Reliefs Utilization
        st.write("#### 6.7 Tax Incentives and Reliefs Utilization")
        
        sme_tax_rates = st.radio(
            "Does your business qualify for SME tax rates?",
            options=[
                "Yes, below the RM 50 million threshold",
                "No, exceeds revenue limits"
            ],
            key="sme_tax_rates"
        )
        
        # Section 6.8: Global Tax Planning
        st.write("#### 6.8 Global Tax Planning")
        
        double_taxation = st.radio(
            "Have you utilized double taxation relief under applicable DTAs?",
            options=[
                "Yes, fully utilized",
                "Yes, partially utilized",
                "No, not applicable"
            ],
            key="double_taxation"
        )
        
        # Section 6.9: Deferral Strategies
        st.write("#### 6.9 Deferral Strategies")
        
        revenue_deferral = st.radio(
            "Have you deferred any revenue recognition to the next fiscal year?",
            options=[
                "Yes, significant amounts > RM 500,000 deferred",
                "Yes, smaller amounts < RM 500,000 deferred",
                "No, no deferrals made"
            ],
            key="revenue_deferral"
        )
        
        # Section 6.10: Estate and Succession Tax Planning
        st.write("#### 6.10 Estate and Succession Tax Planning")
        
        ownership_transfer = st.radio(
            "Are you planning to transfer ownership of the business to future generations?",
            options=[
                "Yes, confirmed",
                "Yes, exploring options",
                "No, not applicable"
            ],
            key="ownership_transfer"
        )

        submit = st.form_submit_button("Submit Tax Planning Information")
        
        if submit:
            return {
                "strategic_tax_planning": {
                    "expansion_plans": expansion_plans,
                    "tax_friendly_jurisdiction": tax_friendly_jurisdiction,
                    "restructuring": restructuring,
                    "acquisitions": acquisitions,
                    "capital_expenditure": capital_expenditure
                },
                "tactical_tax_planning": {
                    "equipment_purchase": equipment_purchase,
                    "advanced_payments": advanced_payments,
                    "operational_expenses": operational_expenses
                },
                "compliance_tax_planning": {
                    "tax_filing_deadlines": tax_filing_deadlines,
                    "audit_notices": audit_notices
                },
                "investment_tax_planning": {
                    "tax_exempt_investments": tax_exempt_investments,
                    "employee_retirement": employee_retirement
                },
                "deductions_exemptions": {
                    "rd_deductions": rd_deductions,
                    "charitable_donations": charitable_donations
                },
                "income_structuring": {
                    "dividend_distribution": dividend_distribution
                },
                "tax_incentives": {
                    "sme_tax_rates": sme_tax_rates
                },
                "global_tax_planning": {
                    "double_taxation": double_taxation
                },
                "deferral_strategies": {
                    "revenue_deferral": revenue_deferral
                },
                "estate_planning": {
                    "ownership_transfer": ownership_transfer
                }
            }
    return None
def process_strategic_tax_planning(data, business_context, api_key):
    # Analyze expansion plans
    expansion_prompt = f"""
    Based on the response: {data.get('expansion_plans')}
    
    Business Context:
    - Current Industry: {business_context['profile'].get('industry')}
    - Revenue Size: {business_context['profile'].get('revenue_size')}
    - Growth Projections: {business_context['financial_projections']}
    - Strategic Plans: {business_context['strategic_analysis']}

    Provide comprehensive AI recommendations:
    1. Evaluate revenue streams from international operations, referencing Malaysia's Double Taxation Agreements (DTAs) for applicable reliefs on foreign income
    2. Simulate foreign tax credits to minimize double taxation on ASEAN-derived revenue
    3. Recommend optimal tax structures for cross-border operations, such as holding companies or joint ventures in tax-efficient jurisdictions
    4. Identify tax incentives for businesses expanding into Malaysia, particularly in Labuan or Free Trade Zones, with compliance details under Section 4A (Income Tax Act 1967)
    5. Create a summary table based on the points above

    Include specific calculations, timelines, and implementation steps.
    """
    expansion_analysis = get_openai_response(expansion_prompt, "You are a tax expansion specialist", api_key)

    # Analyze tax-friendly jurisdiction operations
    jurisdiction_prompt = f"""
    Based on the response: {data.get('tax_friendly_jurisdiction')}
    
    Business Context:
    - Current Operations: {business_context['profile'].get('business_model')}
    - Financial Status: {business_context['financial_projections']}
    - Strategic Goals: {business_context['strategic_analysis']}

    Provide detailed AI recommendations:
    1. Assess the feasibility of relocating to Labuan IBFC, benefiting from 3% tax on trading profits or RM 20,000 flat tax for trading companies
    2. Provide insights into operational models for businesses in Labuan International Business and Financial Centre (IBFC) and Free Trade Zones, considering tax exemptions and reduced customs duties
    3. Recommend compliance strategies under the Labuan Offshore Financial Services Act 1996 and Free Trade Zone (FTZ) regulations for smoother tax operations
    4. Create a summary table based on the points above

    Include specific requirements, benefits calculations, and regulatory compliance steps.
    """
    jurisdiction_analysis = get_openai_response(jurisdiction_prompt, "You are a tax jurisdiction expert", api_key)

    # Analyze restructuring considerations
    restructuring_prompt = f"""
    Based on the response: {data.get('restructuring')}
    
    Business Context:
    - Company Structure: {business_context['profile'].get('incorporation_status')}
    - Financial Analysis: {business_context['financial_projections']}
    - Strategic Plans: {business_context['strategic_analysis']}

    Provide AI-driven restructuring recommendations:
    1. Recommend tax-efficient restructuring strategies to optimize transfer pricing compliance under Section 140A and minimize tax exposure
    2. Analyze the implications of restructuring on withholding taxes for dividend distributions to non-resident shareholders under Section 109 (Income Tax Act 1967)
    3. Propose a review of current ownership structures for alignment with Section 140A (related-party transactions) and identify opportunities for tax savings
    4. Create a summary table based on the points above

    Include impact analysis and compliance requirements.
    """
    restructuring_analysis = get_openai_response(restructuring_prompt, "You are a business restructuring tax expert", api_key)

    # Analyze M&A plans
    acquisition_prompt = f"""
    Based on the response: {data.get('acquisitions')}
    
    Business Context:
    - Company Size: {business_context['profile'].get('revenue_size')}
    - Financial Status: {business_context['financial_projections']}
    - Strategic Goals: {business_context['strategic_analysis']}

    Provide AI-driven M&A tax recommendations:
    1. Simulate the tax impact of acquisitions, including stamp duty exemptions for corporate restructuring under Stamp Act 1949
    2. Analyze the tax efficiency of acquisition costs, either as deductible expenses or capitalized under Schedule 3 of the Income Tax Act 1967
    3. Identify potential tax incentives for merged entities such as group relief provisions and the treatment of tax losses in mergers
    4. Create a summary table based on the points above


    Include detailed tax implications and optimization strategies.
    """
    acquisition_analysis = get_openai_response(acquisition_prompt, "You are an M&A tax specialist", api_key)

    # Analyze capital expenditure plans
    capex_prompt = f"""
    Based on the response: {data.get('capital_expenditure')}
    
    Business Context:
    - Current Assets: {business_context['profile'].get('shareholders_funds')}
    - Financial Projections: {business_context['financial_projections']}
    - Capital Planning: {business_context['capital_analysis']}

    Provide AI recommendations for capital expenditure:
    1. Model tax savings from Accelerated Capital Allowances (ACA) schemes under Budget 2023 and identify qualifying asset categories
    2. Assess eligibility for Investment Tax Allowances (ITA) for sectors like manufacturing or renewable energy under Promotion of Investments Act 1986
    3. Provide timing recommendations to maximize capital allowances for asset purchases and recommend ways to structure expenditures for better tax benefits
    4. Create a summary table based on the points above

    Include quantitative analysis and optimization strategies.
    """
    capex_analysis = get_openai_response(capex_prompt, "You are a capital expenditure tax expert", api_key)

    # Combine all analyses into a structured report
    complete_analysis = f"""
    # Strategic Tax Planning Analysis

    ## 1. Market Expansion Strategy
    {expansion_analysis}

    ## 2. Tax-Friendly Jurisdiction Analysis
    {jurisdiction_analysis}

    ## 3. Business Restructuring Considerations
    {restructuring_analysis}

    ## 4. Mergers & Acquisitions Tax Planning
    {acquisition_analysis}

    ## 5. Capital Expenditure Tax Strategy
    {capex_analysis}
    """

    return complete_analysis
def process_tactical_tax_planning(data, business_context, api_key):
    """Process tactical tax planning questions and provide AI-driven recommendations"""
    
    # Equipment purchase analysis
    equipment_prompt = f"""
    Based on the response: {data.get('equipment_purchase')}
    
    Business Context:
    - Industry: {business_context['profile'].get('industry')}
    - Current Assets: {business_context['profile'].get('shareholders_funds')}
    - Financial Projections: {business_context['financial_projections']}
    - Capital Planning: {business_context['capital_analysis']}

    Provide detailed AI recommendations:
    1. Calculate Initial Allowance (IA) [20%] and Annual Allowance (AA) [14%] under Schedule 3 to maximize asset depreciation
        - Show detailed calculations
        - Provide timeline for claims
        - Impact on tax savings
    
    2. Identify specific asset categories eligible for higher capital allowance rates (e.g., green technology or energy-efficient equipment)
        - List qualifying categories
        - Additional rates available
        - Documentation requirements
    
    3. Recommend filing amendments if prior-year unclaimed capital allowances are identified
        - Review procedure
        - Time limitations
        - Potential benefits
    4. Create a summary table based on the points above


    Include specific calculations, timelines, and regulatory references.
    """
    equipment_analysis = get_openai_response(equipment_prompt, "You are a capital allowance tax expert", api_key)

    # Advanced payments analysis
    payments_prompt = f"""
    Based on the response: {data.get('advanced_payments')}
    
    Business Context:
    - Operating Cash Flow: {business_context['profile'].get('operating_cashflow')}
    - Working Capital: {business_context['capital_analysis']}
    - Financial Status: {business_context['financial_projections']}

    Provide AI-driven recommendations:
    1. Identify prepaid expenses eligible for tax deductions under Section 33(1)
        - List qualifying recurring operational costs like rent, insurance, software licenses
        - Timing requirements
        - Documentation needed
    
    2. Simulate the financial impact of accelerating pre-year-end expenses
        - Calculate potential tax savings
        - Cash flow implications
        - Optimization strategies
    
    3. Recommend changes to maximize allowable deductions
        - Timing strategies
        - Documentation requirements
        - Risk mitigation
    4. Create a summary table based on the points above

    Include quantitative analysis and compliance requirements.
    """
    payments_analysis = get_openai_response(payments_prompt, "You are a tax deduction specialist", api_key)

    # Operational expenses analysis
    expenses_prompt = f"""
    Based on the response: {data.get('operational_expenses')}
    
    Business Context:
    - Current Expenses: {business_context['profile'].get('operating_cashflow')}
    - Financial Planning: {business_context['financial_projections']}
    - Strategic Goals: {business_context['strategic_analysis']}

    Provide comprehensive AI recommendations:
    1. Suggest accelerating employee bonuses, marketing costs, or other deductible expenses
        - List eligible expenses
        - Timing considerations
        - Tax impact calculations
    
    2. Recommend structuring operations for tax-efficient expense timing
        - Operational adjustments needed
        - Implementation timeline
        - Cost-benefit analysis
    
    3. Strategies for minimizing income during high-tax periods
        - Expense planning
        - Timing optimization
        - Risk considerations

    4. Create a summary table based on the points above

    Include practical implementation steps and compliance requirements.
    """
    expenses_analysis = get_openai_response(expenses_prompt, "You are an operational tax planning expert", api_key)

    # Combine all analyses into a structured report
    complete_analysis = f"""
    # Tactical Tax Planning Analysis

    ## 1. Equipment and Asset Purchase Strategy
    {equipment_analysis}

    ## 2. Advanced Payments and Pre-year-end Expenses
    {payments_analysis}

    ## 3. Operational Expense Optimization
    {expenses_analysis}

    """
    return complete_analysis
def process_compliance_tax_planning(data, business_context, api_key):
    """Process compliance tax planning questions and provide AI-driven recommendations"""
    
    # Filing deadlines analysis
    deadlines_prompt = f"""
    Based on the response: {data.get('tax_filing_deadlines')}
    
    Business Context:
    - Business Type: {business_context['profile'].get('incorporation_status')}
    - Industry: {business_context['profile'].get('industry')}
    - Revenue Size: {business_context['profile'].get('revenue_size')}
    - Financial Status: {business_context['financial_projections']}

    Provide detailed AI recommendations focusing on:
    1. Automate compliance tracking and calculate penalties:
        - Calculate potential penalties (RM 200/day under Section 112) for late filings
        - Detailed penalty breakdown by filing type
        - Total exposure assessment
    
    2. Highlight compliance issues:
        - Review Form C (corporate tax) requirements and deadlines
        - Analyze Form E (employee tax returns) obligations
        - Identify missing or incomplete submissions
    
    3. Propose solutions:
        - Compliance tracking system recommendations
        - Filing schedule optimization
        - Internal control improvements

    4. Create a summary table based on the points above

    Include specific timelines, calculations, and regulatory references.
    """
    deadlines_analysis = get_openai_response(deadlines_prompt, "You are a tax compliance expert", api_key)

    # Audit notices analysis
    audit_prompt = f"""
    Based on the response: {data.get('audit_notices')}
    
    Business Context:
    - Financial Records: {business_context['capital_analysis']}
    - Business Operations: {business_context['profile_analysis']}
    - Tax History: {business_context['strategic_analysis']}

    Provide comprehensive AI recommendations:
    1. Identify common audit triggers:
        - Analysis of unreported income risks
        - Review of large deductions
        - Assessment of potential audit outcomes
        - Industry-specific risk factors
    
    2. Record-keeping improvements:
        - Compliance strategies for Section 82A requirements
        - Documentation system recommendations
        - Internal control enhancements
        - Digital record-keeping solutions
    
    3. Audit preparation strategy:
        - Document organization protocols
        - Response procedures
        - Risk mitigation steps

    4. Create a summary table based on the points above

    Include practical implementation steps and compliance requirements.
    """
    audit_analysis = get_openai_response(audit_prompt, "You are a tax audit specialist", api_key)

    # Combine analyses into structured report
    complete_analysis = f"""
    # Tax Compliance Planning Analysis

    ## 1. Filing Compliance Assessment
    {deadlines_analysis}

    ## 2. Audit Readiness Evaluation
    {audit_analysis}
    
    """

    return complete_analysis
def process_investment_tax_planning(data, business_context, api_key):
    """Process investment tax planning questions and provide AI-driven recommendations"""
    
    # Sukuk bonds investment analysis
    sukuk_prompt = f"""
    Based on the response: {data.get('tax_exempt_investments')}
    
    Business Context:
    - Investment Amount: {business_context['profile'].get('shareholders_funds')}
    - Financial Position: {business_context['financial_projections']}
    - Cash Flow Status: {business_context['capital_analysis']}

    Provide detailed AI recommendations:
    1. Tax Savings Analysis:
        - Calculate specific tax savings from sukuk bond exemptions under Income Tax (Exemption) Order 2011
        - Provide detailed calculations based on investment amount
        - Show annual tax benefit projections
    
    2. Investment Comparison:
        - Compare tax-exempt sukuk bonds to other taxable instruments for return on investment
        - Analyze after-tax returns
        - Evaluate risk-adjusted returns
        - Consider liquidity factors
    
    3. Optimization Strategy:
        - Recommend optimal investment allocation
        - Suggest timing of investments
        - Identify additional tax-efficient instruments

    4. Create a summary table based on the points above


    Include quantitative analysis and specific calculations.
    """
    sukuk_analysis = get_openai_response(sukuk_prompt, "You are an investment tax expert", api_key)

    # Employee retirement funds analysis
    epf_prompt = f"""
    Based on the response: {data.get('employee_retirement')}
    
    Business Context:
    - Employee Count: {business_context['profile'].get('staff_strength')}
    - Business Size: {business_context['profile'].get('revenue_size')}
    - Growth Plans: {business_context['strategic_analysis']}

    Provide comprehensive AI recommendations:
    1. EPF Compliance Verification:
        - Verify full EPF contribution compliance under Section 34(4)
        - Calculate mandatory contribution requirements
        - Assess current compliance status
        - Identify gaps in compliance
    
    2. Tax Deductions Optimization:
        - Recommend additional voluntary contributions to maximize tax deductions
        - Calculate potential tax savings
        - Propose contribution strategies
    
    3. Employee Retention Benefits:
        - Simulate potential tax benefits of EPF contributions in increasing employee retention
        - Analyze cost-benefit of increased contributions
        - Recommend retention-focused strategies

    4. Create a summary table based on the points above


    Include practical implementation steps and calculations.
    """
    epf_analysis = get_openai_response(epf_prompt, "You are an employee benefits tax specialist", api_key)

    # Combine analyses into structured report
    complete_analysis = f"""
    # Investment-Based Tax Planning Analysis

    ## 1. Sukuk Bond Investment Strategy
    {sukuk_analysis}

    ## 2. Employee Retirement Fund Planning
    {epf_analysis}

    """

    return complete_analysis

def process_deductions_exemptions(data, business_context, api_key):
    """Process deductions and exemptions analysis focusing on R&D and charitable donations"""
    
    # R&D expenditure analysis
    rd_prompt = f"""
    Based on the response: {data.get('rd_deductions')}
    
    Business Context:
    - Industry: {business_context['profile'].get('industry')}
    - Business Model: {business_context['profile'].get('business_model')}
    - Strategic Plans: {business_context['strategic_analysis']}
    - Financial Status: {business_context['financial_projections']}

    Provide detailed AI recommendations:
    1. R&D Eligibility Verification:
        - Verify R&D activities against Section 34A requirements
        - Analyze alignment with Public Ruling No. 5/2022 for double deduction eligibility
        - Assess current R&D documentation
        - Identify compliance gaps
    
    2. Additional R&D Opportunities:
        - Identify additional R&D expenses eligible for claims
        - Focus on prototype development costs
        - Analyze software-related R&D expenses
        - Calculate potential additional deductions
    
    3. Implementation Strategy:
        - Documentation requirements
        - Claim procedure optimization
        - Risk mitigation steps

    4. Create a summary table based on the points above

    Include specific calculations and regulatory references.
    """
    rd_analysis = get_openai_response(rd_prompt, "You are an R&D tax specialist", api_key)

    # Charitable donations analysis
    donations_prompt = f"""
    Based on the response: {data.get('charitable_donations')}
    
    Business Context:
    - Revenue Size: {business_context['profile'].get('revenue_size')}
    - Profit Range: {business_context['profile'].get('profit_range')}
    - Financial Projections: {business_context['financial_projections']}

    Provide comprehensive AI recommendations:
    1. Deduction Limit Analysis:
        - Calculate deduction limits under Section 44(6)
        - Analyze 10% aggregate income cap
        - Project potential tax savings
        - Optimize donation timing
    
    2. Donation Structure Optimization:
        - Advise on structuring donations for maximum allowable reliefs
        - Recommend approved institutions
        - Suggest optimal donation timing
        - Calculate tax benefit scenarios
    
    3. Implementation Strategy:
        - Documentation requirements
        - Compliance procedures
        - Record-keeping recommendations

    4. Create a summary table based on the points above

    Include practical calculations and implementation steps.
    """
    donations_analysis = get_openai_response(donations_prompt, "You are a charitable tax deductions expert", api_key)

    # Combine analyses into structured report
    complete_analysis = f"""
    # Deductions and Exemptions Analysis

    ## 1. R&D Expenditure Deductions
    {rd_analysis}

    ## 2. Charitable Donations Strategy
    {donations_analysis}

    """

    return complete_analysis

def process_income_structuring(data, business_context, api_key):
    """Process income splitting and structuring analysis focusing on dividend distributions"""
    
    dividend_prompt = f"""
    Based on the response about dividend distributions: {data.get('dividend_distribution')}
    
    Business Context:
    - Revenue: {business_context['profile'].get('revenue_size')}
    - Profit: {business_context['profile'].get('profit_range')}
    - Company Structure: {business_context['profile'].get('incorporation_status')}
    - Financial Performance: {business_context['financial_projections']}

    Provide detailed analysis focusing on two key areas:

    1. Withholding Tax Analysis:
        a) Calculate the withholding tax implications for distributions under Section 109:
           - For non-resident shareholders
           - Based on actual distribution amount (>{data.get('dividend_distribution', '')})
           - Impact on company's cash flow
           - Impact on shareholders' net receipts
    
    2. Profit Allocation Strategy:
        a) Recommend tax-efficient distribution strategies focusing on:
           - Low-taxed individuals
           - Tax-efficient entities
           - Optimal timing of distributions
           - Alternative distribution methods

    For each recommendation, provide:
    - Specific calculations with amounts
    - Tax implications
    - Implementation steps
    - Required documentation
    - Risk considerations
    - Create a summary table based on the points above
    """
    
    analysis = get_openai_response(dividend_prompt, "You are an income structuring tax expert", api_key)
    
    # Structure the complete analysis
    complete_analysis = f"""
    # Income Splitting and Structuring Analysis

    {analysis}

    """
    
    return complete_analysis

def process_tax_incentives(data, business_context, api_key):
    """Process tax incentives analysis focusing on SME tax rates and eligibility"""
    
    sme_prompt = f"""
    Based on the response about SME qualification: {data.get('sme_tax_rates')}
    
    Business Context:
    - Annual Revenue: {business_context['profile'].get('revenue_size')}
    - Business Model: {business_context['profile'].get('business_model')}
    - Industry: {business_context['profile'].get('industry')}
    - Financial Projections: {business_context['financial_projections']}

    Provide detailed analysis for:

    1. SME Tax Rate Eligibility:
        a) Confirm eligibility for 17% tax rate:
           - Analyze first RM 600,000 of taxable income
           - Reference Budget 2025 requirements
           - Calculate potential tax savings
           - Compare with standard tax rates
    
    2. Revenue Management Strategy:
        a) If below threshold:
           - Recommend strategies to maintain SME status
           - Project revenue growth impact
           - Suggest operational optimizations
        
        b) If exceeding threshold:
           - Analyze impact of losing SME status
           - Propose revenue structuring options
           - Calculate cost-benefit of maintaining status

    Include:
    - Specific tax savings calculations
    - Revenue threshold management strategies
    - Implementation timeline
    - Risk considerations
    - Create a summary table based on the points above
    """
    
    analysis = get_openai_response(sme_prompt, "You are a SME tax incentives expert", api_key)
    
    # Structure the complete analysis
    complete_analysis = f"""
    # Tax Incentives and Reliefs Analysis

    {analysis}

    """
    
    return complete_analysis

def process_global_tax_planning(data, business_context, api_key):
    """Process global tax planning analysis focusing on double taxation relief and DTA compliance"""
    
    dta_prompt = f"""
    Based on the response about DTA utilization: {data.get('double_taxation')}
    
    Business Context:
    - International Operations: {business_context['profile'].get('customer_type')}
    - Revenue Scale: {business_context['profile'].get('revenue_size')}
    - Foreign Income: {business_context['financial_projections']}
    - Business Model: {business_context['profile'].get('business_model')}

    Provide detailed analysis focusing on:

    1. Double Taxation Relief Automation:
        a) Identify eligible reliefs under Malaysia's DTA network:
           - Analyze current foreign income streams
           - Map applicable DTAs
           - Calculate maximum foreign tax credits
           - Identify unutilized relief opportunities
    
        b) Relief Maximization Strategy:
           - Review current DTA utilization
           - Calculate potential additional claims
           - Identify optimization opportunities
           - Project tax savings

    2. Compliance Framework:
        a) Provide comprehensive templates for:
           - Relief claim documentation
           - Foreign income reporting
           - Tax credit calculations
           - Compliance checklists
        
        b) Double Taxation Prevention:
           - Income characterization guidelines
           - DTA application procedures
           - Documentation requirements
           - Filing deadlines

    For each recommendation, include:
    - Specific calculations
    - Implementation steps
    - Required documentation
    - Risk considerations
    - Timeline for action
    - Create a summary table based on the points above
    """
    
    analysis = get_openai_response(dta_prompt, "You are a global tax planning expert", api_key)
    
    # Structure the complete analysis
    complete_analysis = f"""
    # Global Tax Planning Analysis

    {analysis}

    """
    
    return complete_analysis

def process_deferral_strategies(data, business_context, api_key):
    """Process deferral strategies analysis focusing on revenue recognition timing"""
    
    deferral_prompt = f"""
    Based on the response about revenue deferrals: {data.get('revenue_deferral')}
    
    Business Context:
    - Current Revenue: {business_context['profile'].get('revenue_size')}
    - Cash Flow Status: {business_context['profile'].get('operating_cashflow')}
    - Growth Projections: {business_context['financial_projections']}
    - Business Model: {business_context['profile'].get('business_model')}

    Provide detailed analysis focusing on:

    1. Financial Impact Simulation:
        a) Model impact of deferred income:
           - Calculate effect on current year taxable income
           - Project impact on cash flow
           - Analyze working capital implications
           - Compare scenarios with different deferral amounts
    
        b) Quantitative Analysis:
           - Current vs. Deferred tax liability
           - Cash flow timing differences
           - Working capital adjustments
           - Net present value of deferrals

    2. Strategic Deferral Planning:
        a) Revenue shifting recommendations:
           - Identify high-income to lower-tax period opportunities
           - Compliance requirements with Revenue Recognition Rules
           - Timing optimization strategies
           - Documentation requirements
        
        b) Risk Management:
           - Compliance considerations
           - Cash flow management
           - Documentation needs
           - Audit defense preparation

    Include:
    - Specific calculations showing tax impacts
    - Cash flow projections
    - Implementation timeline
    - Compliance checklist
    - Create a summary table based on the points above
    """
    
    analysis = get_openai_response(deferral_prompt, "You are a tax deferral strategies expert", api_key)
    
    # Structure the complete analysis
    complete_analysis = f"""
    # Deferral Strategies Analysis

    {analysis}

    """
    
    return complete_analysis

def process_estate_succession_planning(data, business_context, api_key):
    """Process estate and succession tax planning focusing on business ownership transfer"""
    
    succession_prompt = f"""
    Based on the response about ownership transfer: {data.get('ownership_transfer')}
    
    Business Context:
    - Company Value: {business_context['profile'].get('shareholders_funds')}
    - Business Model: {business_context['profile'].get('business_model')}
    - Industry: {business_context['profile'].get('industry')}
    - Financial Performance: {business_context['financial_projections']}

    Provide detailed analysis focusing on:

    1. Wealth Transfer Strategy Modeling:
        a) Family Trust Structure Analysis:
           - Evaluate trust options under Malaysia Trust Act 2013
           - Calculate inheritance tax minimization potential
           - Compare different trust structures
           - Assess compliance requirements
    
        b) Long-term Benefits:
           - Tax savings projections
           - Wealth preservation strategies
           - Control retention options
           - Succession timeline planning

    2. Share Transfer Simulation:
        a) Compare Gifting vs. Inheritance:
           - Calculate tax implications of each approach
           - Project multi-generational tax savings
           - Assess timing considerations
           - Evaluate control transfer options
        
        b) Implementation Framework:
           - Documentation requirements
           - Legal compliance steps
           - Transfer timing optimization
           - Risk management strategies

    Include:
    - Specific calculations for different scenarios
    - Implementation steps and timeline
    - Required documentation
    - Risk considerations
    - Regulatory compliance requirements
    - Create a summary table based on the points above
    """
    
    analysis = get_openai_response(succession_prompt, "You are an estate and succession planning expert", api_key)
    
    # Structure the complete analysis
    complete_analysis = f"""
    # Estate and Succession Tax Planning Analysis

    {analysis}

    """
    
    return complete_analysis
# Main Function
def main():
    initialize_session_state()
    render_header()

    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ''
    
    api_key_input = st.text_input("Your Secret Key", type="password", value=st.session_state.openai_api_key)
    if api_key_input:
        st.session_state.openai_api_key = api_key_input
    if not st.session_state.openai_api_key:
        st.info("Please add your Secret key to continue.", icon="🗝️")
        return

    st.write("The SMEBoost Lite GenAI platform is a streamlined, AI-powered version of the full SMEBoost program")

    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0

    # Personal Profile
    with st.container():
        st.write("## Step 1: Personal Profile")
        if st.session_state.current_step == 0:
            personal_profile = render_personal_profile_form()
            if personal_profile:
                st.session_state["personal_profile"] = personal_profile
                st.session_state.current_step = 1
                st.success("Personal profile submitted! Proceed to next step.")
                st.rerun()
        elif "personal_profile" in st.session_state:
            st.success("✓ Personal Profile Completed")

    # Business Profile
    if st.session_state.current_step >= 1:
        with st.container():
            st.write("## Step 2: Profile Analysis")
            if st.session_state.current_step == 1:
                business_profile = render_business_profile_form()
                if business_profile:
                    st.session_state["business_profile"] = business_profile
                    analysis = process_business_profile_with_gpt(business_profile, st.session_state.openai_api_key)
                    st.session_state["business_profile_analysis"] = analysis
                    st.session_state.current_step = 2
                    st.rerun()
            elif "business_profile" in st.session_state:
                st.success("✓ Profile Analysis Completed")
                with st.expander("Click to View Profile Analysis"):
                    st.markdown(st.session_state["business_profile_analysis"])

    # Business Priorities
    if st.session_state.current_step >= 2:
        with st.container():
            st.write("## Step 3: Business Priorities")
            if st.session_state.current_step == 2:
                priorities = render_business_priority_form()
                if priorities:
                    st.session_state["business_priorities"] = priorities
                    analysis = process_business_priorities_with_gpt(priorities, st.session_state.openai_api_key)
                    st.session_state["priorities_analysis"] = analysis
                    st.session_state.current_step = 3
                    st.rerun()
            elif "business_priorities" in st.session_state:
                st.success("✓ Business Priorities Completed")
                with st.expander("Click to View Business Priorities Analysis"):
                    st.markdown(st.session_state["priorities_analysis"])

    # Business Options
    if st.session_state.current_step >= 3:
        with st.container():
            st.write("## Step 4: Business Options")
            if st.session_state.current_step == 3:
                options = render_business_options(st.session_state["business_priorities"], st.session_state.openai_api_key)
                if options:
                    selected_areas = [opt for opt, selected in options.items() if selected]
                    if selected_areas:
                        st.session_state["business_options"] = selected_areas
                        analyses = {}
                        for option in selected_areas:
                            suggestion = get_specific_suggestions(
                                st.session_state["business_priorities"],
                                option,
                                st.session_state.openai_api_key
                            )
                            analyses[option] = suggestion
                        st.session_state["options_analyses"] = analyses
                        st.session_state["executive_summary"] = get_business_option_summary(
                            selected_areas,
                            st.session_state.user_data,
                            st.session_state.openai_api_key
                        )
                        st.session_state.current_step = 4
                        st.rerun()
            elif "business_options" in st.session_state:
                st.success("✓ Business Options Completed")
                with st.expander("Click to View Business Options Analysis"):
                    st.markdown(st.session_state["executive_summary"])
                    for option, analysis in st.session_state["options_analyses"].items():
                        st.subheader(option)
                        st.markdown(analysis)

    # Working Capital
    if st.session_state.current_step >= 4:
        with st.container():
            st.write("## Step 5: Working Capital")
            if st.session_state.current_step == 4:
                capital = render_working_capital_form()
                if capital:
                    st.session_state["working_capital"] = capital
                    analysis = process_working_capital_with_gpt(capital, st.session_state.openai_api_key)
                    st.session_state["capital_analysis"] = analysis
                    st.session_state.current_step = 5
                    st.rerun()
            elif "working_capital" in st.session_state:
                st.success("✓ Working Capital Completed")
                with st.expander("Click to View Working Capital Analysis"):
                    st.markdown(st.session_state["capital_analysis"])

    # Strategic Planning
    if st.session_state.current_step >= 5:
        with st.container():
            st.write("## Step 6: Strategic Planning")
            if st.session_state.current_step == 5:
                planning = render_strategic_planning_form()
                if planning:
                    st.session_state["strategic_planning"] = planning
                    analysis = process_strategic_planning_with_gpt(planning, st.session_state.openai_api_key)
                    st.session_state["strategic_analysis"] = analysis
                    st.session_state.current_step = 6
                    st.rerun()
            elif "strategic_planning" in st.session_state:
                st.success("✓ Strategic Planning Completed")
                with st.expander("Click to View Strategic Planning Analysis"):
                    st.markdown(st.session_state["strategic_analysis"])

    # Growth Projections
    if st.session_state.current_step >= 6:
        with st.container():
            st.write("## Step 7: Growth Projections")
            if st.session_state.current_step == 6:
                projections = render_financial_projections_form()
                if projections:
                    st.session_state["growth_projections"] = projections
                    company_data = {
                        "business_profile": st.session_state["business_profile"],
                        "business_priorities": st.session_state["business_priorities"],
                        "business_options": st.session_state["business_options"],
                        "working_capital": st.session_state["working_capital"],
                        "strategic_planning": st.session_state["strategic_planning"]
                    }
                    analysis = process_financial_projections_with_gpt(projections, company_data, st.session_state.openai_api_key)
                    analysis2 = process_financial_projections_with_gpt2(projections, company_data, st.session_state.openai_api_key)
                    st.session_state["financial_projections"] = analysis + "\n\n" + analysis2
                    st.session_state.current_step = 7
                    st.rerun()
            elif "growth_projections" in st.session_state:
                st.success("✓ Growth Projections Completed")
                with st.expander("Click to View Financial Projections"):
                    st.markdown(st.session_state["financial_projections"])

    # Taxation Module
    if st.session_state.current_step >= 7:
        with st.container():
            st.write("## Step 8: Taxation Planning")
            if st.session_state.current_step == 7:
                taxation = render_taxation_module_form()
                if taxation:
                    st.session_state["taxation_module"] = taxation
                    
                    # Enhanced business context with financial and strategic analyses
                    business_context = {
                        "profile": st.session_state.get("business_profile", {}),
                        "priorities": st.session_state.get("business_priorities", {}),
                        "priorities_analysis": st.session_state.get("priorities_analysis", ""),
                        "options": st.session_state.get("business_options", []),
                        "capital": st.session_state.get("working_capital", {}),
                        "capital_analysis": st.session_state.get("capital_analysis", ""),
                        "strategic": st.session_state.get("strategic_planning", {}),
                        "strategic_analysis": st.session_state.get("strategic_analysis", ""),
                        "growth": st.session_state.get("growth_projections", {}),
                        "financial_projections": st.session_state.get("financial_projections", ""),
                        "profile_analysis": st.session_state.get("business_profile_analysis", ""),
                        "executive_summary": st.session_state.get("executive_summary", "")
                    }
                    
                    # Process each module with full context
                    st.session_state["strategic_tax"] = process_strategic_tax_planning(
                        taxation["strategic_tax_planning"], 
                        business_context,
                        st.session_state.openai_api_key
                    )
                    
                    st.session_state["tactical_tax"] = process_tactical_tax_planning(
                        taxation["tactical_tax_planning"], 
                        business_context,
                        st.session_state.openai_api_key
                    )
                    
                    st.session_state["compliance_tax"] = process_compliance_tax_planning(
                        taxation["compliance_tax_planning"], 
                        business_context,
                        st.session_state.openai_api_key
                    )
                    
                    st.session_state["investment_tax"] = process_investment_tax_planning(
                        taxation["investment_tax_planning"], 
                        business_context,
                        st.session_state.openai_api_key
                    )
                    
                    st.session_state["deductions_tax"] = process_deductions_exemptions(
                        taxation["deductions_exemptions"], 
                        business_context,
                        st.session_state.openai_api_key
                    )
                    
                    st.session_state["income_tax"] = process_income_structuring(
                        taxation["income_structuring"], 
                        business_context,
                        st.session_state.openai_api_key
                    )
                    
                    st.session_state["incentives_tax"] = process_tax_incentives(
                        taxation["tax_incentives"], 
                        business_context,
                        st.session_state.openai_api_key
                    )
                    
                    st.session_state["global_tax"] = process_global_tax_planning(
                        taxation["global_tax_planning"], 
                        business_context,
                        st.session_state.openai_api_key
                    )
                    
                    st.session_state["deferral_tax"] = process_deferral_strategies(
                        taxation["deferral_strategies"], 
                        business_context,
                        st.session_state.openai_api_key
                    )
                    
                    st.session_state["estate_tax"] = process_estate_succession_planning(
                        taxation["estate_planning"], 
                        business_context,
                        st.session_state.openai_api_key
                    )
                    
                    st.session_state.current_step = 8
                    st.rerun()
                    
            elif "taxation_module" in st.session_state:
                st.success("✓ Taxation Planning Completed")
                
                # Display each analysis with full context
                with st.expander("Strategic Tax Planning Analysis", expanded=True):
                    st.markdown(st.session_state["strategic_tax"])
                    
                with st.expander("Tactical Tax Planning Analysis"):
                    st.markdown(st.session_state["tactical_tax"])
                    
                with st.expander("Tax Compliance Analysis"):
                    st.markdown(st.session_state["compliance_tax"])
                    
                with st.expander("Investment Tax Planning Analysis"):
                    st.markdown(st.session_state["investment_tax"])
                    
                with st.expander("Deductions and Exemptions Analysis"):
                    st.markdown(st.session_state["deductions_tax"])
                    
                with st.expander("Income Structuring Analysis"):
                    st.markdown(st.session_state["income_tax"])
                    
                with st.expander("Tax Incentives Analysis"):
                    st.markdown(st.session_state["incentives_tax"])
                    
                with st.expander("Global Tax Planning Analysis"):
                    st.markdown(st.session_state["global_tax"])
                    
                with st.expander("Deferral Strategies Analysis"):
                    st.markdown(st.session_state["deferral_tax"])
                    
                with st.expander("Estate and Succession Planning Analysis"):
                    st.markdown(st.session_state["estate_tax"])

    # Final Report Generation
    if st.session_state.current_step == 8:
        st.write("## Review and Edit")
        
        sections = {
            "Personal Profile": {
                "key": "personal_profile",
                "display_fields": [
                    ("Full Name", "full_name"),
                    ("Email", "email"),
                    ("Phone", "phone")
                ]
            },
            "Business Profile": {
                "key": "business_profile",
                "display_fields": [
                    ("Company Name", "company_name"),
                    ("Industry", "industry"),
                    ("Business Model", "business_model"),
                    ("Products/Services", "products_services"),
                    ("Incorporation Status", "incorporation_status"),
                    ("Primary Currency", "primary_currency"),
                    ("Revenue Size", "revenue_size"),
                    ("Profit Range", "profit_range"),
                    ("Operating Cashflow", "operating_cashflow"),
                    ("Debt/Equity Ratio", "debt_equity_ratio"),
                    ("Shareholders Funds", "shareholders_funds"),
                    ("Staff Strength", "staff_strength"),
                    ("Customer Type", "customer_type")
                ]
            },
            "Business Priorities": {
                "key": "business_priorities",
                "display_fields": [("Business Priorities", "business_priorities")]
            },
            "Business Options": {
                "key": "business_options",
                "is_list": True
            },
            "Working Capital": {
                "key": "working_capital",
                "display_fields": [
                    ("Funding Amount", "funding_amount"),
                    ("Funding Types", "funding_types"),
                    ("Other Funding Type", "other_funding_type"),
                    ("Funding Purposes", "funding_purposes"),
                    ("Other Purpose", "other_purpose")
                ]
            },
            "Strategic Planning": {
                "key": "strategic_planning",
                "is_dict": True
            },
            "Growth Projections": {
                "key": "growth_projections",
                "display_fields": [("Growth Rate", "growth_rate")]
            },
            "Taxation Planning": {
                "key": "taxation_module",
                "is_dict": True
            }
        }

        analysis_keys = {
            "business_profile": "business_profile_analysis",
            "business_priorities": "priorities_analysis",
            "working_capital": "capital_analysis",
            "strategic_planning": "strategic_analysis",
            "growth_projections": "financial_projections",
            "taxation_module": "taxation_analysis"
        }

        for title, config in sections.items():
            key = config["key"]
            if key in st.session_state:
                with st.expander(f"Review {title}", expanded=True):
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        if st.button(f"📝 Edit {title}", key=f"edit_{key}"):
                            st.session_state.current_step = list(sections.keys()).index(title)
                            st.rerun()
                    
                    with col2:
                        st.markdown(f"### {title} Data")
                        if config.get("is_list", False):
                            for item in st.session_state[key]:
                                st.write(f"- {item}")
                        elif config.get("is_dict", False):
                            if key == "taxation_module":
                                for section, data in st.session_state[key].items():
                                    st.markdown(f"**{section.replace('_', ' ').title()}:**")
                                    for q, a in data.items():
                                        st.write(f"- {q.replace('_', ' ').title()}: {a}")
                            else:
                                for q, responses in st.session_state[key].items():
                                    st.markdown(f"**{q}**")
                                    if isinstance(responses, list):
                                        for resp in responses:
                                            st.write(f"- {resp}")
                                    else:
                                        st.write(responses)
                        else:
                            data = st.session_state[key]
                            for label, field in config.get("display_fields", []):
                                if isinstance(data, dict) and field in data:
                                    value = data[field]
                                    if isinstance(value, dict):
                                        st.markdown(f"**{label}:**")
                                        for k, v in value.items():
                                            if v:
                                                if k == "Others please specify" and data.get("other_purpose"):
                                                    st.write(f"- Others: {data['other_purpose']}")
                                                elif k == "Others please specify" and data.get("other_funding_type"):
                                                    st.write(f"- Others: {data['other_funding_type']}")
                                                else:
                                                    st.write(f"- {k}")
                                    else:
                                        if field == "industry" and value == "Others please specify":
                                            st.markdown(f"**{label}:** {data.get('other_industry_details', 'N/A')}")
                                        elif field == "incorporation_status" and value == "Others":
                                            st.markdown(f"**{label}:** {data.get('other_incorporation_details', 'N/A')}")
                                        else:
                                            st.markdown(f"**{label}:** {value}")
                                else:
                                    st.markdown(f"**{label}:** {data}")
                    
                    if key in analysis_keys and analysis_keys[key] in st.session_state:
                        st.markdown("### Analysis")
                        st.markdown(st.session_state[analysis_keys[key]])
                    elif key == "business_options" and "executive_summary" in st.session_state:
                        st.markdown("### Analysis")
                        st.markdown(st.session_state["executive_summary"])
                        if "options_analyses" in st.session_state:
                            for option, analysis in st.session_state["options_analyses"].items():
                                st.subheader(option)
                                st.markdown(analysis)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.write("## Generate Final Report")
            
            # Generate PDF Report button
            if st.button("📄 Generate Complete Reports", type="primary"):
                try:
                    with st.spinner("Generating PDF reports..."):
                        # Main business analysis data
                        sme_data = {
                            'business_profile_analysis': st.session_state['business_profile_analysis'],
                            'priorities_analysis': st.session_state['priorities_analysis'],
                            'executive_summary': st.session_state['executive_summary'],
                            'capital_analysis': st.session_state['capital_analysis'],
                            'strategic_analysis': st.session_state['strategic_analysis'],
                            'financial_projections': st.session_state['financial_projections']
                        }
                        
                        # Tax analysis data
                        tax_data = {
                            'strategic_tax': st.session_state['strategic_tax'],
                            'tactical_tax': st.session_state['tactical_tax'],
                            'compliance_tax': st.session_state['compliance_tax'],
                            'investment_tax': st.session_state['investment_tax'],
                            'deductions_tax': st.session_state['deductions_tax'],
                            'income_tax': st.session_state['income_tax'],
                            'incentives_tax': st.session_state['incentives_tax'],
                            'global_tax': st.session_state['global_tax'],
                            'deferral_tax': st.session_state['deferral_tax'],
                            'estate_tax': st.session_state['estate_tax']
                        }
                        
                        personal_info = st.session_state["personal_profile"].copy()
                        personal_info['company_name'] = st.session_state['business_profile']['company_name']
                        
                        # Generate both PDFs
                        main_pdf_buffer = generate_main_pdf(sme_data, personal_info, [4, 8, 11, 14, 17, 20])
                        tax_pdf_buffer = generate_tax_pdf(tax_data, personal_info, [4, 7, 10, 13, 16, 19, 22, 25, 28, 31])
                        
                        if main_pdf_buffer and tax_pdf_buffer:
                            st.success("PDF reports generated successfully!")
                            
                            # Download buttons for both PDFs
                            st.download_button(
                                "📥 Download Business Analysis Report",
                                data=main_pdf_buffer,
                                file_name=f"business_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf"
                            )
                            
                            st.download_button(
                                "📥 Download Tax Analysis Report",
                                data=tax_pdf_buffer,
                                file_name=f"tax_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf"
                            )
                            
                            # Excel Download button
                            excel_buffer = generate_excel_report(st.session_state)
                            st.download_button(
                                "📊 Download Input Data (Excel)",
                                data=excel_buffer,
                                file_name=f"sme_analysis_input_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                                mime="application/vnd.ms-excel"
                            )
                            
                    # Send emails with both PDFs
                    with st.spinner("Sending reports via email..."):
                        analysis_statistics = calculate_analysis_statistics(st.session_state)
                        contact_details = f"""Contact Details:
                    Full Name: {personal_info.get('full_name', 'Not provided')}
                    Email: {personal_info.get('email', 'Not provided')}
                    Mobile: {personal_info.get('phone', 'Not provided')}"""

                        for email in [personal_info['email'], EMAIL_SENDER]:
                            send_combined_email_with_attachments(
                                receiver_email=email,
                                company_name=personal_info['company_name'],
                                subject="SME Analysis Reports and Input Data",
                                body="SME Business and Tax Analysis Reports from SMEBoost Lite GenAI.",
                                pdf_buffer=main_pdf_buffer,  # You'll need to modify the email function to handle multiple PDFs
                                excel_buffer=excel_buffer,
                                statistics=analysis_statistics,
                                contact_details=contact_details,
                                tax_pdf_buffer=tax_pdf_buffer  # New parameter
                            )
                            
                except Exception as e:
                    st.error(f"Error generating reports: {str(e)}")
                    print(f"Detailed error: {str(e)}")

if __name__ == "__main__":
    main()
#16/12/2024
