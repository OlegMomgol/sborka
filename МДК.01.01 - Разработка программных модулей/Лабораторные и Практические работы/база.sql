CREATE DATABASE note_manager;
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO categories (name) VALUES 
    ('Учёба'),
    ('Работа'),
    ('Личное'),
    ('Идеи'),
    ('Важное');

INSERT INTO users (username) VALUES 
    ('student'),
    ('admin'),
    ('user1');

INSERT INTO notes (title, content, category_id, user_id) VALUES 
    ('Первая заметка', 'Текст первой заметки', 1, 1),
    ('План работы', '1. Встреча с командой\n2. Написать отчет\n3. Проверить почту', 2, 1),
    ('Список покупок', 'Молоко, хлеб, яйца, сыр', 3, 1),
    ('Идея для проекта', 'Создать приложение для управления задачами', 4, 2),
    ('Важная встреча', 'Встреча с клиентом в 15:00', 5, 2);

CREATE INDEX idx_notes_category ON notes(category_id);
CREATE INDEX idx_notes_user ON notes(user_id);
CREATE INDEX idx_notes_created ON notes(created_at DESC);