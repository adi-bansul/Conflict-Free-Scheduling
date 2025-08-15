from datetime import datetime, timedelta
import random

def generate_timetable():
    print("Timetable Scheduling System")
    print("--------------------------\n")
    
    # User Inputs - Academic Year
    academic_year = int(input("Enter Academic Year (1-4): "))
    while academic_year not in [1, 2, 3, 4]:
        print("Invalid input! Please enter a value between 1 and 4.")
        academic_year = int(input("Enter Academic Year (1-4): "))
    
    # Determine default start time based on academic year
    default_times = {
        1: "08:00",
        2: "10:00",
        3: "10:00",
        4: "11:00"
    }
    mode = "Offline" if academic_year in [1, 2, 3] else "Online"
    
    # Ask if user wants to use default time or custom
    use_default = input(f"Use default start time ({default_times[academic_year]} {mode})? (yes/no): ").lower()
    if use_default == 'yes' or use_default == 'y':
        start_time_str = default_times[academic_year]
    else:
        start_time_str = input("Enter custom start time (HH:MM format, 24-hour clock): ")
    
    # Rest of the user inputs
    working_days = int(input("\nEnter number of working days (Monday is day 1): "))
    num_subjects = int(input("Enter number of subjects: "))
    
    # Get subject names
    subjects = []
    for i in range(num_subjects):
        subject = input(f"Enter name of subject {i+1}: ")
        subjects.append(subject)
    
    print("\nEnter lecture types (per week for each subject):")
    theory_lectures = int(input("Number of theory lectures per subject: "))
    lab_lectures = int(input("Number of lab lectures per subject: "))
    tutorial_lectures = int(input("Number of tutorial lectures per subject: "))
    
    print("\nEnter lecture durations (in hours):")
    theory_duration = float(input("Duration of theory lectures: "))
    lab_duration = float(input("Duration of lab lectures: "))
    tutorial_duration = float(input("Duration of tutorial lectures: "))
    
    break_duration = float(input("\nEnter break duration (in hours): "))
    
    # Constants
    START_TIME = datetime.strptime(start_time_str, "%H:%M")
    MAX_CONSECUTIVE_HOURS = 3  # Max 3 hours without break
    
    # Create lecture pools for each type
    theory_pool = []
    for subject in subjects:
        theory_pool.extend([(subject, f'Theory ({mode})')] * theory_lectures)
    
    lab_pool = []
    for subject in subjects:
        lab_pool.extend([(subject, f'Lab ({mode})')] * lab_lectures)
    
    tutorial_pool = []
    for subject in subjects:
        tutorial_pool.extend([(subject, f'Tutorial ({mode})')] * tutorial_lectures)
    
    # Shuffle the pools to distribute subjects
    random.shuffle(theory_pool)
    random.shuffle(lab_pool)
    random.shuffle(tutorial_pool)
    
    # Generate timetable
    timetable = {}
    current_time = START_TIME
    
    for day in range(1, working_days + 1):
        day_name = get_day_name(day)
        timetable[day_name] = []
        current_time = START_TIME  # Reset time for each day
        consecutive_hours = 0
        
        # Add lectures for this day
        # Try to add one of each type per day (if available)
        
        # Add theory lecture
        if theory_pool:
            subject, lect_type = theory_pool.pop()
            end_time = current_time + timedelta(hours=theory_duration)
            timetable[day_name].append({
                'name': f"{subject} ({lect_type})",
                'start': current_time.strftime("%H:%M"),
                'end': end_time.strftime("%H:%M")
            })
            current_time = end_time
            consecutive_hours += theory_duration
            
            # Check if break needed
            if consecutive_hours >= MAX_CONSECUTIVE_HOURS:
                end_time = current_time + timedelta(hours=break_duration)
                timetable[day_name].append({
                    'name': 'Break',
                    'start': current_time.strftime("%H:%M"),
                    'end': end_time.strftime("%H:%M")
                })
                current_time = end_time
                consecutive_hours = 0
        
        # Add lab lecture
        if lab_pool:
            subject, lect_type = lab_pool.pop()
            end_time = current_time + timedelta(hours=lab_duration)
            timetable[day_name].append({
                'name': f"{subject} ({lect_type})",
                'start': current_time.strftime("%H:%M"),
                'end': end_time.strftime("%H:%M")
            })
            current_time = end_time
            consecutive_hours += lab_duration
            
            # Check if break needed
            if consecutive_hours >= MAX_CONSECUTIVE_HOURS:
                end_time = current_time + timedelta(hours=break_duration)
                timetable[day_name].append({
                    'name': 'Break',
                    'start': current_time.strftime("%H:%M"),
                    'end': end_time.strftime("%H:%M")
                })
                current_time = end_time
                consecutive_hours = 0
        
        # Add tutorial lecture
        if tutorial_pool:
            subject, lect_type = tutorial_pool.pop()
            end_time = current_time + timedelta(hours=tutorial_duration)
            timetable[day_name].append({
                'name': f"{subject} ({lect_type})",
                'start': current_time.strftime("%H:%M"),
                'end': end_time.strftime("%H:%M")
            })
            current_time = end_time
            consecutive_hours += tutorial_duration
            
            # Check if break needed
            if consecutive_hours >= MAX_CONSECUTIVE_HOURS:
                end_time = current_time + timedelta(hours=break_duration)
                timetable[day_name].append({
                    'name': 'Break',
                    'start': current_time.strftime("%H:%M"),
                    'end': end_time.strftime("%H:%M")
                })
                current_time = end_time
                consecutive_hours = 0
    
    # Display timetable
    print(f"\nGenerated Timetable for Year {academic_year} ({mode}):")
    print("=========================================")
    
    for day, slots in timetable.items():
        print(f"\n{day}:")
        print("{:<30} {:<10} {:<10}".format("Subject (Type)", "Start", "End"))
        print("-" * 50)
        for slot in slots:
            print("{:<30} {:<10} {:<10}".format(
                slot['name'], slot['start'], slot['end']))
    
    print("\nTimetable generation complete!")

def get_day_name(day_num):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[day_num - 1] if day_num <= 7 else f"Day {day_num}"

if __name__ == "__main__":
    generate_timetable()