from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

output_path = "/mnt/data/Acidity_Recovery_Designed_v2.pdf"

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=colors.HexColor("#0E3A5D"),
    spaceAfter=14
)
section_style = ParagraphStyle(
    'SectionStyle',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor("#1F5A85"),
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

# Sections
sections = {
    "Daily Timings": """
• Wake: 9:30–9:45 am<br/>
• Breakfast: 10:30 am<br/>
• Mid-meal: 12:30 pm<br/>
• Lunch: 2:30 pm<br/>
• Snack: 6:00 pm<br/>
• Dinner: 9:30–10:00 pm<br/>
• Sleep: 1:30 am<br/>
• Water: 6–8 glasses/day (warm)<br/>
""",
    "Medicines": """
• Pantoprazole 40 mg – 30 min before breakfast (10 days)<br/>
• Isabgol – 1 tsp in warm water every night<br/>
• Optional: 1 tsp ghee in warm water before bed<br/>
""",
    "7-Day Meal Plan": """
<b>Breakfast:</b> Idli, Oats, Poha, Upma, Egg + Toast<br/>
<b>Mid-meal:</b> Banana, Buttermilk, Curd, Apple, Coconut water, Nuts<br/>
<b>Lunch:</b> Khichdi + Curd OR Chapati + Dal + Sabzi + Curd OR Dal Rice + Curd<br/>
<b>Evening:</b> Fruit, Coconut Water, Roasted Chana<br/>
<b>Dinner:</b> Khichdi, Curd Rice, Soup, 2 Chapatis + Sabzi<br/>
<b>Bedtime:</b> Isabgol<br/>
""",
    "Shopping List": """
Rice, Moong Dal, Oats, Wheat Flour<br/>
Lauki, Carrot, Beans, Spinach, Cucumber, Potatoes, Tomato<br/>
Banana, Apple, Papaya, Melon<br/>
Curd, Buttermilk, Milk<br/>
Jeera, Turmeric, Ghee, Honey, Salt, Isabgol, Eggs<br/>
""",
    "WhatsApp Style Routine": """
• 9:30 am – Wake + Warm Water<br/>
• 10:00 am – Pantoprazole<br/>
• 10:30 am – Breakfast<br/>
• 12:30 pm – Mid-meal<br/>
• 2:30 pm – Lunch<br/>
• 3:00 pm – Jeera Water<br/>
• 6:00 pm – Snack<br/>
• 9:30 pm – Dinner<br/>
• 1:00 am – Isabgol<br/>
• 1:30 am – Sleep<br/>
"""
}

for title, content in sections.items():
    story.append(Paragraph(title, section_style))
    story.append(Paragraph(content, text_style))
    story.append(Spacer(1, 12))

# Symptom Tracker Table
story.append(Paragraph("Symptom Tracker (14 Days)", section_style))
table_data = [["Day", "Burning", "Bloating", "Constipation", "Burps", "Energy"]]
for i in range(1, 15):
    table_data.append([str(i), "", "", "", "", ""])

table = Table(table_data, colWidths=[40, 70, 70, 80, 60, 60])
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#B7D4EA")),
    ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("ALIGN", (0,0), (-1,-1), "CENTER")
]))

story.append(table)

doc = SimpleDocTemplate(output_path, pagesize=letter)
doc.build(story)

output_path
