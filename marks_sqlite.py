import requests
import lxml.etree as etree
import pandas as pd
import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Read data from CSV file
df = pd.read_csv('extra_after_harshit.csv')

# Extract roll number and link from the DataFrame as lists
roll_numbers = df.iloc[:, 1].tolist()  # Assuming roll number is in the 2nd column
links = df.iloc[:, 2].tolist()         # Assuming link is in the 3rd column

# Create SQLite database to store the results
conn = sqlite3.connect('data_calculated.db', check_same_thread=False)
lock = Lock()  # SQLite requires thread safety
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS results (
        roll_number TEXT,
        link TEXT,
        candidate_name TEXT,
        venue_name TEXT,
        exam_date TEXT,
        math_right INTEGER,
        math_not_attempted INTEGER,
        math_right_with_bonus INTEGER,
        math_not_attempted_with_bonus INTEGER,
        reasoning_right INTEGER,
        reasoning_not_attempted INTEGER,
        reasoning_right_with_bonus INTEGER,
        reasoning_not_attempted_with_bonus INTEGER,
        english_right INTEGER,
        english_not_attempted INTEGER,
        english_right_with_bonus INTEGER,
        english_not_attempted_with_bonus INTEGER,
        gk_right INTEGER,
        gk_not_attempted INTEGER,
        gk_right_with_bonus INTEGER,
        gk_not_attempted_with_bonus INTEGER,
        computer_right INTEGER,
        computer_not_attempted INTEGER,
        computer_right_with_bonus INTEGER,
        computer_not_attempted_with_bonus INTEGER
    )
