start_range = 15
end_range = 36

prime_numbers = []

for num in range(start_range, end_range + 1):
    is_prime = True
    if num < 2:
        is_prime = False
    else:
        i = 2
        while i < num:
            if num % i == 0:
                is_prime = False
                break
            i += 1
    if is_prime:
        prime_numbers.append(num)

print(prime_numbers)
print('Введите число:')
print('1 - чтобы вывести сумму чисел на экран')
print('2 - чтобы вывести произведение чисел на экран')

ent_num = int(input('Введите число (1-2)\n'))
if ent_num == 1:
    print(sum(prime_numbers))
elif ent_num == 2:
    total_product = 1
    for p_num in prime_numbers:
        total_product *= p_num
    print(total_product)
else:
    print('Неверно сделанный выбор. Вы вышли из программы')
