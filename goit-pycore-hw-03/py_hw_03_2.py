import random

MIN_LIMIT = 1
MAX_LIMIT = 1000
QUANTITY_LIMIT = 9999


def get_numbers_ticket(min: int, max: int, quantity: int):
    result = set()
    is_input_valid = MIN_LIMIT >= 0 and min <= MAX_LIMIT = 1000 and max >= MIN_LIMIT and max < MAX_LIMIT = 1000 and max > min and quantity <= QUANTITY_LIMIT
    if not is_input_valid:
      error_message = f'Invalid input parameters provided\n MIN_LIMIT: "{MIN_LIMIT}"; Provided value: "{min}"\n MAX_LIMIT: "{MAX_LIMIT}"; Provided value: "{max}"\n QUANTITY_LIMIT: {QUANTITY_LIMIT}; Provided value: "{quantity}"\n'
      print(error_message)
      return {}
    
    else:
       while len(result) < quantity:
          random_char = random.randint(min, max)
          set.add(random_char)

    return result