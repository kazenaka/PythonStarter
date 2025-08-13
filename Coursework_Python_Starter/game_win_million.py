import random
import json
import os
from copy import deepcopy
from playsound import playsound

# --- База данных вопросов ---
QUESTIONS = [
    {"question": "Какая самая большая планета в Солнечной системе?",
     "options": ["Марс", "Земля", "Юпитер", "Сатурн"], "answer_index": 2},
    {"question": "Какой элемент обозначается символом 'Fe'?",
     "options": ["Фтор", "Железо", "Золото", "Серебро"], "answer_index": 1},
    {"question": "Кто написал 'Гамлета'?",
     "options": ["Чарльз Диккенс", "Уильям Шекспир", "Лев Толстой", "Джейн Остин"], "answer_index": 1},
    {"question": "Как называется столица Австралии?",
     "options": ["Сидней", "Мельбурн", "Канберра", "Перт"], "answer_index": 2},
    {"question": "Сколько континентов на Земле?",
     "options": ["5", "6", "7", "8"], "answer_index": 2}
]

PRIZES = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]

# --- Функции звука ---
def play_sound(file):
    if os.path.exists(file):
        try:
            playsound(file)
        except Exception as e:
            print(f"Ошибка при воспроизведении звука: {e}")

# --- Сохранение и загрузка ---
def save_game(state, filename="save.json"):
    with open(filename, "w") as f:
        json.dump(state, f, indent=4)
    print("Игра сохранена!")

def load_game(filename="save.json"):
    if not os.path.exists(filename):
        print("Файл сохранения не найден. Начинаем новую игру.")
        return None
    try:
        with open(filename, "r") as f:
            state = json.load(f)
        print("Игра успешно загружена!")
        return state
    except Exception:
        print("Ошибка при загрузке файла. Начинаем новую игру.")
        return None

