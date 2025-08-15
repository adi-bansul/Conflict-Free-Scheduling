import datetime
from datetime import timedelta
import calendar
import holidays

def get_user_input():
    print("=== Exam Timetable Scheduling System ===")
    
    # Get number of subjects
    while True:
        try:
            num_subjects = int(input("Enter the number of subjects: "))
            if num_subjects > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Get components for each subject
    subjects = []
    for i in range(num_subjects):
        print(f"\nSubject {i+1}:")
        name = input("Enter subject name: ")
        
        components = {}
        for comp in ['Theory', 'Lab', 'Course project', 'Viva', 'Seminar PPT']:
            while True:
                resp = input(f"Does it have {comp} component? (Y/N): ").upper()
                if resp in ['Y', 'N']:
                    components[comp] = (resp == 'Y')
                    break
                print("Please enter Y or N.")
        
        subjects.append({'name': name, 'components': components})
    
    # Get year and date range
    while True:
        try:
            year = int(input("\nEnter the year for the exam schedule: "))
            if year >= datetime.datetime.now().year:
                break
            print("Year must be current or future.")
        except ValueError:
            print("Invalid year. Please enter a number.")
    
    while True:
        start_date_str = input("Enter exam start date (DD-MM-YYYY): ")
        end_date_str = input("Enter exam end date (DD-MM-YYYY): ")
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%d-%m-%Y").date()
            end_date = datetime.datetime.strptime(end_date_str, "%d-%m-%Y").date()
            if start_date > end_date:
                print("Start date must be before end date.")
                continue
            if start_date.year == year and end_date.year == year:
                break
            print(f"Dates must be in the same year ({year}).")
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY.")
    
    return subjects, year, start_date, end_date

def get_holidays(year, country='IN'):
    # Get national holidays for India
    holiday_dates = holidays.CountryHoliday(country, years=year).keys()
    
    # Add Sundays
    cal = calendar.Calendar()
    sundays = []
    for month in range(1, 13):
        for day in cal.itermonthdays2(year, month):
            if day[0] != 0 and day[1] == 6:  # day[1] = 6 is Sunday
                sundays.append(datetime.date(year, month, day[0]))
    
    # Combine and return unique dates
    all_holidays = set(holiday_dates).union(set(sundays))
    return sorted(all_holidays)

def calculate_required_days(subjects):
    component_counts = {
        'Theory': 0,
        'Lab': 0,
        'Course project': 0,
        'Seminar PPT': 0,
        'Viva': 0
    }
    
    for subject in subjects:
        for comp, has_comp in subject['components'].items():
            if has_comp:
                component_counts[comp] += 1
    
    # Calculate required days with breaks
    total_days = 0
    components_order = ['Theory', 'Lab', 'Course project', 'Seminar PPT', 'Viva']
    
    for comp in components_order:
        if component_counts[comp] > 0:
            total_days += component_counts[comp]  # Each component takes 1 day per exam
            if comp != components_order[-1]:  # Add break after each component except last
                total_days += 2  # 2-day break between components
    
    return total_days

def generate_compressed_timetable(subjects, year, start_date, end_date, holidays_list):
    current_date = start_date
    timetable = []
    scheduled_exams = {comp: [] for comp in ['Theory', 'Lab', 'Course project', 'Seminar PPT', 'Viva']}
    
    # First pass: Schedule Course Projects and Seminar PPTs (grouped when possible)
    for subject in subjects:
        if subject['components'].get('Course project', False):
            while current_date <= end_date:
                if current_date in holidays_list:
                    timetable.append({
                        'date': current_date,
                        'type': 'holiday',
                        'content': "HOLIDAY (" + get_holiday_name(current_date, year) + ")"
                    })
                    current_date += timedelta(days=1)
                    continue
                
                # Try to pair with Seminar PPT from same subject
                entry_content = f"{subject['name']} Course project"
                if subject['components'].get('Seminar PPT', False):
                    entry_content += f" + {subject['name']} Seminar PPT"
                    scheduled_exams['Seminar PPT'].append(subject['name'])
                    subject['components']['Seminar PPT'] = False
                
                timetable.append({
                    'date': current_date,
                    'type': 'exam',
                    'content': entry_content
                })
                scheduled_exams['Course project'].append(subject['name'])
                current_date += timedelta(days=1)
                break
            else:
                return timetable, False

    # Second pass: Schedule remaining Seminar PPTs
    for subject in subjects:
        if subject['components'].get('Seminar PPT', False):
            while current_date <= end_date:
                if current_date in holidays_list:
                    timetable.append({
                        'date': current_date,
                        'type': 'holiday',
                        'content': "HOLIDAY (" + get_holiday_name(current_date, year) + ")"
                    })
                    current_date += timedelta(days=1)
                    continue
                
                timetable.append({
                    'date': current_date,
                    'type': 'exam',
                    'content': f"{subject['name']} Seminar PPT"
                })
                scheduled_exams['Seminar PPT'].append(subject['name'])
                current_date += timedelta(days=1)
                break
            else:
                return timetable, False

    # Third pass: Schedule Theory and Vivas (grouped when possible)
    for subject in subjects:
        if subject['components'].get('Theory', False):
            while current_date <= end_date:
                if current_date in holidays_list:
                    timetable.append({
                        'date': current_date,
                        'type': 'holiday',
                        'content': "HOLIDAY (" + get_holiday_name(current_date, year) + ")"
                    })
                    current_date += timedelta(days=1)
                    continue
                
                # Try to pair with Viva from same subject
                entry_content = f"{subject['name']} Theory"
                if subject['components'].get('Viva', False):
                    entry_content += f" + {subject['name']} Viva"
                    scheduled_exams['Viva'].append(subject['name'])
                    subject['components']['Viva'] = False
                
                timetable.append({
                    'date': current_date,
                    'type': 'exam',
                    'content': entry_content
                })
                scheduled_exams['Theory'].append(subject['name'])
                current_date += timedelta(days=1)
                break
            else:
                return timetable, False

    # Fourth pass: Schedule remaining Vivas
    remaining_vivas = [s['name'] for s in subjects if s['components'].get('Viva', False)]
    for i in range(0, len(remaining_vivas), 2):  # Schedule 2 vivas per day
        if i+1 < len(remaining_vivas):
            content = f"{remaining_vivas[i]} Viva + {remaining_vivas[i+1]} Viva"
        else:
            content = f"{remaining_vivas[i]} Viva"
        
        while current_date <= end_date:
            if current_date in holidays_list:
                timetable.append({
                    'date': current_date,
                    'type': 'holiday',
                    'content': "HOLIDAY (" + get_holiday_name(current_date, year) + ")"
                })
                current_date += timedelta(days=1)
                continue
            
            timetable.append({
                'date': current_date,
                'type': 'exam',
                'content': content
            })
            scheduled_exams['Viva'].extend(remaining_vivas[i:i+2])
            current_date += timedelta(days=1)
            break
        else:
            return timetable, False

    return timetable, True

