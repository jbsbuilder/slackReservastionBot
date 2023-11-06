import slack_sdk
import os
from dotenv import load_dotenv
import calendar

env_path = ".env"
load_dotenv(env_path)

client = slack_sdk.WebClient(os.environ['Slack_BOT_TOKEN'])

def block_out_days(cal_str, year, month):
    # Find out how many days are in the month
    _, num_days_in_month = calendar.monthrange(year, month)

    # Ask the user which days to block out
    days_to_block = input(f"Enter the days to block out (1-{num_days_in_month}): ")
    days_to_block = [int(day.strip()) for day in days_to_block.split(',')]

    # Split the calendar string into lines
    lines = cal_str.split('\n')
    
    # The days of the week header is always the second line
    days_of_week = lines[1].split()
    
    # New list to hold modified lines
    new_lines = [lines[0], lines[1]]
    
    # Start at the first line with dates
    for line in lines[2:]:
        new_line = line
        for day in days_to_block:
            # Each day number is right-aligned and occupies 3 spaces
            day_str = "{:>2}".format(day)  # Right-align the day in a 2-char field
            new_line = new_line.replace(day_str, 'XX')
        new_lines.append(new_line)
    
    # Join the modified lines back into a single string
    new_cal_str = '\n'.join(new_lines)
    return new_cal_str

# Ask the user for the year and month
year = int(input("Enter the year (e.g., 2023): "))
month = int(input("Enter the month (1-12): "))

# Create a text calendar instance
cal = calendar.TextCalendar(calendar.SUNDAY)

# Generate the calendar for the given month and year
cal_str = cal.formatmonth(year, month)

# Call the function to block out specified days
blocked_cal_str = block_out_days(cal_str, year, month)

def post_message(blocked_cal_str):
    client.chat_postMessage(channel='#powmow', text=blocked_cal_str)
    print(blocked_cal_str)
