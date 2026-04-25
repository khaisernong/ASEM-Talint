import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_ocr_pdf(output_path):
    # Create an image with text
    img = Image.new('RGB', (800, 1000), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    text_content = [
        "John Imageonly",
        "john.image@example.com",
        "+60 12-888 9999",
        "Projects",
        "Python automation and debugging project",
        "Internship",
        "Automation Intern at Penang E&E SME"
    ]
    
    y = 50
    for line in text_content:
        d.text((50, y), line, fill=(0, 0, 0))
        y += 50
        
    img_path = "temp_resume_img.png"
    img.save(img_path)
    
    # Convert image to PDF
    c = canvas.Canvas(output_path, pagesize=letter)
    c.drawImage(img_path, 0, 0, width=612, height=792)
    c.save()
    
    os.remove(img_path)
    print(f"Generated OCR PDF at {output_path}")

if __name__ == "__main__":
    generate_ocr_pdf(r"C:\Users\ongkh\AppData\Local\Temp\asem_ocr_resume.pdf")
