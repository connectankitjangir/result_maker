import fitz  # PyMuPDF
import os
import csv
import time

start_time = time.time()
title_texts_lists = ["Roll", "NAME", "FATHERNAME", "MOTHERNAME", "DOB", "CAT1", "CAT2", "CAT3"]
# pdf_path = "jso_part_.pdf"
# csv_path = "jso_part_1.csv"

def pdf_to_csv(pdf_path, csv_path):
    pdf_file = fitz.open(pdf_path)

    original_rows_per_page = 51
    additional_row = 0

    data = []  # List to store row data

    for page_number in range(pdf_file.page_count):
        ignor_heading = 0
        if page_number != 0:
            ignor_heading = 11.9
            additional_row = -1
        
        coloum_widths = []        
        page = pdf_file[page_number]
        condition_met = False
        text_occurance_Record = page.search_for("Record#")
        if text_occurance_Record:
            y_coordinate_record = text_occurance_Record[0][1]
        else:
            continue

        for title_text_list in title_texts_lists:
            text_occurances_in_loop = page.search_for(title_text_list)
            for text_occurance_in_loop in text_occurances_in_loop:
                if y_coordinate_record < text_occurance_in_loop[3]:
                    coloum_widths.append(text_occurance_in_loop[0])
                    condition_met = True
                    break  
            if not condition_met:
                continue  
        coloum_widths.append(page.rect.width)
        coloum_widths.insert(0,0)
        
        for row_number in range(original_rows_per_page + int(additional_row)):
            row_data = []
            total_coloum = len(coloum_widths)
            coloum_index = 1
            while coloum_index < total_coloum:
                x0 = coloum_widths[coloum_index-1]
                x1 = coloum_widths[coloum_index]
                y0 = y_coordinate_record + 11.9 * row_number + ignor_heading
                y1 = y0 + 11.9
                cell_text = page.get_text("text", clip=(x0, y0, x1, y1))
                row_data.append(cell_text.strip())
                coloum_index += 1
            
            # Check if row_data is completely empty
            if not any(row_data):
                print("Blank row found. Stopping extraction.")
                # Save the data to the .csv file
                with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
                pdf_file.close()
                end_time = time.time()
                print("Total time taken by script in seconds is:", end_time - start_time)
                exit()  # Stop the script
            
            data.append(row_data)  # Add row_data to the list

        print("Process completed till page no.:", str(page_number + 1), "/", str(pdf_file.page_count))

    # Save the remaining data to the .csv file if no blank row was found
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    pdf_file.close()
    end_time = time.time()
    print("Total time taken by script in seconds is:", end_time - start_time)


for i in range(1, 21):
    pdf_to_csv(f"part_{i}.pdf", f"part_{i}.csv")

