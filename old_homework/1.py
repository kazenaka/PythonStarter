new_list = [99, 7, 55, 15, 99, 7, 55, 15, 99, 7, 55, 15]
user_number = int(input('Введите число'))
count_number = new_list.count(user_number)

all_numbers = []
for index, value in enumerate(new_list):
    if value == user_number:
        all_numbers.append(index)

print(f'Число {user_number} встречается в списке {count_number} раз/а в позициях: {all_numbers}')
