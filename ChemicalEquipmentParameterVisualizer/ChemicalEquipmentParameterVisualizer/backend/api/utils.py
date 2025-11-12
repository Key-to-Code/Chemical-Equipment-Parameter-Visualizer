import pandas as pd
import io
from .models import Dataset

def process_csv_data(csv_content, filename):
    df = pd.read_csv(io.StringIO(csv_content))
    
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV must contain columns: {', '.join(required_columns)}")
    
    total_count = len(df)
    avg_flowrate = df['Flowrate'].mean()
    avg_pressure = df['Pressure'].mean()
    avg_temperature = df['Temperature'].mean()
    
    type_distribution = df['Type'].value_counts().to_dict()
    
    dataset = Dataset.objects.create(
        name=filename,
        csv_file=csv_content,
        total_count=total_count,
        avg_flowrate=round(avg_flowrate, 2),
        avg_pressure=round(avg_pressure, 2),
        avg_temperature=round(avg_temperature, 2)
    )
    dataset.set_type_distribution(type_distribution)
    dataset.save()
    
    cleanup_old_datasets()
    
    return dataset

def cleanup_old_datasets():
    datasets = Dataset.objects.all().order_by('-uploaded_at')
    if datasets.count() > 5:
        old_datasets = datasets[5:]
        for ds in old_datasets:
            ds.delete()

def generate_pdf_report(dataset):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch
    import io
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    title = Paragraph(f"<b>Equipment Data Report: {dataset.name}</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    uploaded_date = Paragraph(f"<b>Uploaded:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    elements.append(uploaded_date)
    elements.append(Spacer(1, 0.2*inch))
    
    summary_title = Paragraph("<b>Summary Statistics</b>", styles['Heading2'])
    elements.append(summary_title)
    elements.append(Spacer(1, 0.1*inch))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(dataset.total_count)],
        ['Average Flowrate', f"{dataset.avg_flowrate:.2f}"],
        ['Average Pressure', f"{dataset.avg_pressure:.2f}"],
        ['Average Temperature', f"{dataset.avg_temperature:.2f}"]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    type_dist_title = Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2'])
    elements.append(type_dist_title)
    elements.append(Spacer(1, 0.1*inch))
    
    type_dist = dataset.get_type_distribution()
    type_data = [['Equipment Type', 'Count']]
    for eq_type, count in type_dist.items():
        type_data.append([eq_type, str(count)])
    
    type_table = Table(type_data, colWidths=[3*inch, 2*inch])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(type_table)
    elements.append(Spacer(1, 0.3*inch))
    
    equipment_title = Paragraph("<b>Equipment Details</b>", styles['Heading2'])
    elements.append(equipment_title)
    elements.append(Spacer(1, 0.1*inch))
    
    import csv
    lines = dataset.csv_file.strip().split('\n')
    reader = csv.DictReader(lines)
    equipment_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
    for row in reader:
        equipment_data.append([
            row['Equipment Name'],
            row['Type'],
            row['Flowrate'],
            row['Pressure'],
            row['Temperature']
        ])
    
    equipment_table = Table(equipment_data, colWidths=[1.5*inch, 1.3*inch, 1*inch, 1*inch, 0.8*inch])
    equipment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(equipment_table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
