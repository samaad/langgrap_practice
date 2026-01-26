from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

output_path = "/Users/imshoaib/Acidity_Recovery_Designed.pdf"

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=colors.HexColor("#1F4E79"),
    spaceAfter=14
)
section_style = ParagraphStyle(
    'SectionStyle',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor("#38598B"),
    spaceAfter=10
)
text_style = ParagraphStyle(
    'TextStyle',
    parent=styles['BodyText'],
    fontSize=11,
    leading=16
)

story = []

story.append(Paragraph("14-DAY ACIDITY & BLOATING RECOVERY PLAN", title_style))
story.append(Spacer(1, 12))

# Section 1
story.append(Paragraph("Daily Timings", section_style))
timings = """
• Wake: 9:30–9:45 am<br/>
• Breakfast: 10:30 am<br/>
• Mid-meal: 12:30 pm<br/>
• Lunch: 2:30 pm<br/>
• Snack: 6:00 pm<br/>
• Dinner: 9:30–10:00 pm<br/>
• Sleep: 1:30 am<br/>
• Water: 6–8 glasses/day (warm)<br/>
"""
story.append(Paragraph(timings, text_style))
story.append(Spacer(1, 12))

# Section 2
story.append(Paragraph("Medicines", section_style))
meds = """
• Pantoprazole 40 mg – every morning, 30 min before breakfast (10 days)<br/>
• Isabgol – 1 tsp in warm water every night<br/>
• Optional: 1 tsp ghee in warm water before bed<br/>
"""
story.append(Paragraph(meds, text_style))
story.append(Spacer(1, 12))

# Section 3
story.append(Paragraph("7-Day Meal Plan", section_style))
meals = """
<b>Breakfast:</b> Idli, Oats, Poha, Upma, Egg + Toast<br/>
<b>Mid-meal:</b> Banana, Buttermilk, Curd, Apple, Coconut water, Nuts<br/>
<b>Lunch:</b> Khichdi + Curd OR Chapati + Dal + Sabzi + Curd OR Dal Rice + Curd<br/>
<b>Evening:</b> Fruit, Coconut Water, Roasted Chana<br/>
<b>Dinner:</b> Khichdi, Curd Rice, Soup, 2 Chapatis + Sabzi<br/>
<b>Bedtime:</b> Isabgol<br/>
"""
story.append(Paragraph(meals, text_style))
story.append(Spacer(1, 12))

# Section 4
story.append(Paragraph("Shopping List", section_style))
shopping = """
Rice, Moong Dal, Oats, Wheat Flour<br/>
Lauki, Carrot, Beans, Spinach, Cucumber, Potatoes, Tomato<br/>
Banana, Apple, Papaya, Melon<br/>
Curd, Buttermilk, Milk<br/>
Jeera, Turmeric, Ghee, Honey, Salt, Isabgol, Eggs<br/>
"""
story.append(Paragraph(shopping, text_style))
story.append(Spacer(1, 12))

# Section 5
story.append(Paragraph("WhatsApp Style Routine", section_style))
routine = """
• 9:30 am – Wake + warm water<br/>
• 10:00 am – Pantoprazole<br/>
• 10:30 am – Breakfast<br/>
• 12:30 pm – Mid-meal<br/>
• 2:30 pm – Lunch<br/>
• 3:00 pm – Jeera water<br/>
• 6:00 pm – Snack<br/>
• 9:30 pm – Dinner<br/>
• 1:00 am – Isabgol<br/>
• 1:30 am – Sleep<br/>
"""
story.append(Paragraph(routine, text_style))
story.append(Spacer(1, 12))

# Symptom Tracker Table
story.append(Paragraph("Symptom Tracker (14 Days)", section_style))

table_data = [["Day", "Burning", "Bloating", "Constipation", "Burps", "Energy"]]
for i in range(1, 15):
    table_data.append([str(i), "", "", "", "", ""])

table = Table(table_data, colWidths=[40, 70, 70, 80, 60, 60])
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#D9E1F2")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.black),
    ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("ALIGN", (0,0), (-1,-1), "CENTER")
]))

story.append(table)

doc = SimpleDocTemplate(output_path, pagesize=letter)
doc.build(story)

output_path
