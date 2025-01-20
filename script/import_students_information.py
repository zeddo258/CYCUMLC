import openpyxl
from datetime import datetime
from attendance.models import Student


def import_from(file_path):
    """
    Import students from an XLSX file into the Student model.
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active  # Assumes data is in the first sheet

    # Iterate through rows, assuming the header is in the first row
    for row in sheet.iter_rows(min_row=2, values_only=True):
        try:
            chinese_name = row[1]  # Column A: 學員姓名
            nationality = row[5]
            sex = 'Female' if row[2] == '女' else 'Male'  # Column C: 性別, translate to English
            english_name = row[7]
            passport_id = row[8]
            birth_date = row[9]
            class_time = row[10]
            first_day = row[13]
            if birth_date and isinstance(birth_date, datetime):
                birth_date_formatted = birth_date.strftime('%Y-%m-%d')
            elif isinstance(birth_date, str):
                # Remove unwanted characters like \n and reformat
                birth_date_cleaned = birth_date.strip()  # Remove trailing \n
                birth_date_obj = datetime.strptime(birth_date_cleaned, '%Y/%m/%d')  # Parse the string
                birth_date_formatted = birth_date_obj.strftime('%Y-%m-%d')  # Format to YY-MM-DD
            else:
                birth_date_formatted = birth_date 
             
            if first_day and isinstance(birth_date, datetime):
                fday_formatted = first_day.strftime('%Y-%m-%d')
            else:
                fday_formatted = first_day
            
            # Create or update the student record
            student, created = Student.objects.update_or_create(
                id=passport_id,  # Use 護照號碼 as the unique identifier
                defaults={
                    'chinese_name': chinese_name,
                    'english_name': english_name,
                    'sex': sex,
                    'birth': birth_date_formatted,
                    'nationality': nationality,
                    'study_time': class_time,
                }
            )
            if created:
                print(f"Student {student.chinese_name} added successfully.")
            else:
                print(f"Student {student.chinese_name} updated successfully.")

        except Exception as e:
            print(f"Error adding student {row[7]}: {e}")



