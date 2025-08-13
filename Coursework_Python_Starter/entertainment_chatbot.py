import random
import pyjokes
import emoji
from prettytable import PrettyTable
from termcolor import colored

# Общая база данных контента
content_data = {
    'films': ["Интерстеллар", "Начало", "Матрица", "Криминальное чтиво", "Властелин колец"],
    'music': ["Imagine Dragons", "The Beatles", "Linkin Park", "BTS", "Coldplay", "Metallica"],
    'games': ["Ведьмак 3: Дикая Охота", "Minecraft", "Cyberpunk 2077", "Assassin's Creed: Odyssey"],
    'jokes': [],  # pyjokes подтягивает откуда-то автоматически
    'stories': [
        "Программист всю ночь искал баг, который оказался неправильно поставленной запятой.",
        "Наконец-то написав идеальный код, программист понял, что забыл сохранить файл.",
        "Разработчик заснул за клавиатурой и проснулся от звонка начальника, который хвалил его за идеальный автокоммит.",
        "Программист, работавший над искусственным интеллектом, внезапно обнаружил, что его кофемашина начала отвечать на вопросы.",
        "Когда дедлайн горел, программист нашёл решение проблемы, которое пришло к нему во сне."
    ]
}


def show_menu():
    """
    Отображает главное меню чат-бота. В меню выбор действий с эмодзи. Таблица выравнивается по левому краю.
    """
    table = PrettyTable()
    table.align = 'l'
    table.field_names = [colored("№", "cyan"), colored("Действие", "green")]
    menu_items = [
        (1, emoji.emojize(":clapper: Фильмы посмотреть", language='alias')),
        (2, emoji.emojize(":musical_note: Музыка послушать", language='alias')),
        (3, emoji.emojize(":video_game: Игры поиграть", language='alias')),
        (4, emoji.emojize(":joy: Шутки посмеяться", language='alias')),
        (5, emoji.emojize(":book: Истории послушать", language='alias')),
        (6, emoji.emojize(":game_die: Игра 'Угадай число'", language='alias')),
        (0, emoji.emojize(":door: Выход", language='alias'))
    ]
    for num, action in menu_items:
        table.add_row([num, action])
    print(table)


def recommend(category):
    """
    Выводит рекомендации по выбранной категории: фильмы, музыка, игры и т.д.
    """
    print(colored(f"Рекомендую {category}:", "yellow"))
    for item in content_data[category]:
        print(f"- {item}")


def tell_joke():
    """
    Выводит случайную шутку с использованием модуля pyjokes, качает откуда-то из интернета.
    """
    print(colored(pyjokes.get_joke(), "magenta"))


def tell_story():
    """
    Выводит короткие истории про программистов. Сорян, юмор спецефический. Интересно, тоже таким стану?
    """
    story = random.choice(content_data['stories'])
    print(colored(story, "cyan"))


def guess_number():
    """
    Игра "Угадай число". Бот загадывает число от 1 до 100. Пользователь вводит варианты.
    Бот подсказывает "Больше" или "Меньше". При угадывании выводится поздравление с эмодзи.
    """
    number = random.randint(1, 100)
    print(colored("Загадал число от 1 до 100. Попробуй угадать!", "yellow"))
    while True:
        try:
            guess = int(input("Твой вариант: "))
        except ValueError:
            print(colored("Введите целое число!", "red"))
            continue
        if guess < number:
            print("Больше")
        elif guess > number:
            print("Меньше")
        else:
            print(colored(f"Ура, четко! Ты угадал! {emoji.emojize(':tada:', language='alias')}", "green"))
            break


def main():
    """
    Основной цикл чат-бота. Отображает меню и обрабатывает ввод пользователя.
    """
    while True:
        show_menu()
        choice = input(colored("Выберите действие: ", "blue"))
        if choice == '1':
            recommend('films')
        elif choice == '2':
            recommend('music')
        elif choice == '3':
            recommend('games')
        elif choice == '4':
            tell_joke()
        elif choice == '5':
            tell_story()
        elif choice == '6':
            guess_number()
        elif choice == '0':
            print(colored("Спасибо! До свидания!", "green"))
            break
        else:
            print(colored("Ку, числа от 1 до 6 и 0 для выхода))", "red"))


main()
input("Нажмите Enter для выхода...")