''')
conn.commit()

# Save iteration number in a text file to keep track of the number of candidates processed
if os.path.exists('iteration.txt'):
    with open('iteration.txt', 'r') as f:
        iteration_number = int(f.read())
else:
    iteration_number = 0


def process_candidate(roll_number, link):
    try:
        if not link.startswith(('http://', 'https://')):
            # If link is not valid, write 'ABSENT' in all text fields and leave integers as blank
            with lock:  # Ensure SQLite thread safety
                c.execute('''
                    INSERT INTO results (
                        roll_number, link, candidate_name, venue_name, exam_date,
                        math_right, math_not_attempted, math_right_with_bonus, math_not_attempted_with_bonus,
                        reasoning_right, reasoning_not_attempted, reasoning_right_with_bonus, reasoning_not_attempted_with_bonus,
                        english_right, english_not_attempted, english_right_with_bonus, english_not_attempted_with_bonus,
                        gk_right, gk_not_attempted, gk_right_with_bonus, gk_not_attempted_with_bonus,
                        computer_right, computer_not_attempted, computer_right_with_bonus, computer_not_attempted_with_bonus
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (roll_number, link, 'ABSENT', 'ABSENT', 'ABSENT',
                      None, None, None, None,
                      None, None, None, None,
                      None, None, None, None,
                      None, None, None, None,
                      None, None, None, None))
                conn.commit()
            return

        response = requests.get(link, timeout=10)
        parser = etree.HTMLParser()
        tree = etree.fromstring(response.content, parser)

        tbody = tree.xpath('//tbody')[0]
        candidate_name = tbody.xpath('/html/body/div/div[2]/table/tbody/tr[2]/td[2]')[0].text.strip()
        venue_name = tbody.xpath('/html/body/div/div[2]/table/tbody/tr[3]/td[2]')[0].text.strip()
        exam_date = tbody.xpath('/html/body/div/div[2]/table/tbody/tr[4]/td[2]')[0].text.strip()

        question_panels = tree.xpath('//div[contains(@class, "question-pnl")]')

        wrong_questions_id = [630680674736, 630680262118, 630680617611]

        # Initialize counters for scores
        math_right = math_not_attempted = math_right_with_bonus = math_not_attempted_with_bonus = 0
        reasoning_right = reasoning_not_attempted = reasoning_right_with_bonus = reasoning_not_attempted_with_bonus = 0
        english_right = english_not_attempted = english_right_with_bonus = english_not_attempted_with_bonus = 0
        gk_right = gk_not_attempted = gk_right_with_bonus = gk_not_attempted_with_bonus = 0
        computer_right = computer_not_attempted = computer_right_with_bonus = computer_not_attempted_with_bonus = 0

        for index, question_panel in enumerate(question_panels):
            answer_text = question_panel.xpath('.//td[@class="bold"]')[9].text.strip()
            question_id = int(question_panel.xpath('.//td[@class="bold"]')[3].text.strip())
            correct_answer = question_panel.xpath('.//td[contains(@class, "rightAns")]/text()')[0][0]

            if index < 30:
                if question_id in wrong_questions_id:
                    math_right_with_bonus += 1
                    if correct_answer == answer_text:
                        math_right += 1
                    elif '--' in answer_text:
                        math_not_attempted += 1
                elif '--' in answer_text:
                    math_not_attempted += 1
                    math_not_attempted_with_bonus += 1
                elif correct_answer == answer_text:
                    math_right += 1
                    math_right_with_bonus += 1
            elif index < 60:
                if question_id in wrong_questions_id:
                    reasoning_right_with_bonus += 1
                    if correct_answer == answer_text:
                        reasoning_right += 1
                    elif '--' in answer_text:
                        reasoning_not_attempted += 1
                elif '--' in answer_text:
                    reasoning_not_attempted += 1
                    reasoning_not_attempted_with_bonus += 1
                elif correct_answer == answer_text:
                    reasoning_right += 1
                    reasoning_right_with_bonus += 1
            elif index < 105:
                if question_id in wrong_questions_id:
                    english_right_with_bonus += 1
                    if correct_answer == answer_text:
                        english_right += 1
                    elif '--' in answer_text:
                        english_not_attempted += 1
                elif '--' in answer_text:
                    english_not_attempted += 1
                    english_not_attempted_with_bonus += 1
                elif correct_answer == answer_text:
                    english_right += 1
                    english_right_with_bonus += 1
            elif index < 130:
                if question_id in wrong_questions_id:
                    gk_right_with_bonus += 1
                    if correct_answer == answer_text:
                        gk_right += 1
                    elif '--' in answer_text:
                        gk_not_attempted += 1
                elif '--' in answer_text:
                    gk_not_attempted += 1
                    gk_not_attempted_with_bonus += 1
                elif correct_answer == answer_text:
                    gk_right += 1
                    gk_right_with_bonus += 1
            elif index < 150:
                if question_id in wrong_questions_id:
                    computer_right_with_bonus += 1
                    if correct_answer == answer_text:
                        computer_right += 1
                    elif '--' in answer_text:
                        computer_not_attempted += 1
                elif '--' in answer_text:
                    computer_not_attempted += 1
                    computer_not_attempted_with_bonus += 1
                elif correct_answer == answer_text:
                    computer_right += 1
                    computer_right_with_bonus += 1

        # Save results to SQLite
        with lock:  # Ensure SQLite thread safety
            c.execute('''
                INSERT INTO results (
                    roll_number, link, candidate_name, venue_name, exam_date,
                    math_right, math_not_attempted, math_right_with_bonus, math_not_attempted_with_bonus,
                    reasoning_right, reasoning_not_attempted, reasoning_right_with_bonus, reasoning_not_attempted_with_bonus,

                    english_right, english_not_attempted, english_right_with_bonus, english_not_attempted_with_bonus,
                    gk_right, gk_not_attempted, gk_right_with_bonus, gk_not_attempted_with_bonus,
                    computer_right, computer_not_attempted, computer_right_with_bonus, computer_not_attempted_with_bonus
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (roll_number, link, candidate_name, venue_name, exam_date,
                  math_right, math_not_attempted, math_right_with_bonus, math_not_attempted_with_bonus,
                  reasoning_right, reasoning_not_attempted, reasoning_right_with_bonus, reasoning_not_attempted_with_bonus,
                  english_right, english_not_attempted, english_right_with_bonus, english_not_attempted_with_bonus,
                  gk_right, gk_not_attempted, gk_right_with_bonus, gk_not_attempted_with_bonus,
                  computer_right, computer_not_attempted, computer_right_with_bonus, computer_not_attempted_with_bonus))
            conn.commit()
    except Exception as e:
        print(f"Error processing roll number {roll_number}: {e}")


def process_in_parallel(roll_numbers, links, iteration_start, max_workers=20):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_candidate, roll_number, link): (roll_number, link) 
                   for roll_number, link in zip(roll_numbers[iteration_start:], links[iteration_start:])}

        for future in as_completed(futures):
            roll_number, link = futures[future]
            try:
                future.result()
                # Update the iteration number in the text file after processing each candidate
                global iteration_number
                iteration_number += 1
                with open('iteration.txt', 'w') as f:
                    f.write(f'{iteration_number}')
            except Exception as e:
                print(f"Error in future for roll number {roll_number}: {e}")


# Start parallel processing
process_in_parallel(roll_numbers, links, iteration_number)
