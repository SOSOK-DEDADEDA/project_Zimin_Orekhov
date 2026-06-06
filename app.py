# app.py 
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import json
import os
import hashlib
import re
from functools import wraps
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from advanced_chatbot import chatbot
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-this-in-production'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Базовый путь к папке проекта
BASE_DIR = Path(__file__).parent.absolute()

# Файлы для хранения данных
USERS_FILE = BASE_DIR / 'users.json'
RESULTS_FILE = BASE_DIR / 'results.json'
LESSONS_FILE = BASE_DIR / 'lessons_data.json'
DIFFICULTIES_FILE = BASE_DIR / 'difficulties.json'

# Инициализация чат-бота
chatbot_instance = None

def get_chatbot():
    """Ленивая инициализация продвинутого мультиязычного чат-бота"""
    global chatbot_instance
    if chatbot_instance is None:
        try:
            print(" Инициализация продвинутого мультиязычного чат-бота...")
            chatbot_instance = chatbot
            chatbot_instance.init()
            stats = chatbot_instance.get_analytics()
            print(f"✅ Чат-бот успешно инициализирован!")
            # Исправленные ключи для новой версии бота
            if 'total_questions_ru' in stats:
                print(f"    Русских вопросов: {stats['total_questions_ru']}")
            else:
                print(f"    База знаний: {stats.get('total_questions_ru', stats.get('total_queries', 0))} вариантов")
            if 'vocabulary_size_ru' in stats:
                print(f"   📖 Словарь RU: {stats['vocabulary_size_ru']} слов")
        except Exception as e:
            print(f"❌ Ошибка инициализации чат-бота: {e}")
            import traceback
            traceback.print_exc()
            chatbot_instance = None
    return chatbot_instance

# Декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Пожалуйста, войдите в систему', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Функция для хеширования паролей
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password(password):
    if len(password) < 8:
        return False, "Пароль должен содержать минимум 8 символов"
    if not re.search(r"[A-Z]", password):
        return False, "Пароль должен содержать хотя бы одну заглавную букву"
    if not re.search(r"[a-z]", password):
        return False, "Пароль должен содержать хотя бы одну строчную букву"
    if not re.search(r"\d", password):
        return False, "Пароль должен содержать хотя бы одну цифру"
    return True, "Пароль надежный"

def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False, "Имя пользователя должно быть от 3 до 20 символов"
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", username):
        return False, "Имя пользователя должно начинаться с буквы и содержать только буквы, цифры и _"
    return True, "Имя пользователя допустимо"

def load_users():
    try:
        if USERS_FILE.exists():
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Ошибка загрузки пользователей: {e}")
        return {}

def save_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения пользователей: {e}")

