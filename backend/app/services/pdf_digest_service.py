# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — ReportLab Morning PDF Digest Generator Service

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_morning_pdf_digest(high_ticket_leads=None, doctor_statuses=None) -> bytes:
    """Generates an official 08:30 AM Morning Reception Digest PDF document."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor('#059669'),
        spaceAfter=12
    )

    heading2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#334155'),
        leading=12
    )

    elements = []

    # Title & Header
    elements.append(Paragraph("APEX DENTAL CLINIC — CONCIERGE DIGEST", title_style))
    elements.append(Paragraph(f"☀️ 08:30 AM Morning Shift Dispatch — Date: {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#10B981'), spaceAfter=12))

    # Section 1: Priority High-Ticket Morning Callbacks
    elements.append(Paragraph("⚡ Priority High-Ticket Morning Callbacks (> ₹3,500)", heading2_style))

    if not high_ticket_leads:
        high_ticket_leads = [
            {"id": "HT-9821", "patient_name": "Rahul Kumar", "patient_phone": "+919876543210", "service_name": "Invisible Aligners", "estimated_value": 45000.0, "requested_slot": "10:00 AM IST"},
            {"id": "HT-9822", "patient_name": "Priya Sharma", "patient_phone": "+919876543211", "service_name": "Microscopic RCT", "estimated_value": 6500.0, "requested_slot": "11:30 AM IST"},
            {"id": "HT-9823", "patient_name": "Vikram Sen", "patient_phone": "+919876543212", "service_name": "Teeth-in-a-Day Implant", "estimated_value": 85000.0, "requested_slot": "02:00 PM IST"},
        ]

    lead_table_data = [["Lead ID", "Patient Name", "Phone", "Procedure", "Slot", "Est. Value"]]
    total_val = 0.0
    for lead in high_ticket_leads:
        val = lead.get("estimated_value", 0.0)
        total_val += val
        lead_table_data.append([
            lead.get("id", "HT-XXXX"),
            lead.get("patient_name", "N/A"),
            lead.get("patient_phone", "N/A"),
            lead.get("service_name", "N/A"),
            lead.get("requested_slot", "N/A"),
            f"₹{val:,.2f}"
        ])

    lead_table = Table(lead_table_data, colWidths=[65, 100, 95, 130, 80, 70])
    lead_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
    ]))
    elements.append(lead_table)
    elements.append(Spacer(1, 10))

    # Section 2: Doctor Status & Surgery Schedule
    elements.append(Paragraph("👨‍⚕️ Doctor Duty Roster & Live Status", heading2_style))

    if not doctor_statuses:
        doctor_statuses = [
            {"doctor_name": "Dr. Chinmay Hudedamani", "current_status": "AVAILABLE", "est_completion_mins": 0},
            {"doctor_name": "Dr. Ananya Rao", "current_status": "IN_SURGERY", "est_completion_mins": 45},
            {"doctor_name": "Dr. Vikramaditya Hegde", "current_status": "ON_BREAK", "est_completion_mins": 15},
        ]

    doc_table_data = [["Doctor Name", "Current Status", "Est. Completion (Mins)"]]
    for doc_item in doctor_statuses:
        doc_table_data.append([
            doc_item.get("doctor_name", "N/A"),
            doc_item.get("current_status", "AVAILABLE"),
            f"{doc_item.get('est_completion_mins', 0)} mins"
        ])

    doc_table = Table(doc_table_data, colWidths=[200, 160, 180])
    doc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
    ]))
    elements.append(doc_table)
    elements.append(Spacer(1, 12))

    # Section 3: Daily High-Ticket Pipeline Summary
    elements.append(Paragraph("📈 Expected High-Ticket Pipeline Summary", heading2_style))
    summary_text = f"<b>Total High-Ticket Lead Pipeline:</b> ₹{total_val:,.2f} across {len(high_ticket_leads)} priority callbacks.<br/>" \
                   f"<b>Target Conversion Rate:</b> 85% expected lock-in during morning call dispatch."
    elements.append(Paragraph(summary_text, body_style))
    elements.append(Spacer(1, 14))

    # Footer Notice
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=8))
    elements.append(Paragraph("Generated by Copus AI Concierge Engine · Confidential Receptionist Report", ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#64748B'), alignment=1)))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
