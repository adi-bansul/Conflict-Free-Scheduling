from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta, date
import random
import calendar
import holidays

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/college_tt', methods=['GET', 'POST'])
def college_tt():
    if request.method == 'POST':
        # Process form data (unchanged from previous version)
        academic_year = int(request.form['academic_year'])
        use_default = request.form.get('use_default', 'no')
        
        if use_default == 'yes':
            default_times = {
                1: "08:00",
                2: "10:00",
                3: "10:00",
                4: "11:00"
            }
            start_time = default_times[academic_year]
            mode = "Offline" if academic_year in [1, 2, 3] else "Online"
        else:
            start_time = request.form['custom_time']
            mode = request.form['mode']
        
        working_days = int(request.form['working_days'])
        subjects = request.form.getlist('subjects[]')
        
        theory_lectures = int(request.form['theory_lectures'])
        lab_lectures = int(request.form['lab_lectures'])
        tutorial_lectures = int(request.form['tutorial_lectures'])
        
        theory_duration = float(request.form['theory_duration'])
        lab_duration = float(request.form['lab_duration'])
        tutorial_duration = float(request.form['tutorial_duration'])
        
        break_duration = float(request.form['break_duration'])
        
        # Generate timetable (unchanged from previous version)
        timetable = {}
        current_time = datetime.strptime(start_time, "%H:%M")
        
        # Create lecture pools
        theory_pool = [(subj, f'Theory ({mode})') for subj in subjects for _ in range(theory_lectures)]
        lab_pool = [(subj, f'Lab ({mode})') for subj in subjects for _ in range(lab_lectures)]
        tutorial_pool = [(subj, f'Tutorial ({mode})') for subj in subjects for _ in range(tutorial_lectures)]
        
        random.shuffle(theory_pool)
        random.shuffle(lab_pool)
        random.shuffle(tutorial_pool)
        
        MAX_CONSECUTIVE_HOURS = 3
        
        for day in range(1, working_days + 1):
            day_name = get_day_name(day)
            timetable[day_name] = []
            current_time = datetime.strptime(start_time, "%H:%M")
            consecutive_hours = 0
            
            # Add lectures for the day
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
                
                if consecutive_hours >= MAX_CONSECUTIVE_HOURS:
                    end_time = current_time + timedelta(hours=break_duration)
                    timetable[day_name].append({
                        'name': 'Break',
                        'start': current_time.strftime("%H:%M"),
                        'end': end_time.strftime("%H:%M")
                    })
                    current_time = end_time
                    consecutive_hours = 0
            
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
                
                if consecutive_hours >= MAX_CONSECUTIVE_HOURS:
                    end_time = current_time + timedelta(hours=break_duration)
                    timetable[day_name].append({
                        'name': 'Break',
                        'start': current_time.strftime("%H:%M"),
                        'end': end_time.strftime("%H:%M")
                    })
                    current_time = end_time
                    consecutive_hours = 0
            
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
                
                if consecutive_hours >= MAX_CONSECUTIVE_HOURS:
                    end_time = current_time + timedelta(hours=break_duration)
                    timetable[day_name].append({
                        'name': 'Break',
                        'start': current_time.strftime("%H:%M"),
                        'end': end_time.strftime("%H:%M")
                    })
                    current_time = end_time
                    consecutive_hours = 0
        
        return render_template('college_result.html', 
                            academic_year=academic_year,
                            mode=mode,
                            timetable=timetable)
    
    return render_template('college_tt.html')

