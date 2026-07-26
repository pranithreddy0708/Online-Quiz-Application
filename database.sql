-- ========================================================
-- ONLINE QUIZ APPLICATION - MYSQL DATABASE SCHEMA & SEED DATA
-- ========================================================

CREATE DATABASE IF NOT EXISTS online_quiz_db;
USE online_quiz_db;

-- --------------------------------------------------------
-- Table structure for table `users`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `results`;
DROP TABLE IF EXISTS `questions`;
DROP TABLE IF EXISTS `quizzes`;
DROP TABLE IF EXISTS `categories`;
DROP TABLE IF EXISTS `admins`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` INT AUTO_INCREMENT PRIMARY KEY,
  `full_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(120) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table structure for table `admins`
-- --------------------------------------------------------
CREATE TABLE `admins` (
  `admin_id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(80) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table structure for table `categories`
-- --------------------------------------------------------
CREATE TABLE `categories` (
  `category_id` INT AUTO_INCREMENT PRIMARY KEY,
  `category_name` VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table structure for table `quizzes`
-- --------------------------------------------------------
CREATE TABLE `quizzes` (
  `quiz_id` INT AUTO_INCREMENT PRIMARY KEY,
  `category_id` INT NOT NULL,
  `quiz_title` VARCHAR(150) NOT NULL,
  `description` TEXT,
  `time_limit` INT NOT NULL DEFAULT 10,
  `total_questions` INT NOT NULL DEFAULT 10,
  FOREIGN KEY (`category_id`) REFERENCES `categories`(`category_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table structure for table `questions`
-- --------------------------------------------------------
CREATE TABLE `questions` (
  `question_id` INT AUTO_INCREMENT PRIMARY KEY,
  `quiz_id` INT NOT NULL,
  `question` TEXT NOT NULL,
  `option_a` VARCHAR(255) NOT NULL,
  `option_b` VARCHAR(255) NOT NULL,
  `option_c` VARCHAR(255) NOT NULL,
  `option_d` VARCHAR(255) NOT NULL,
  `correct_answer` VARCHAR(1) NOT NULL,
  FOREIGN KEY (`quiz_id`) REFERENCES `quizzes`(`quiz_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table structure for table `results`
-- --------------------------------------------------------
CREATE TABLE `results` (
  `result_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `quiz_id` INT NOT NULL,
  `score` INT NOT NULL,
  `total_marks` INT NOT NULL,
  `percentage` FLOAT NOT NULL,
  `completed_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`quiz_id`) REFERENCES `quizzes`(`quiz_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========================================================
-- SEED DATA INSERTIONS
-- ========================================================

-- Default Admin (username: pranith0708, password: mrec2024)
INSERT INTO `admins` (`admin_id`, `username`, `password`) VALUES
(1, 'pranith0708', 'scrypt:32768:8:1$85XORyxEzH4oJn2V$0905aa131cbd0f346c2907b94473ee9a81bb44b549340323672495746d22b319794e85a859038a9fc70a01a78d80e63debd756d15945a8d4acc6f0f98db6ee23')
ON DUPLICATE KEY UPDATE `username`='pranith0708', `password`='scrypt:32768:8:1$85XORyxEzH4oJn2V$0905aa131cbd0f346c2907b94473ee9a81bb44b549340323672495746d22b319794e85a859038a9fc70a01a78d80e63debd756d15945a8d4acc6f0f98db6ee23';


-- Default User (john@example.com, password: user123)
INSERT INTO `users` (`user_id`, `full_name`, `email`, `password`) VALUES
(1, 'John Doe', 'john@example.com', 'scrypt:32768:8:1$fai5UBW06K2Fg6GB$4688cbaecd6e095e3af5c083d0f834180f400c82d220b6bf455cd83e07a51711a6651c7c448678ffde709d8528fc9200d86e54c3d531aaa8abcefc2004e80547')
ON DUPLICATE KEY UPDATE `email`=`email`;


-- Categories
INSERT INTO `categories` (`category_id`, `category_name`) VALUES
(1, 'Programming'),
(2, 'Web Development'),
(3, 'Database'),
(4, 'Aptitude & Logic');

-- Quizzes
INSERT INTO `quizzes` (`quiz_id`, `category_id`, `quiz_title`, `description`, `time_limit`, `total_questions`) VALUES
(1, 1, 'Python Basics', 'Test your fundamental knowledge of Python data types, loops, functions, and standard library.', 10, 10),
(2, 2, 'HTML & CSS', 'Evaluate your understanding of HTML5 semantics, CSS grid, flexbox, and web styling principles.', 10, 10),
(3, 2, 'JavaScript', 'Master ES6+ JavaScript concepts including async/await, closures, DOM manipulation, and promises.', 10, 10),
(4, 3, 'SQL', 'Test your relational database queries, JOINs, aggregation functions, and DDL/DML statements.', 10, 10),
(5, 4, 'General Aptitude', 'Assess logical reasoning, quantitative problem solving, and analytical skills.', 10, 10);

-- Questions (50 Total MCQ Questions)

-- Quiz 1: Python Basics
INSERT INTO `questions` (`quiz_id`, `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_answer`) VALUES
(1, 'What is the correct file extension for Python files?', '.pyt', '.python', '.py', '.pt', 'C'),
(1, 'Which keyword is used to define a function in Python?', 'func', 'def', 'function', 'define', 'B'),
(1, 'How do you insert COMMENTS in Python code?', '// This is a comment', '/* This is a comment */', '# This is a comment', '<!-- This is a comment -->', 'C'),
(1, 'Which data structure is immutable in Python?', 'List', 'Dictionary', 'Set', 'Tuple', 'D'),
(1, 'What will type([]) return in Python?', '<class \'tuple\'>', '<class \'dict\'>', '<class \'list\'>', '<class \'array\'>', 'C'),
(1, 'Which operator is used for exponentiation (power) in Python?', '^', '**', '^^', '//', 'B'),
(1, 'What is the output of len(\'Hello World\')?', '10', '11', '12', '9', 'B'),
(1, 'Which built-in module in Python is used to generate random numbers?', 'math', 'random', 'rand', 'generate', 'B'),
(1, 'What is the correct syntax to print a message in Python 3?', 'echo \'Hello\'', 'print(\'Hello\')', 'System.out.println(\'Hello\')', 'console.log(\'Hello\')', 'B'),
(1, 'How do you create a variable with the floating number 2.8 in Python?', 'x = float(2.8)', 'x = 2.8', 'Both A and B are correct', 'float x = 2.8', 'C');

-- Quiz 2: HTML & CSS
INSERT INTO `questions` (`quiz_id`, `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_answer`) VALUES
(2, 'What does HTML stand for?', 'Hyper Text Markup Language', 'High Text Machine Language', 'Hyperlink Text Management Language', 'Home Tool Markup Language', 'A'),
(2, 'Which HTML5 tag is used to define an independent self-contained article?', '<section>', '<article>', '<div>', '<main>', 'B'),
(2, 'Which CSS property is used to change the background color of an element?', 'color', 'bgcolor', 'background-color', 'canvas-color', 'C'),
(2, 'How do you select an element with id \'header\' in CSS?', '.header', '#header', 'header', '*header', 'B'),
(2, 'What is the default value of the position property in CSS?', 'relative', 'absolute', 'fixed', 'static', 'D'),
(2, 'Which CSS Flexbox property aligns items along the cross axis?', 'justify-content', 'align-items', 'flex-direction', 'align-content', 'B'),
(2, 'Which HTML tag is used to embed an image?', '<img>', '<image>', '<pic>', '<media>', 'A'),
(2, 'Which HTML attribute specifies an alternate text for an image if the image cannot be displayed?', 'title', 'src', 'alt', 'longdesc', 'C'),
(2, 'How can you make a numbered list in HTML?', '<ul>', '<dl>', '<list>', '<ol>', 'D'),
(2, 'What does CSS stand for?', 'Cascading Style Sheets', 'Creative Style Sheets', 'Computer Style System', 'Colorful Style Sheets', 'A');

-- Quiz 3: JavaScript
INSERT INTO `questions` (`quiz_id`, `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_answer`) VALUES
(3, 'Which keyword is used to declare a block-scoped variable in JavaScript?', 'var', 'let', 'dim', 'set', 'B'),
(3, 'What will typeof NaN evaluate to in JavaScript?', '\'number\'', '\'NaN\'', '\'undefined\'', '\'object\'', 'A'),
(3, 'Which method converts a JSON string into a JavaScript object?', 'JSON.stringify()', 'JSON.parse()', 'JSON.toObject()', 'JSON.convert()', 'B'),
(3, 'What is the output of 0 == \'0\' in JavaScript?', 'true', 'false', 'TypeError', 'undefined', 'A'),
(3, 'What is the output of 0 === \'0\' in JavaScript?', 'true', 'false', 'TypeError', 'undefined', 'B'),
(3, 'Which method is used to add new items to the end of an Array?', 'push()', 'pop()', 'unshift()', 'append()', 'A'),
(3, 'How do you write an arrow function in JavaScript?', 'const fn = () => {}', 'const fn = function() {}', 'function => fn() {}', 'def fn():', 'A'),
(3, 'Which object represents an eventual completion or failure of an asynchronous operation?', 'Callback', 'Promise', 'AsyncToken', 'EventListener', 'B'),
(3, 'How do you select an HTML element by ID in JavaScript?', 'document.getElement(id)', 'document.getElementById(id)', 'document.queryId(id)', 'window.findId(id)', 'B'),
(3, 'Which event occurs when the user clicks on an HTML element?', 'onchange', 'onmouseover', 'onclick', 'onkeydown', 'C');

-- Quiz 4: SQL
INSERT INTO `questions` (`quiz_id`, `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_answer`) VALUES
(4, 'What does SQL stand for?', 'Structured Query Language', 'Simple Query Logic', 'Sequential Query List', 'Standard Question Language', 'A'),
(4, 'Which SQL clause is used to filter records matching specified criteria?', 'GROUP BY', 'ORDER BY', 'WHERE', 'HAVING', 'C'),
(4, 'Which command is used to retrieve data from a database in SQL?', 'GET', 'FETCH', 'EXTRACT', 'SELECT', 'D'),
(4, 'Which SQL statement is used to insert new data into a database table?', 'ADD RECORD', 'INSERT INTO', 'UPDATE', 'CREATE ROW', 'B'),
(4, 'Which JOIN type returns all rows from the left table and matched rows from the right table?', 'INNER JOIN', 'RIGHT JOIN', 'LEFT JOIN', 'FULL JOIN', 'C'),
(4, 'Which Aggregate function in SQL counts the number of rows?', 'SUM()', 'COUNT()', 'TOTAL()', 'ROW_COUNT()', 'B'),
(4, 'How do you delete a database table structure permanently in SQL?', 'REMOVE TABLE', 'DELETE TABLE', 'DROP TABLE', 'TRUNCATE TABLE', 'C'),
(4, 'Which keyword is used to sort the result set in ascending or descending order?', 'SORT BY', 'ORDER BY', 'GROUP BY', 'ALIGN BY', 'B'),
(4, 'Which SQL constraint uniquely identifies each record in a table?', 'FOREIGN KEY', 'CHECK', 'NOT NULL', 'PRIMARY KEY', 'D'),
(4, 'Which clause is used with aggregate functions to filter groups of records?', 'WHERE', 'HAVING', 'GROUP FILTER', 'LIKE', 'B');

-- Quiz 5: General Aptitude
INSERT INTO `questions` (`quiz_id`, `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_answer`) VALUES
(5, 'What comes next in the sequence: 2, 6, 12, 20, 30, ...?', '36', '40', '42', '48', 'C'),
(5, 'If a car travels 120 km in 2 hours, what is its average speed in meters per second?', '16.67 m/s', '30 m/s', '60 m/s', '25 m/s', 'A'),
(5, 'A father is 4 times as old as his son. In 20 years, he will be twice as old as his son. How old is the son now?', '5 years', '10 years', '15 years', '20 years', 'B'),
(5, 'Which letter comes next in the series: A, C, F, J, O, ...?', 'S', 'T', 'U', 'V', 'C'),
(5, 'What is 15% of 240?', '30', '34', '36', '40', 'C'),
(5, 'If 6 men can complete a work in 12 days, how many days will 8 men take to complete the same work?', '9 days', '8 days', '10 days', '6 days', 'A'),
(5, 'Which fraction is the largest: 3/4, 5/6, 7/9, or 4/5?', '3/4', '5/6', '7/9', '4/5', 'B'),
(5, 'Find the odd one out: Apple, Banana, Mango, Potato, Grape.', 'Banana', 'Mango', 'Potato', 'Grape', 'C'),
(5, 'If \'CODES\' is written as \'DPEFT\' in a code language, how is \'LOGIC\' written?', 'MPHJD', 'MPHID', 'NQIJD', 'KNFHB', 'A'),
(5, 'What is the probability of getting an even number when throwing a fair 6-sided die?', '1/6', '1/3', '1/2', '2/3', 'C');
