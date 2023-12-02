import boto3
from mock_dynamodb_setup import setup_dynamodb_user_list, setup_fall_semester_table
import re





def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    student_netID = event.get('netID')
    class_name = event.get('class_name')
    
    try:
        students_table = setup_dynamodb_user_list(dynamodb)

        student_response = students_table.get_item(
            Key={
                'netID': student_netID
            }
        )
        student = student_response.get('Item')

        classes_table = setup_fall_semester_table(dynamodb)
    
        class_response = classes_table.get_item(
            Key={
                'class_name': class_name
            }
        )
        course = class_response.get('Item')
    
        if not student or not course:
            return {
                'statusCode': 400,
                'body': 'Error: Student or class not found.'
            }
    
        student_courses = student.get('prior_courses')
        course_prerequisites = course.get('pre_requisites')
        
        #prerequisite check
        for prereq in course_prerequisites:
            if prereq not in student_courses:
                return {
                    'statusCode': 400,
                    'body': f'Error: Missing prerequisite {prereq}'
                }
    
        roster = course.get('roster', [])
        current = student.get('current_courses', [])
        max_enrollment = course.get('max_enrollment')  
        available_seats = course.get('available_seats')
        
        #check if student is already enrolled
        if student_netID in roster:
            return {
                'statusCode': 400,
                'body': 'Error: Student already registered.'
            }
    
        #check for available seats
        if available_seats <= 0:
            return {
                'statusCode': 400,
                'body': 'Error: Class is full.'
            }
            
        #check for schedule conflicts
        new_course_time = parse_meeting_time(course.get('meeting_time'))
        current_courses = student.get('current_courses')
        current_course_times = []
        
        for course_name in current_courses:
            course_response = classes_table.get_item(Key={'class_name': course_name})
            current_course = course_response.get('Item')
            if current_course:
                current_course_times.append(parse_meeting_time(current_course.get('meeting_time')))

        if check_conflict(new_course_time, current_course_times):
            return {
                'statusCode': 400,
                'body': 'Error: Class schedule conflicts with current courses.'
            }
            
        #update available seats and append course roster and student's current classes
        available_seats -= 1    
        roster.append(student_netID)
        current.append(class_name)
        update_roster = classes_table.update_item(
            Key={
                'class_name': class_name
            },
            UpdateExpression="SET roster = :r, available_seats = :as",
            ExpressionAttributeValues={
                ':r': roster,
                ':as': available_seats
            }
        )

        students_table = setup_dynamodb_user_list(dynamodb)

        update_course = students_table.update_item(
            Key={
                'netID': student_netID
            },
            UpdateExpression="SET current_courses = :r",
            ExpressionAttributeValues={
                ':r': current
            }
        )
    
        return {
            'statusCode': 200,
            'body': 'Successfully registered for the class.'
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error registering for the class.'
        }
        
def parse_meeting_time(meeting_time_str):
    #split string into days and times
    time_start_index = re.search("\d", meeting_time_str).start()
    days_str = meeting_time_str[:time_start_index].strip()
    times_str = meeting_time_str[time_start_index:].strip()

    #parse the days
    days = []
    day_mapping = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'TH': 'Thursday', 'F': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
    i = 0
    while i < len(days_str):
        if days_str[i:i+2] in day_mapping:
            days.append(day_mapping[days_str[i:i+2]])
            i += 2
        elif days_str[i] in day_mapping:
            days.append(day_mapping[days_str[i]])
            i += 1
        else:
            i += 1

    #parse the times
    start_time, end_time = times_str.split('-')

    return {
        'days': days,
        'start_time': start_time,
        'end_time': end_time
    }
    
def time_to_minutes(time_str):
    """Converts time in hh:mm format to pure minutes"""
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def check_conflict(new_course_time, current_course_times):
    new_start_time = time_to_minutes(new_course_time['start_time'])
    new_end_time = time_to_minutes(new_course_time['end_time'])
    
    for current_course in current_course_times:
        #check for day conflict
        day_overlap = any(day in new_course_time['days'] for day in current_course['days'])
        
        if day_overlap:
            current_start_time = time_to_minutes(current_course['start_time'])
            current_end_time = time_to_minutes(current_course['end_time'])
            
            #check for time conflict
            if (new_start_time < current_end_time and new_end_time > current_start_time):
                return True

    return False