import os
from asem_talent.services.resume_parser import parse_resume_document

pdf_path = r"C:\Users\ongkh\AppData\Local\Temp\asem_ocr_resume.pdf"

with open(pdf_path, "rb") as f:
    content_bytes = f.read()

try:
    response = parse_resume_document(
        file_name="asem_ocr_resume.pdf",
        content_type="application/pdf",
        content_bytes=content_bytes
    )
    
    print("\n--- OCR Smoke Test Results ---")
    print(f"Extracted Name: {response.profile.full_name}")
    print(f"Extracted Email: {response.profile.email}")
    print(f"Preview Text: {response.preview[:500]}...")
    
    # Check for success
    text_found = "John Imageonly" in response.preview
    email_redacted = "****" in response.preview and "john.image@example.com" not in response.preview
    phone_redacted = "****" in response.preview and "+60 12-888 9999" not in response.preview
    
    # Check for keywords (case insensitive usually)
    preview_lower = response.preview.lower()
    python_detected = "python" in preview_lower
    debugging_detected = "debugging" in preview_lower
    
    print(f"OCR Extracted Text Successfully: {text_found}")
    print(f"Email/Phone Redacted in Preview: {email_redacted or phone_redacted}")
    print(f"Python Detected: {python_detected}")
    print(f"Debugging Detected: {debugging_detected}")

except Exception as e:
    print(f"Error during parsing: {e}")
    import traceback
    traceback.print_exc()
