import fitz  # PyMuPDF
import os

def split_pdf_into_parts(pdf_path, parts=20):
    pdf_file = fitz.open(pdf_path)
    total_pages = pdf_file.page_count
    pages_per_part = total_pages // parts
    remainder = total_pages % parts

    start_page = 0
    for i in range(parts):
        end_page = start_page + pages_per_part + (1 if i < remainder else 0)
        part_pdf = fitz.open()  # Create a new PDF for the part

        for page_number in range(start_page, end_page):
            part_pdf.insert_pdf(pdf_file, from_page=page_number, to_page=page_number)

        part_pdf_path = f'part_{i + 1}.pdf'  # Save in the same folder
        part_pdf.save(part_pdf_path)
        part_pdf.close()

        start_page = end_page

    pdf_file.close()


pdf_path = "cgl_2024.pdf"
split_pdf_into_parts(pdf_path, parts=20)
