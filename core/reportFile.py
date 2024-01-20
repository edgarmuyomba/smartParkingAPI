from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from io import BytesIO


class ReportFile:
    def __init__(self, type, data):
        self.type = type
        self.data = data
        self.buffer = BytesIO()

    def get_report_file(self):
        report_file_map = {
            # "occupancy_trends": self.get_occupancy_trends(),
            "revenue_analysis": self.get_revenue_analysis(),
            # "time_analysis": self.get_time_analysis(),
            # "usage_patterns": self.get_usage_patterns(),
            # "peak_usage_hours": self.get_peak_usage_hours(),
            # "session_duration": self.get_session_duration(),
            # "session_distribution": self.get_session_distribution(),
            # "user_activity": self.get_user_activity(),
        }
        return report_file_map[self.type]

    def get_occupancy_trends(self):
        doc = SimpleDocTemplate(self.buffer, pagesize=letter)

        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(
            'Header1', parent=styles['Heading1'], fontSize=18)

        content = []
        content.append(Paragraph("Occupancy Trends Report", header_style))
        content.append(Paragraph(self.data["date"], styles["BodyText"]))
        content.append(Paragraph(
            f"Overall Percentage: {self.data['overall_percentage']}%", styles["BodyText"]))
        content.append(Paragraph(
            f"Overall Occupancy: {self.data['overall_occupancy']}", styles["BodyText"]))
        content.append(Spacer(1, 12))

        table_data = [["Parking Lot", "Percentage Occupancy", "Occupancy"]]
        for lot in self.data["parking_lot_details"]:
            table_data.append(
                [lot["name"], f"{lot['percentage_occupancy']}%", lot["occupancy"]])

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('LEADING', (0, 0), (-1, -1), 15),
        ])

        lot_table = Table(table_data, colWidths=[doc.width / 3.0] * 3)
        lot_table.setStyle(table_style)

        content.append(lot_table)

        doc.build(content)

        self.buffer.seek(0)

        return self.buffer

    def get_revenue_analysis(self):
        doc = SimpleDocTemplate(self.buffer, pagesize=letter)

        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(
            'Header1', parent=styles['Heading1'], fontSize=18)

        content = []
        content.append(Paragraph("Revenue Analysis Report", header_style))
        content.append(Paragraph(self.data["date"], styles["BodyText"]))
        content.append(Paragraph(
            f"Total Expected Income: UGX {self.data['total_expected_income']}", styles["BodyText"]))
        content.append(
            Paragraph(f"Session Count: {self.data['session_count']}", styles["BodyText"]))
        content.append(Spacer(1, 12))

        table_data = [["Parking Lot", "Expected Income"]]
        for lot in self.data["parking_lot_details"]:
            table_data.append([lot["name"], f"UGX {lot['expected_income']}"])

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('LEADING', (0, 0), (-1, -1), 15),
        ])

        # Adjust colWidths as needed
        lot_table = Table(table_data, colWidths=[doc.width / 2.0] * 2)
        lot_table.setStyle(table_style)

        content.append(lot_table)

        doc.build(content)

        self.buffer.seek(0)

        return self.buffer
