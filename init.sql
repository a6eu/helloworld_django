-- Создание новой базы данных

CREATE DATABASE helloworld_db;

-- Создание нового пользователя

CREATE USER adminshop WITH PASSWORD 'helloworld_coc_2024';

-- Предоставление пользователю прав на новую базу данных

GRANT ALL PRIVILEGES ON DATABASE helloworld_db TO adminshop;