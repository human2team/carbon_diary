CREATE DATABASE IF NOT EXISTS carbon_diary DEFAULT CHARACTER SET utf8mb4;

USE carbon_diary;

CREATE TABLE diary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entry_date DATE NOT NULL,
    meal VARCHAR(255),
    transport VARCHAR(255),
    computer_hours FLOAT,
    emissions FLOAT
);