def generate_timetable(subjects, year, start_date, end_date):
    # Get all holidays
    holidays_list = get_holidays(year)
    
    # Calculate working days available
    total_days = (end_date - start_date).days + 1
    working_days = total_days - len([d for d in holidays_list if start_date <= d <= end_date])
    
    # Calculate required days under normal scheduling
    required_days = calculate_required_days(subjects)
    
    # Check if dates are feasible
    if working_days < required_days / 2:  # Less than half required
        print("\nWarning: The time between start and end dates is extremely short.")
        print("Exams cannot be scheduled in such a short timespan.")
        return None
    
    if working_days < required_days:
        print(f"\nWarning: Only {working_days} working days available between the dates.")
        print(f"Normal scheduling requires {required_days} working days.")
        choice = input("Do you want to proceed with a compressed schedule? (Y/N): ").upper()
        if choice != 'Y':
            return None
        
        # Generate compressed timetable
        timetable, complete = generate_compressed_timetable(
            subjects, year, start_date, end_date, holidays_list
        )
        
        if not complete:
            print("\nWarning: Could not schedule all exams within the given dates.")
            choice = input("Do you want to see the partial schedule? (Y/N): ").upper()
            if choice != 'Y':
                return None
        return timetable
    
    # Normal scheduling if enough days are available
    component_order = ['Theory', 'Lab', 'Course project', 'Seminar PPT', 'Viva']
    exams_by_component = {comp: [] for comp in component_order}
    
    for subject in subjects:
        for comp, has_comp in subject['components'].items():
            if has_comp:
                exams_by_component[comp].append(subject['name'])
    
    current_date = start_date
    timetable = []
    
    for comp in component_order:
        exams = exams_by_component[comp]
        if not exams:
            continue
        
        # Add component header
        timetable.append({
            'date': current_date,
            'type': 'header',
            'content': f"=== {comp} Exams ==="
        })
        
        # Schedule exams for this component
        for exam in exams:
            # Skip holidays
            while current_date in holidays_list:
                timetable.append({
                    'date': current_date,
                    'type': 'holiday',
                    'content': "HOLIDAY (" + get_holiday_name(current_date, year) + ")"
                })
                current_date += timedelta(days=1)
                if current_date > end_date:
                    return timetable
            
            if current_date > end_date:
                return timetable
            
            timetable.append({
                'date': current_date,
                'type': 'exam',
                'content': f"{exam} {comp}"
            })
            current_date += timedelta(days=1)
        
        # Add break between components (2 working days)
        if comp != component_order[-1]:  # No break after last component
            break_days = 2
            while break_days > 0 and current_date <= end_date:
                if current_date in holidays_list:
                    timetable.append({
                        'date': current_date,
                        'type': 'holiday',
                        'content': "HOLIDAY (" + get_holiday_name(current_date, year) + ")"
                    })
                else:
                    break_days -= 1
                current_date += timedelta(days=1)
    
    return timetable

def get_holiday_name(date, year):
    # Check if it's a Sunday
    if date.weekday() == 6:
        return "Sunday"
    
    # Check Indian holidays
    in_holidays = holidays.CountryHoliday('IN', years=year)
    return in_holidays.get(date, "Holiday")

def display_timetable(timetable):
    if not timetable:
        return
    
    print("\n=== Generated Exam Timetable ===")
    current_date = None
    
    for entry in timetable:
        if entry['date'] != current_date:
            current_date = entry['date']
            day_name = current_date.strftime("%A")
            print(f"\n{day_name}, {current_date.strftime('%d-%m-%Y')}:")
        
        if entry['type'] == 'header':
            print(f"\n{entry['content']}")
        elif entry['type'] == 'holiday':
            print(f"*** {entry['content']} ***")
        else:
            print(f"- {entry['content']}")

def main():
    subjects, year, start_date, end_date = get_user_input()
    timetable = generate_timetable(subjects, year, start_date, end_date)
    display_timetable(timetable)

if __name__ == "__main__":
    main()