from datetime import datetime, timedelta, date

users = [
    {"name": "John Doe", "birthday": "1985.10.19"},
    {"name": "Jane Smith", "birthday": "1990.01.27"}
]

def calc_next_monday(d: date) -> date:
    days = (7 - d.weekday()) % 7
    return d + timedelta(days=7 if days == 0 else days)

def next_available_greeting_date(birthday: date) -> date:
    is_weekend = date.weekday(birthday) >= 5
    next_monday = calc_next_monday(birthday)
    return next_monday if is_weekend else birthday

def get_upcoming_birthdays(users):
    upcoming_greetings = list()
    # filter out the onse outside 7d range
    for user_info in users:
        birthday = datetime.strptime(user_info["birthday"], "%Y.%m.%d").date()
        next_birthday = date(datetime.today().year, birthday.month, birthday.day)
        greetings_range_start = datetime.now().date()
        greetings_range_end = greetings_range_start + timedelta(days=7)
        birthday_is_in_greeting_range = next_birthday >= greetings_range_start and next_birthday <= greetings_range_end
        if birthday_is_in_greeting_range:
            upcoming_greetings.append({"name": user_info['name'], "congratulation_date": next_available_greeting_date(next_birthday)})

    return upcoming_greetings

upcoming_birthdays = get_upcoming_birthdays(users)
print("List of congratulations for this week:", upcoming_birthdays)