@app.route('/exam_tt', methods=['GET', 'POST'])
def exam_tt():
    if request.method == 'POST':
        # Process form data
        num_subjects = int(request.form['num_subjects'])
        subjects = []
        
        for i in range(num_subjects):
            subject_name = request.form[f'subject_{i}_name']
            components = {
                'Theory': request.form.get(f'subject_{i}_theory') == 'on',
                'Lab': request.form.get(f'subject_{i}_lab') == 'on',
                'Course project': request.form.get(f'subject_{i}_course_project') == 'on',
                'Viva': request.form.get(f'subject_{i}_viva') == 'on',
                'Seminar PPT': request.form.get(f'subject_{i}_seminar_ppt') == 'on'
            }
            subjects.append({'name': subject_name, 'components': components})
        
        year = int(request.form['year'])
        start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d").date()
        
        # Check if start date is before end date
        if start_date > end_date:
            flash('Error: Start date must be before end date', 'danger')
            return redirect(url_for('exam_tt'))
        
        # Check if dates are in the same year
        if start_date.year != year or end_date.year != year:
            flash('Error: Dates must be in the same year as specified', 'danger')
            return redirect(url_for('exam_tt'))
        
        # Get all holidays
        try:
            holidays_list = get_holidays(year)
        except:
            holidays_list = []
        
        # Calculate working days available
        total_days = (end_date - start_date).days + 1
        working_days = total_days - len([d for d in holidays_list if start_date <= d <= end_date])
        
        # Calculate required days under normal scheduling
        required_days = calculate_required_days(subjects)
        
        # Check if dates are feasible
        if working_days < required_days / 2:  # Less than half required
            flash('Error: The time between start and end dates is extremely short. Exams cannot be scheduled in such a short timespan.', 'danger')
            return redirect(url_for('exam_tt'))
        
        if working_days < required_days:
            # Store data in session to use after user confirms
            request.session['exam_data'] = {
                'subjects': subjects,
                'year': year,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'holidays_list': [d.isoformat() for d in holidays_list],
                'working_days': working_days,
                'required_days': required_days
            }
            return render_template('exam_confirm.html', 
                                working_days=working_days,
                                required_days=required_days)
        
        # Generate normal timetable if enough days are available
        timetable = generate_normal_timetable(subjects, year, start_date, end_date, holidays_list)
        return render_template('exam_result.html', 
                            timetable=timetable,
                            year=year,
                            compressed=False)
    
    return render_template('exam_tt.html')

@app.route('/exam_confirm', methods=['POST'])
def exam_confirm():
    if request.method == 'POST':
        # Retrieve data from session
        exam_data = request.session.get('exam_data')
        if not exam_data:
            flash('Error: Session data missing. Please try again.', 'danger')
            return redirect(url_for('exam_tt'))
        
        # Convert back to proper types
        subjects = exam_data['subjects']
        year = exam_data['year']
        start_date = date.fromisoformat(exam_data['start_date'])
        end_date = date.fromisoformat(exam_data['end_date'])
        holidays_list = [date.fromisoformat(d) for d in exam_data['holidays_list']]
        
        if request.form.get('confirm') == 'yes':
            # Generate compressed timetable
            timetable, complete = generate_compressed_timetable(
                subjects, year, start_date, end_date, holidays_list
            )
            
            if not complete:
                flash('Warning: Could not schedule all exams within the given dates. Showing partial schedule.', 'warning')
            
            return render_template('exam_result.html', 
                                timetable=timetable,
                                year=year,
                                compressed=True)
        else:
            return redirect(url_for('exam_tt'))

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

def generate_normal_timetable(subjects, year, start_date, end_date, holidays_list):
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

def get_day_name(day_num):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[day_num - 1] if day_num <= 7 else f"Day {day_num}"

def get_holidays(year, country='IN'):
    try:
        holiday_dates = holidays.CountryHoliday(country, years=year).keys()
    except:
        holiday_dates = set()
    
    cal = calendar.Calendar()
    sundays = []
    for month in range(1, 13):
        for day in cal.itermonthdays2(year, month):
            if day[0] != 0 and day[1] == 6:  # day[1] = 6 is Sunday
                sundays.append(date(year, month, day[0]))
    
    # Combine and return unique dates
    all_holidays = set(holiday_dates).union(set(sundays))
    return sorted(all_holidays)

def get_holiday_name(date_obj, year):
    # Check if it's a Sunday
    if date_obj.weekday() == 6:
        return "Sunday"
    
    # Check Indian holidays
    try:
        in_holidays = holidays.CountryHoliday('IN', years=year)
        return in_holidays.get(date_obj, "Holiday")
    except:
        return "Holiday"

if __name__ == '__main__':
    app.run(debug=True)