# --- Функции статистики ---
def save_stats(state):
    """Сохраняет статистику игры в файл stats.json."""
    stats_record = {
        "total_questions": len(state["questions"][:state["current_index"] + 1]),
        "correct_answers": state["correct_answers_count"],
        "final_score": state["score"]
    }

    filename = "stats.json"
    data = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(stats_record)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def show_stats():
    """Отображает статистику всех сыгранных игр."""
    filename = "stats.json"
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        print("Статистика пока пуста. Сыграйте хотя бы одну игру!")
        return

    with open(filename, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Ошибка чтения файла статистики.")
            return

    print("\n--- Статистика игр ---")
    for i, s in enumerate(data):
        total = s.get("total_questions", 0)
        correct = s.get("correct_answers", 0)
        final = s.get("final_score", 0)
        print(f"Игра #{i + 1}: задано вопросов — {total}, правильных — {correct}, выигрыш — {final}$")
    print("----------------------")


# --- Подсказки ---
def lifeline_50_50(state, question, display_options):
    if state["lifelines"]["50/50"]:
        correct_text = question["options"][question["answer_index"]]
        incorrect_options = [opt for opt in display_options if opt != correct_text]
        if incorrect_options:
            random_incorrect = random.choice(incorrect_options)
            display_options[:] = [correct_text, random_incorrect]
            random.shuffle(display_options)
        state["lifelines"]["50/50"] = False
        print("Варианты ответа обновлены (50/50).")
    else:
        print("Подсказка '50/50' уже использована.")

def lifeline_call_friend(state, question, display_options):
    if state["lifelines"]["звонок другу"]:
        print("Звонок другу...")
        correct_text = question["options"][question["answer_index"]]
        is_correct = random.choices([True, False], weights=[0.7,0.3])[0]
        if is_correct:
            answer = correct_text
        else:
            options = [opt for opt in display_options if opt != correct_text]
            answer = random.choice(options) if options else correct_text
        print(f"Друг считает, что правильный ответ: {answer}")
        state["lifelines"]["звонок другу"] = False
    else:
        print("Подсказка 'Звонок другу' уже использована.")

def lifeline_ask_audience(state, question, display_options):
    if state["lifelines"]["помощь зала"]:
        print("Помощь зала...")
        correct_text = question["options"][question["answer_index"]]
        total_votes = 100
        votes = {}
        correct_votes = random.randint(40,70)
        votes[correct_text] = correct_votes
        remaining = total_votes - correct_votes
        incorrect_options = [opt for opt in display_options if opt != correct_text]
        for i, opt in enumerate(incorrect_options):
            if i == len(incorrect_options)-1:
                votes[opt] = remaining
            else:
                v = random.randint(0, remaining)
                votes[opt] = v
                remaining -= v
        for opt in display_options:
            print(f"  {opt}: {votes.get(opt,0)}%")
        state["lifelines"]["помощь зала"] = False
    else:
        print("Подсказка 'Помощь зала' уже использована.")

# --- Вопрос ---
def display_question(state, question, number, display_options):
    print(f"\nВопрос {number} на {PRIZES[number-1]}$: {question['question']}")
    for i,opt in enumerate(display_options):
        print(f" {i+1}) {opt}")
    available = [k for k,v in state["lifelines"].items() if v]
    if available:
        print(f"Доступные подсказки: {', '.join(available)}")
    print("Для сохранения игры введите 'сохранить', для выхода 'выход'.")

def validate_answer(state, user_input, question, display_options):
    if user_input.lower() == "выход":
        return "quit"
    try:
        idx = int(user_input)-1
        if 0 <= idx < len(display_options):
            if display_options[idx] == question["options"][question["answer_index"]]:
                print("Правильно!")
                return True
            else:
                print(f"Неверно. Правильный ответ: {question['options'][question['answer_index']]}")
                return False
        else:
            print("Некорректный номер ответа.")
            return None
    except ValueError:
        return None

# --- Игровой цикл ---
def play(state=None):
    if state is None:
        state = {
            "score":0,
            "lifelines":{"50/50":True,"звонок другу":True,"помощь зала":True},
            "current_index":0,
            "questions":deepcopy(QUESTIONS),
            "correct_answers_count":0,
            "wrong_answers_count":0
        }
        random.shuffle(state["questions"])
    while state["current_index"] < len(state["questions"]):
        q = state["questions"][state["current_index"]]
        number = state["current_index"]+1
        display_options = deepcopy(q["options"])
        while True:
            display_question(state, q, number, display_options)
            choice = input("Ваш ответ: ").strip().lower()
            if choice == "сохранить":
                save_game(state)
                continue
            if choice in state["lifelines"] and state["lifelines"][choice]:
                if choice == "50/50": lifeline_50_50(state,q,display_options)
                elif choice == "звонок другу": lifeline_call_friend(state,q,display_options)
                elif choice == "помощь зала": lifeline_ask_audience(state,q,display_options)
                continue
            result = validate_answer(state, choice, q, display_options)
            if result is None: continue
            elif result == "quit":
                print(f"Вы вышли из игры. Текущий выигрыш: {state['score']}$")
                if input("Сохранить игру? (да/нет): ").lower()=="да":
                    save_game(state)
                save_stats(state)
                return
            elif result:
                play_sound("correct.mp3")
                state["score"]=PRIZES[state["current_index"]]
                state["correct_answers_count"]+=1
                state["current_index"]+=1
                break
            else:
                play_sound("wrong.mp3")
                state["wrong_answers_count"]+=1
                print(f"Игра окончена. Вы выиграли {state['score']}$")
                save_stats(state)
                return
    print(f"Поздравляем! Вы выиграли максимальную сумму: {state['score']}$!")
    save_stats(state)

# --- Главное меню ---
def main_menu():
    while True:
        print("\n--- Меню ---")
        print("1. Новая игра")
        print("2. Загрузить игру")
        print("3. Статистика")
        print("4. Выход")
        choice = input("Выберите опцию: ").strip()
        if choice=="1": play()
        elif choice=="2":
            state = load_game()
            if state: play(state)
        elif choice=="3": show_stats()
        elif choice=="4":
            print("Выход.")
            break
        else: print("Некорректный ввод.")

# --- Запуск ---
main_menu()