def load_lessons():
    try:
        if LESSONS_FILE.exists():
            with open(LESSONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            default_lessons = {
                "1": {
                    "title": "Введение в Godot и установка",
                    "content": "В этом уроке мы познакомимся с движком Godot и установим его на ваш компьютер. Рассмотрим интерфейс и основные понятия.",
                    "iframe_url": "/static/files/lesson_1",
                    "additional_files": [],
                    "quiz": {
                        "questions": [
                            "Какой язык программирования используется в Godot?",
                            "Какая последняя стабильная версия Godot?",
                            "Godot это бесплатный движок?"
                        ],
                        "correct": ["GDScript", "4.x", "Да"]
                    }
                },
                "2": {
                    "title": "Создание первого проекта",
                    "content": "Создадим наш первый проект и настроим сцену для платформера. Изучим основные узлы и сцены.",
                    "iframe_url": "/static/files/lesson_2",
                    "additional_files": [],
                    "quiz": {
                        "questions": [
                            "Какой тип проекта нужно выбрать для 2D игры?",
                            "Как называется основной узел для платформера?",
                            "В каком формате сохраняются сцены?"
                        ],
                        "correct": ["2D", "CharacterBody2D", ".tscn"]
                    }
                },
                "3": {
                    "title": "Спрайты и анимация персонажа",
                    "content": "Добавим спрайты и создадим анимации для нашего персонажа. Настроим спрайты и анимации.",
                    "iframe_url": "/static/files/lesson_3",
                    "additional_files": [],
                    "quiz": {
                        "questions": [
                            "Какой узел используется для анимации?",
                            "Сколько кадров в секунду обычно используют для 2D анимации?",
                            "Какой узел отвечает за отображение текстуры?"
                        ],
                        "correct": ["AnimationPlayer", "12", "Sprite2D"]
                    }
                }
            }
            with open(LESSONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_lessons, f, ensure_ascii=False, indent=2)
            return default_lessons
    except Exception as e:
        print(f"Ошибка загрузки уроков: {e}")
        return {}

def save_quiz_results(username, lesson_id, score):
    try:
        results = {}
        if RESULTS_FILE.exists():
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                results = json.load(f)
        
        if username not in results:
            results[username] = {}
        
        results[username][str(lesson_id)] = {
            'score': score,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения результатов: {e}")

def load_quiz_results(username):
    try:
        if RESULTS_FILE.exists():
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                results = json.load(f)
                user_results = results.get(username, {})
                formatted_results = {}
                for lesson_id, data in user_results.items():
                    if isinstance(data, dict):
                        formatted_results[lesson_id] = data['score']
                    else:
                        formatted_results[lesson_id] = data
                return formatted_results
    except Exception as e:
        print(f"Ошибка загрузки результатов: {e}")
    return {}

def load_difficulties():
    try:
        if DIFFICULTIES_FILE.exists():
            with open(DIFFICULTIES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Ошибка загрузки трудностей: {e}")
        return {}

def save_difficulty(username, lesson_id, difficult_parts):
    try:
        difficulties = load_difficulties()
        
        if str(lesson_id) not in difficulties:
            difficulties[str(lesson_id)] = {}
        
        difficulties[str(lesson_id)][username] = {
            'difficult_parts': difficult_parts,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(DIFFICULTIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(difficulties, f, ensure_ascii=False, indent=2)
            
        return True
    except Exception as e:
        print(f"Ошибка сохранения трудностей: {e}")
        return False

def get_difficulty_stats(lesson_id):
    try:
        difficulties = load_difficulties()
        lesson_stats = difficulties.get(str(lesson_id), {})
        
        if not lesson_stats:
            return {
                'total_responses': 0,
                'parts_stats': {},
                'percentages': {}
            }
        
        total_responses = len(lesson_stats)
        parts_stats = defaultdict(int)
        for user_data in lesson_stats.values():
            for part in user_data.get('difficult_parts', []):
                parts_stats[part] += 1
        
        percentages = {}
        for part, count in parts_stats.items():
            percentages[part] = round((count / total_responses) * 100, 1)
        
        return {
            'total_responses': total_responses,
            'parts_stats': dict(parts_stats),
            'percentages': percentages
        }
    except Exception as e:
        print(f"Ошибка получения статистики: {e}")
        return {'total_responses': 0, 'parts_stats': {}, 'percentages': {}}

# ОСНОВНЫЕ МАРШРУТЫ 

@app.route('/')
def index():
    lessons = load_lessons()
    user_results = {}
    if 'username' in session:
        user_results = load_quiz_results(session['username'])
    return render_template('index.html', lessons=lessons, user_results=user_results)

@app.route('/lesson/<int:lesson_id>')
@login_required
def lesson(lesson_id):
    lessons = load_lessons()
    if str(lesson_id) in lessons:
        lesson_data = lessons[str(lesson_id)]
        user_results = load_quiz_results(session['username'])
        difficulty_stats = get_difficulty_stats(lesson_id)
        
        user_difficulties = None
        difficulties = load_difficulties()
        if str(lesson_id) in difficulties and session['username'] in difficulties[str(lesson_id)]:
            user_difficulties = difficulties[str(lesson_id)][session['username']]
        
        return render_template('lesson.html', 
                             lesson=lesson_data, 
                             lesson_id=lesson_id,
                             user_results=user_results,
                             difficulty_stats=difficulty_stats,
                             user_difficulties=user_difficulties)
    flash('Урок не найден', 'error')
    return redirect(url_for('index'))

@app.route('/submit_quiz/<int:lesson_id>', methods=['POST'])
@login_required
def submit_quiz(lesson_id):
    data = request.json
    answers = data.get('answers', [])
    
    lessons = load_lessons()
    if str(lesson_id) not in lessons:
        return jsonify({'error': 'Урок не найден'}), 404
        
    correct_answers = lessons[str(lesson_id)]['quiz']['correct']
    
    correct_count = 0
    for i, answer in enumerate(answers):
        if i < len(correct_answers):
            if answer.lower().strip() == correct_answers[i].lower().strip():
                correct_count += 1
    
    percentage = (correct_count / len(correct_answers)) * 100 if correct_answers else 0
    
    save_quiz_results(session['username'], lesson_id, percentage)
    
    return jsonify({
        'percentage': round(percentage, 1),
        'correct': correct_count,
        'total': len(correct_answers)
    })

@app.route('/submit_difficulties/<int:lesson_id>', methods=['POST'])
@login_required
def submit_difficulties(lesson_id):
    data = request.json
    difficult_parts = data.get('difficult_parts', [])
    
    success = save_difficulty(session['username'], lesson_id, difficult_parts)
    
    if success:
        stats = get_difficulty_stats(lesson_id)
        return jsonify({
            'success': True,
            'message': 'Спасибо за обратную связь!',
            'stats': stats
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Ошибка при сохранении'
        }), 500

@app.route('/get_difficulty_stats/<int:lesson_id>')
def get_difficulty_stats_route(lesson_id):
    stats = get_difficulty_stats(lesson_id)
    return jsonify(stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('login_username', '').strip()
        password = request.form.get('login_password', '')
        
        if not username or not password:
            flash('Заполните все поля', 'error')
            return render_template('login.html')
        
        users = load_users()
        
        if username in users and users[username]['password'] == hash_password(password):
            session['username'] = username
            session['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            flash(f'Добро пожаловать, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not username or not password or not confirm_password:
            flash('Заполните все поля', 'error')
            return render_template('login.html', register=True)
        
        is_valid_username, username_message = validate_username(username)
        if not is_valid_username:
            flash(username_message, 'error')
            return render_template('login.html', register=True)
        
        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return render_template('login.html', register=True)
        
        is_valid_password, password_message = validate_password(password)
        if not is_valid_password:
            flash(password_message, 'error')
            return render_template('login.html', register=True)
        
        users = load_users()
        
        if username in users:
            flash('Имя пользователя уже занято', 'error')
            return render_template('login.html', register=True)
        
        users[username] = {
            'password': hash_password(password),
            'registered_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_login': None
        }
        
        save_users(users)
        session['username'] = username
        flash(f'Регистрация успешна! Добро пожаловать, {username}!', 'success')
        return redirect(url_for('index'))
    
    return render_template('login.html', register=True)

@app.route('/logout')
def logout():
    username = session.get('username')
    session.clear()
    if username:
        flash(f'До свидания, {username}!', 'info')
    return redirect(url_for('index'))

@app.route('/check_username')
def check_username():
    username = request.args.get('username', '').strip()
    
    if not username:
        return jsonify({'available': False, 'message': 'Введите имя пользователя'})
    
    is_valid, message = validate_username(username)
    if not is_valid:
        return jsonify({'available': False, 'message': message})
    
    users = load_users()
    if username in users:
        return jsonify({'available': False, 'message': 'Имя пользователя уже занято'})
    
    return jsonify({'available': True, 'message': 'Имя пользователя доступно'})

# МАРШРУТЫ ДЛЯ ПРОДВИНУТОГО ЧАТ-БОТА 

@app.route('/api/chatbot/ask', methods=['POST'])
def chatbot_ask():
    """API для вопросов к чат-боту с поддержкой контекста и мультиязычности"""
    try:
        data = request.json
        question = data.get('question', '').strip()
        session_id = data.get('session_id', session.get('username', 'anonymous'))
        
        if not question:
            return jsonify({'error': 'Введите вопрос'}), 400
        
        bot = get_chatbot()
        if bot is None:
            return jsonify({
                'answer': 'Извините, чат-бот временно недоступен. Попробуйте позже.',
                'confidence': 0,
                'found': False,
                'suggestions': ["Как зарегистрироваться?", "How to register?"]
            }), 200
        
        # Получаем ответ с учетом контекста
        if session.get('username'):
            response = bot.predict_with_context(question, session_id)
        else:
            response = bot.predict(question)
        
        # Определяем язык ответа
        language = bot.detect_language(question)
        
        # Сохраняем историю
        try:
            history_file = BASE_DIR / 'chatbot_history.json'
            history = {}
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            if 'questions' not in history:
                history['questions'] = []
            
            history['questions'].append({
                'question': question,
                'answer': response.get('answer', '')[:200],
                'confidence': float(response.get('confidence', 0)),
                'found': bool(response.get('found', False)),
                'category': str(response.get('category', '')),
                'language': language,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'user': session.get('username', 'anonymous')
            })
            
            # Оставляем последние 500 вопросов
            history['questions'] = history['questions'][-500:]
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")
        
        # Получаем персонализированные предложения
        suggestions = []
        if not response.get('found', False):
            suggestions = bot.get_category_suggestions(session_id, language)
        elif 'suggestions' in response:
            suggestions = response['suggestions']
        
        return jsonify({
            'answer': response.get('answer', 'Извините, ответ не найден'),
            'confidence': float(response.get('confidence', 0)),
            'found': bool(response.get('found', False)),
            'category': str(response.get('category', '')),
            'suggestions': suggestions,
            'language': language
        })
        
    except Exception as e:
        print(f"Ошибка в chatbot_ask: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'answer': 'Извините, произошла техническая ошибка. Пожалуйста, попробуйте позже.',
            'confidence': 0,
            'found': False,
            'suggestions': ["Как зарегистрироваться?", "How to register?"]
        }), 200

@app.route('/api/chatbot/suggestions', methods=['GET'])
def chatbot_suggestions():
    """Получение персонализированных предложений"""
    try:
        session_id = session.get('username', 'anonymous')
        language = request.args.get('lang', 'ru')
        bot = get_chatbot()
        
        if bot:
            suggestions = bot.get_category_suggestions(session_id, language)
        else:
            if language == 'ru':
                suggestions = ["Как зарегистрироваться?", "Как начать обучение?", "Сколько всего уроков?"]
            else:
                suggestions = ["How to register?", "How to start learning?", "How many lessons?"]
        
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        print(f"Ошибка в chatbot_suggestions: {e}")
        return jsonify({'suggestions': ["Как зарегистрироваться?", "How to register?"]})

@app.route('/api/chatbot/feedback', methods=['POST'])
def chatbot_feedback():
    """Сохранение отзыва о качестве ответа"""
    try:
        data = request.json
        question = data.get('question', '')
        helpful = data.get('helpful', False)
        
        feedback_file = BASE_DIR / 'chatbot_feedback.json'
        feedback = {}
        
        if feedback_file.exists():
            with open(feedback_file, 'r', encoding='utf-8') as f:
                feedback = json.load(f)
        
        if 'entries' not in feedback:
            feedback['entries'] = []
        
        feedback['entries'].append({
            'question': question,
            'helpful': helpful,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user': session.get('username', 'anonymous')
        })
        
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback, f, ensure_ascii=False, indent=2)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Ошибка в chatbot_feedback: {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/api/chatbot/stats', methods=['GET'])
@login_required
def chatbot_stats():
    """Статистика чат-бота (только для админа)"""
    if session.get('username') != 'admin':
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    try:
        bot = get_chatbot()
        if bot:
            stats = bot.get_analytics()
        else:
            stats = {
                'total_questions': 0,
                'russian_questions': 0,
                'english_questions': 0,
                'categories': 0,
                'total_queries': 0,
                'success_rate': 0,
                'model_loaded': False
            }
        
        # Добавляем историю из файла
        history_file = BASE_DIR / 'chatbot_history.json'
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                stats['total_queries_history'] = len(history.get('questions', []))
        
        return jsonify(stats)
    except Exception as e:
        print(f"Ошибка в chatbot_stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot/stats/detailed', methods=['GET'])
@login_required
def chatbot_detailed_stats():
    """Детальная статистика чат-бота (только для админа)"""
    if session.get('username') != 'admin':
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    try:
        bot = get_chatbot()
        if bot:
            stats = bot.get_analytics()
            
            # Добавляем пользовательскую статистику
            if hasattr(bot, 'user_profiles'):
                stats['user_stats'] = []
                for user_id, profile in list(bot.user_profiles.items())[:20]:
                    stats['user_stats'].append(bot.get_user_stats(user_id))
            
            # Добавляем информацию о кэше
            stats['cache_info'] = {
                'size': len(bot.cache),
                'max_size': bot.cache_size,
                'hit_rate': round(bot.stats.get('cache_hits', 0) / max(1, bot.stats.get('total_queries', 1)) * 100, 1)
            }
        
        return jsonify(stats)
    except Exception as e:
        print(f"Ошибка в chatbot_detailed_stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot/add_faq', methods=['POST'])
@login_required
def chatbot_add_faq():
    """Добавление нового FAQ (только для админа)"""
    if session.get('username') != 'admin':
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    try:
        data = request.json
        question = data.get('question')
        answer = data.get('answer')
        category = data.get('category', 'general')
        language = data.get('language', 'ru')
        
        if not question or not answer:
            return jsonify({'error': 'Вопрос и ответ обязательны'}), 400
        
        bot = get_chatbot()
        bot.add_question_answer(question, answer, category, language)
        
        return jsonify({'status': 'success', 'message': 'FAQ успешно добавлен'})
    except Exception as e:
        print(f"Ошибка в chatbot_add_faq: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot/clear_cache', methods=['POST'])
@login_required
def chatbot_clear_cache():
    """Очистка кэша чат-бота (только для админа)"""
    if session.get('username') != 'admin':
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    try:
        bot = get_chatbot()
        bot.clear_cache()
        return jsonify({'status': 'success', 'message': 'Кэш успешно очищен'})
    except Exception as e:
        print(f"Ошибка в chatbot_clear_cache: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot/language', methods=['POST'])
def chatbot_set_language():
    """Установка предпочтительного языка пользователя"""
    try:
        data = request.json
        language = data.get('language', 'ru')
        session_id = session.get('username', 'anonymous')
        
        bot = get_chatbot()
        if bot and hasattr(bot, 'user_profiles') and session_id in bot.user_profiles:
            from advanced_chatbot import Language
            bot.user_profiles[session_id].preferred_language = Language(language)
        
        return jsonify({'status': 'success', 'language': language})
    except Exception as e:
        print(f"Ошибка в chatbot_set_language: {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/admin/chatbot')
@login_required
def admin_chatbot():
    """Админ-панель управления чат-ботом"""
    if session.get('username') != 'admin':
        flash('Доступ запрещен', 'error')
        return redirect(url_for('index'))
    return render_template('admin_chatbot.html')


if __name__ == '__main__':
    print(f"Проект запущен из: {BASE_DIR}")
    
    # Создаем необходимые файлы
    for file in [USERS_FILE, RESULTS_FILE, DIFFICULTIES_FILE]:
        if not file.exists():
            with open(file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            print(f"✅ Создан файл: {file.name}")
    
    if not LESSONS_FILE.exists():
        load_lessons()
        print(f"✅ Создан файл уроков: {LESSONS_FILE.name}")
    
    # Создаем папку для файлов
    static_files_dir = BASE_DIR / 'static' / 'files'
    static_files_dir.mkdir(parents=True, exist_ok=True)
    
    # Создаем тестового пользователя
    users = load_users()
    if "admin" not in users:
        users["admin"] = {
            'password': hash_password("Admin123"),
            'registered_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_login': None
        }
        save_users(users)
        print("✅ Создан тестовый пользователь: admin / Admin123")
    
    print("\n" + "="*60)
    print(" СЕРВЕР УСПЕШНО ЗАПУЩЕН!")
    print("="*60)
    print(f"🌐 Адрес: http://127.0.0.1:5000")
    print(f" Тестовый пользователь: admin")
    print(f" Пароль: Admin123")
    print("\n ЧАТ-БОТ ДОСТУПЕН НА ВСЕХ СТРАНИЦАХ!")
    print("   Поддерживает русский и английский языки")
    print("   Понимает контекст диалога")
    print("   Запоминает интересы пользователя")
    print("\n Админ-панель чат-бота:")
    print(f"   http://127.0.0.1:5000/admin/chatbot")
    print("\n Статистика доступна в админ-панели")
    print("="*60)
    print("\n💡 Для остановки сервера нажмите Ctrl+C\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
