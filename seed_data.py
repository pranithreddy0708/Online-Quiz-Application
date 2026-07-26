import sys
import os
from werkzeug.security import generate_password_hash

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from models import db
from models.user import User
from models.admin import Admin
from models.quiz import Category, Quiz
from models.question import Question
from models.result import Result

app = create_app()

def seed_database():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

        # Seed Admin if not exists or update credentials
        admin = Admin.query.first()
        if not admin:
            admin = Admin(username='pranith0708')
            admin.set_password('mrec2024')
            db.session.add(admin)
            print("Default admin created (username: pranith0708, password: mrec2024)")
        else:
            admin.username = 'pranith0708'
            admin.set_password('mrec2024')
            print("Admin credentials updated to username: pranith0708, password: mrec2024")



        # Seed Sample User if not exists
        if not User.query.filter_by(email='john@example.com').first():
            user = User(full_name='John Doe', email='john@example.com')
            user.set_password('user123')
            db.session.add(user)
            print("Default user created (email: john@example.com, password: user123)")

        db.session.commit()

        # Seed Categories
        categories_data = ['Programming', 'Web Development', 'Database', 'Aptitude & Logic']
        cat_map = {}
        for cat_name in categories_data:
            cat = Category.query.filter_by(category_name=cat_name).first()
            if not cat:
                cat = Category(category_name=cat_name)
                db.session.add(cat)
                db.session.flush()
            cat_map[cat_name] = cat.category_id

        db.session.commit()

        # Seed 5 Quizzes with 10 questions each
        quizzes_seed = [
            {
                "title": "Python Basics",
                "category": "Programming",
                "description": "Test your fundamental knowledge of Python data types, loops, functions, and standard library.",
                "time_limit": 10,
                "questions": [
                    {
                        "q": "What is the correct file extension for Python files?",
                        "a": ".pyt", "b": ".python", "c": ".py", "d": ".pt",
                        "correct": "C"
                    },
                    {
                        "q": "Which keyword is used to define a function in Python?",
                        "a": "func", "b": "def", "c": "function", "d": "define",
                        "correct": "B"
                    },
                    {
                        "q": "How do you insert COMMENTS in Python code?",
                        "a": "// This is a comment", "b": "/* This is a comment */", "c": "# This is a comment", "d": "<!-- This is a comment -->",
                        "correct": "C"
                    },
                    {
                        "q": "Which data structure is immutable in Python?",
                        "a": "List", "b": "Dictionary", "c": "Set", "d": "Tuple",
                        "correct": "D"
                    },
                    {
                        "q": "What will `type([])` return in Python?",
                        "a": "<class 'tuple'>", "b": "<class 'dict'>", "c": "<class 'list'>", "d": "<class 'array'>",
                        "correct": "C"
                    },
                    {
                        "q": "Which operator is used for exponentiation (power) in Python?",
                        "a": "^", "b": "**", "c": "^^", "d": "//",
                        "correct": "B"
                    },
                    {
                        "q": "What is the output of `len('Hello World')`?",
                        "a": "10", "b": "11", "c": "12", "d": "9",
                        "correct": "B"
                    },
                    {
                        "q": "Which built-in module in Python is used to generate random numbers?",
                        "a": "math", "b": "random", "c": "rand", "d": "generate",
                        "correct": "B"
                    },
                    {
                        "q": "What is the correct syntax to print a message in Python 3?",
                        "a": "echo 'Hello'", "b": "print('Hello')", "c": "System.out.println('Hello')", "d": "console.log('Hello')",
                        "correct": "B"
                    },
                    {
                        "q": "How do you create a variable with the floating number 2.8 in Python?",
                        "a": "x = float(2.8)", "b": "x = 2.8", "c": "Both A and B are correct", "d": "float x = 2.8",
                        "correct": "C"
                    }
                ]
            },
            {
                "title": "HTML & CSS",
                "category": "Web Development",
                "description": "Evaluate your understanding of HTML5 semantics, CSS grid, flexbox, and web styling principles.",
                "time_limit": 10,
                "questions": [
                    {
                        "q": "What does HTML stand for?",
                        "a": "Hyper Text Markup Language", "b": "High Text Machine Language", "c": "Hyperlink Text Management Language", "d": "Home Tool Markup Language",
                        "correct": "A"
                    },
                    {
                        "q": "Which HTML5 tag is used to define an independent self-contained article?",
                        "a": "<section>", "b": "<article>", "c": "<div>", "d": "<main>",
                        "correct": "B"
                    },
                    {
                        "q": "Which CSS property is used to change the background color of an element?",
                        "a": "color", "b": "bgcolor", "c": "background-color", "d": "canvas-color",
                        "correct": "C"
                    },
                    {
                        "q": "How do you select an element with id 'header' in CSS?",
                        "a": ".header", "b": "#header", "c": "header", "d": "*header",
                        "correct": "B"
                    },
                    {
                        "q": "What is the default value of the `position` property in CSS?",
                        "a": "relative", "b": "absolute", "c": "fixed", "d": "static",
                        "correct": "D"
                    },
                    {
                        "q": "Which CSS Flexbox property aligns items along the cross axis?",
                        "a": "justify-content", "b": "align-items", "c": "flex-direction", "d": "align-content",
                        "correct": "B"
                    },
                    {
                        "q": "Which HTML tag is used to embed an image?",
                        "a": "<img>", "b": "<image>", "c": "<pic>", "d": "<media>",
                        "correct": "A"
                    },
                    {
                        "q": "Which HTML attribute specifies an alternate text for an image if the image cannot be displayed?",
                        "a": "title", "b": "src", "c": "alt", "d": "longdesc",
                        "correct": "C"
                    },
                    {
                        "q": "How can you make a numbered list in HTML?",
                        "a": "<ul>", "b": "<dl>", "c": "<list>", "d": "<ol>",
                        "correct": "D"
                    },
                    {
                        "q": "What does CSS stand for?",
                        "a": "Cascading Style Sheets", "b": "Creative Style Sheets", "c": "Computer Style System", "d": "Colorful Style Sheets",
                        "correct": "A"
                    }
                ]
            },
            {
                "title": "JavaScript",
                "category": "Web Development",
                "description": "Master ES6+ JavaScript concepts including async/await, closures, DOM manipulation, and promises.",
                "time_limit": 10,
                "questions": [
                    {
                        "q": "Which keyword is used to declare a block-scoped variable in JavaScript?",
                        "a": "var", "b": "let", "c": "dim", "d": "set",
                        "correct": "B"
                    },
                    {
                        "q": "What will `typeof NaN` evaluate to in JavaScript?",
                        "a": "'number'", "b": "'NaN'", "c": "'undefined'", "d": "'object'",
                        "correct": "A"
                    },
                    {
                        "q": "Which method converts a JSON string into a JavaScript object?",
                        "a": "JSON.stringify()", "b": "JSON.parse()", "c": "JSON.toObject()", "d": "JSON.convert()",
                        "correct": "B"
                    },
                    {
                        "q": "What is the output of `0 == '0'` in JavaScript?",
                        "a": "true", "b": "false", "c": "TypeError", "d": "undefined",
                        "correct": "A"
                    },
                    {
                        "q": "What is the output of `0 === '0'` in JavaScript?",
                        "a": "true", "b": "false", "c": "TypeError", "d": "undefined",
                        "correct": "B"
                    },
                    {
                        "q": "Which method is used to add new items to the end of an Array?",
                        "a": "push()", "b": "pop()", "c": "unshift()", "d": "append()",
                        "correct": "A"
                    },
                    {
                        "q": "How do you write an arrow function in JavaScript?",
                        "a": "const fn = () => {}", "b": "const fn = function() {}", "c": "function => fn() {}", "d": "def fn():",
                        "correct": "A"
                    },
                    {
                        "q": "Which object represents an eventual completion or failure of an asynchronous operation?",
                        "a": "Callback", "b": "Promise", "c": "AsyncToken", "d": "EventListener",
                        "correct": "B"
                    },
                    {
                        "q": "How do you select an HTML element by ID in JavaScript?",
                        "a": "document.getElement(id)", "b": "document.getElementById(id)", "c": "document.queryId(id)", "d": "window.findId(id)",
                        "correct": "B"
                    },
                    {
                        "q": "Which event occurs when the user clicks on an HTML element?",
                        "a": "onchange", "b": "onmouseover", "c": "onclick", "d": "onkeydown",
                        "correct": "C"
                    }
                ]
            },
            {
                "title": "SQL",
                "category": "Database",
                "description": "Test your relational database queries, JOINs, aggregation functions, and DDL/DML statements.",
                "time_limit": 10,
                "questions": [
                    {
                        "q": "What does SQL stand for?",
                        "a": "Structured Query Language", "b": "Simple Query Logic", "c": "Sequential Query List", "d": "Standard Question Language",
                        "correct": "A"
                    },
                    {
                        "q": "Which SQL clause is used to filter records matching specified criteria?",
                        "a": "GROUP BY", "b": "ORDER BY", "c": "WHERE", "d": "HAVING",
                        "correct": "C"
                    },
                    {
                        "q": "Which command is used to retrieve data from a database in SQL?",
                        "a": "GET", "b": "FETCH", "c": "EXTRACT", "d": "SELECT",
                        "correct": "D"
                    },
                    {
                        "q": "Which SQL statement is used to insert new data into a database table?",
                        "a": "ADD RECORD", "b": "INSERT INTO", "c": "UPDATE", "d": "CREATE ROW",
                        "correct": "B"
                    },
                    {
                        "q": "Which JOIN type returns all rows from the left table and matched rows from the right table?",
                        "a": "INNER JOIN", "b": "RIGHT JOIN", "c": "LEFT JOIN", "d": "FULL JOIN",
                        "correct": "C"
                    },
                    {
                        "q": "Which Aggregate function in SQL counts the number of rows?",
                        "a": "SUM()", "b": "COUNT()", "c": "TOTAL()", "d": "ROW_COUNT()",
                        "correct": "B"
                    },
                    {
                        "q": "How do you delete a database table structure permanently in SQL?",
                        "a": "REMOVE TABLE", "b": "DELETE TABLE", "c": "DROP TABLE", "d": "TRUNCATE TABLE",
                        "correct": "C"
                    },
                    {
                        "q": "Which keyword is used to sort the result set in ascending or descending order?",
                        "a": "SORT BY", "b": "ORDER BY", "c": "GROUP BY", "d": "ALIGN BY",
                        "correct": "B"
                    },
                    {
                        "q": "Which SQL constraint uniquely identifies each record in a table?",
                        "a": "FOREIGN KEY", "b": "CHECK", "c": "NOT NULL", "d": "PRIMARY KEY",
                        "correct": "D"
                    },
                    {
                        "q": "Which clause is used with aggregate functions to filter groups of records?",
                        "a": "WHERE", "b": "HAVING", "c": "GROUP FILTER", "d": "LIKE",
                        "correct": "B"
                    }
                ]
            },
            {
                "title": "General Aptitude",
                "category": "Aptitude & Logic",
                "description": "Assess logical reasoning, quantitative problem solving, and analytical skills.",
                "time_limit": 10,
                "questions": [
                    {
                        "q": "What comes next in the sequence: 2, 6, 12, 20, 30, ...?",
                        "a": "36", "b": "40", "c": "42", "d": "48",
                        "correct": "C"
                    },
                    {
                        "q": "If a car travels 120 km in 2 hours, what is its average speed in meters per second?",
                        "a": "16.67 m/s", "b": "30 m/s", "c": "60 m/s", "d": "25 m/s",
                        "correct": "A"
                    },
                    {
                        "q": "A father is 4 times as old as his son. In 20 years, he will be twice as old as his son. How old is the son now?",
                        "a": "5 years", "b": "10 years", "c": "15 years", "d": "20 years",
                        "correct": "B"
                    },
                    {
                        "q": "Which letter comes next in the series: A, C, F, J, O, ...?",
                        "a": "S", "b": "T", "c": "U", "d": "V",
                        "correct": "C"
                    },
                    {
                        "q": "What is 15% of 240?",
                        "a": "30", "b": "34", "c": "36", "d": "40",
                        "correct": "C"
                    },
                    {
                        "q": "If 6 men can complete a work in 12 days, how many days will 8 men take to complete the same work?",
                        "a": "9 days", "b": "8 days", "c": "10 days", "d": "6 days",
                        "correct": "A"
                    },
                    {
                        "q": "Which fraction is the largest: 3/4, 5/6, 7/9, or 4/5?",
                        "a": "3/4", "b": "5/6", "c": "7/9", "d": "4/5",
                        "correct": "B"
                    },
                    {
                        "q": "Find the odd one out: Apple, Banana, Mango, Potato, Grape.",
                        "a": "Banana", "b": "Mango", "c": "Potato", "d": "Grape",
                        "correct": "C"
                    },
                    {
                        "q": "If 'CODES' is written as 'DPEFT' in a code language, how is 'LOGIC' written?",
                        "a": "MPHJD", "b": "MPHID", "c": "NQIJD", "d": "KNFHB",
                        "correct": "A"
                    },
                    {
                        "q": "What is the probability of getting an even number when throwing a fair 6-sided die?",
                        "a": "1/6", "b": "1/3", "c": "1/2", "d": "2/3",
                        "correct": "C"
                    }
                ]
            }
        ]

        for qdata in quizzes_seed:
            cat_id = cat_map[qdata["category"]]
            quiz = Quiz.query.filter_by(quiz_title=qdata["title"]).first()
            if not quiz:
                quiz = Quiz(
                    category_id=cat_id,
                    quiz_title=qdata["title"],
                    description=qdata["description"],
                    time_limit=qdata["time_limit"],
                    total_questions=len(qdata["questions"])
                )
                db.session.add(quiz)
                db.session.flush()

                for item in qdata["questions"]:
                    question = Question(
                        quiz_id=quiz.quiz_id,
                        question=item["q"],
                        option_a=item["a"],
                        option_b=item["b"],
                        option_c=item["c"],
                        option_d=item["d"],
                        correct_answer=item["correct"]
                    )
                    db.session.add(question)
                print(f"Added Quiz '{qdata['title']}' with {len(qdata['questions'])} questions.")

        db.session.commit()
        print("Database seed completed successfully!")

if __name__ == '__main__':
    seed_database()
