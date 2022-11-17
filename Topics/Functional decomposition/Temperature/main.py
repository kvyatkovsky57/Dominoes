def fahrenheit_to_celsius(temps_f):
    temps_c = (temps_f - 32) * 5 / 9
    return round(temps_c, 2)


def celsius_to_fahrenheit(temps_c):
    temps_f = temps_c * 9 / 5 + 32
    return round(temps_f, 2)

def print_answer(new_temp, new_unit):
    return print(f'{new_temp} {new_unit}')

def main():
    """Entry point of the program."""
    temperature, unit = input().split()  # read the input
    
    if str(unit).lower() == 'c':
        new_temp = celsius_to_fahrenheit(int(temperature))
        new_unit = 'F'
    elif str(unit).lower() == 'f':
        new_temp = fahrenheit_to_celsius(int(temperature))
        new_unit = 'C'
    
    print_answer(new_temp, new_unit)
