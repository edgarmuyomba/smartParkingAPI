from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

import csv
from io import BytesIO, StringIO

class ReportFile:
    def __init__(self, type, data):
        self.type = type
        self.data = data
        self.pdf_buffer = BytesIO()
        self.csv_buffer = StringIO()

    def get_report_file(self):
        report_file_map = {
            "occupancy_trends": self.get_occupancy_trends,
            "revenue_analysis": self.get_revenue_analysis,
            "time_analysis": self.get_time_analysis,
            "usage_patterns": self.get_usage_patterns,
            "peak_usage_hours": self.get_peak_usage_hours,
            "session_duration": self.get_session_duration,
            "session_distribution": self.get_session_distribution,
            "user_activity": self.get_user_activity,
        }
        
        report_function = report_file_map.get(self.type)
        return report_function()

    def get_occupancy_trends(self):
        doc = SimpleDocTemplate(self.pdf_buffer, pagesize=letter)

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

        self.pdf_buffer.seek(0)

        return self.pdf_buffer, "Occupancy Trends Report.pdf", 'application/pdf'

    def get_revenue_analysis(self):
        doc = SimpleDocTemplate(self.pdf_buffer, pagesize=letter)

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

        self.pdf_buffer.seek(0)

        return self.pdf_buffer, "Revenue Analysis Report.pdf", 'application/pdf'

    def get_time_analysis(self):
        doc = SimpleDocTemplate(self.pdf_buffer, pagesize=letter)

        styles = getSampleStyleSheet()
        header_style = ParagraphStyle('Header1', parent=styles['Heading1'], fontSize=18)

        content = []
        content.append(Paragraph("Time Analysis Report", header_style))
        content.append(Paragraph(self.data["date"], styles["BodyText"]))
        content.append(Paragraph(f"Average Session Duration: {self.data['average_session_duration']} hours", styles["BodyText"]))
        content.append(Spacer(1, 12))

        table_data = [["Time", "Count"]]
        for peak_hour in self.data["peak_hours"]:
            table_data.append([peak_hour["time"], f"{peak_hour['count']} Sessions"])

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

        peak_hours_table = Table(table_data, colWidths=[doc.width / 2.0] * 2) 
        peak_hours_table.setStyle(table_style)

        content.append(peak_hours_table)

        doc.build(content)

        self.pdf_buffer.seek(0)

        return self.pdf_buffer, "Time Analysis Report.pdf", 'application/pdf'
    
    def get_usage_patterns(self):
        csv_writer = csv.writer(self.csv_buffer)

        csv_writer.writerow(["Session ID", "User ID", "Start Time"])

        for session in self.data:
            csv_writer.writerow([session["session_id"], session["user_id"], session["start_time"]])

        self.csv_buffer.seek(0)

        return self.csv_buffer.getvalue().encode('utf-8'), "Usage Patterns Report.csv", 'text/csv'
    
    def get_peak_usage_hours(self):
        csv_writer = csv.writer(self.csv_buffer)

        csv_writer.writerow(["Hour", "Count", "Average Duration (Hours)"])

        for hour in self.data:
            csv_writer.writerow([hour["hour"], hour["count"], hour["average_duration"]])

        self.csv_buffer.seek(0)

        return self.csv_buffer.getvalue().encode('utf-8'), "Peak Usage Hours Report.csv", 'text/csv'
    
    def get_session_duration(self):
        csv_writer = csv.writer(self.csv_buffer)

        csv_writer.writerow(["Session ID", "Duration (Hours)"])

        for session in self.data:
            csv_writer.writerow([session["session_id"], session["duration"]])

        self.csv_buffer.seek(0)

        return self.csv_buffer.getvalue().encode('utf-8'), "Session Duration Report.csv", 'text/csv'
    
    def get_session_distribution(self):
        csv_writer = csv.writer(self.csv_buffer)

        csv_writer.writerow(["Date", "Count (Sessions)", "Busiest Location"])

        for session in self.data:
            csv_writer.writerow([session["date"], session["count"], session["busiest_location"]])

        self.csv_buffer.seek(0)

        return self.csv_buffer.getvalue().encode('utf-8'), "Session Distribution Report.csv", 'text/csv'
    
    def get_user_activity(self):
        doc = SimpleDocTemplate(self.pdf_buffer, pagesize=letter, leftMargin=30)

        styles = getSampleStyleSheet()
        header_style = ParagraphStyle('Header1', parent=styles['Heading1'], fontSize=18)

        content = []
        content.append(Paragraph("User Activity Report", header_style))
        content.append(Paragraph(self.data["date"], styles["BodyText"]))
        content.append(Spacer(1, 12))

        for user in self.data["users"]:
            user_id_style = ParagraphStyle('User_ID', parent=styles['Heading2'], fontSize=12) 
            content.append(Paragraph(f"User ID: {user['user_id']}", user_id_style))
            if user["sessions"]:
                sessions_table_data = [["Sessions"]]
                for session in user["sessions"]:
                    sessions_table_data.append([session])

                sessions_table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('LEADING', (0, 0), (-1, -1), 15),
                ])

                sessions_table = Table(sessions_table_data, colWidths=[doc.width / 2.0])  
                sessions_table.setStyle(sessions_table_style)

                content.append(sessions_table)
            else:
                content.append(Paragraph("No sessions for this user.", styles["BodyText"]))

            content.append(Spacer(1, 12))

        doc.build(content)

        self.pdf_buffer.seek(0)

        return self.pdf_buffer, "User Activity Report.pdf", "application/pdf"