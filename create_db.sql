USE Music_information;

CREATE TABLE Artist (
    id INT IDENTITY PRIMARY KEY, 
    name NVARCHAR(100) NOT NULL, 
    startDate DATE NOT NULL,
    country NVARCHAR(40) NOT NULL,
    description NVARCHAR(500) 
);

CREATE TABLE Song (
    id INT IDENTITY PRIMARY KEY, 
    artistId INT NOT NULL, 
    title NVARCHAR(100) NOT NULL, 
    genre NVARCHAR(50) NOT NULL, 
    duration TIME NOT NULL, 
    releaseDate DATE NOT NULL, 
    rating DECIMAL(2, 1) DEFAULT 0, 
    CONSTRAINT FK_Song_Artist FOREIGN KEY (artistId) REFERENCES Artist(id)
);

INSERT INTO Artist (name, startDate, country, description)
VALUES 
    ('Depeche Mode', '1980-01-01', 'UK', 'An iconic synth-pop and electronic music band.'),
    ('Daft Punk', '1993-01-01', 'France', 'Famous French electronic music duo known for their unique sound and robot personas.'),
    ('Sting', '1971-01-01', 'UK', 'Legendary musician, songwriter, and former member of The Police.');

INSERT INTO Song (artistId, title, genre, duration, releaseDate, rating)
VALUES 
    (1, 'Enjoy the Silence', 'Synth-pop', '00:04:15', '1990-02-05', 4.8), 
    (1, 'Personal Jesus', 'Synth-rock', '00:04:56', '1989-08-29', 4.9),   

    (2, 'One More Time', 'House', '00:05:20', '2000-11-30', 4.7),        
    (2, 'Get Lucky', 'Disco', '00:06:09', '2013-04-19', 4.9),           

    (3, 'Fields of Gold', 'Soft Rock', '00:03:40', '1993-06-01', 4.6),   
    (3, 'Englishman in New York', 'Jazz-pop', '00:04:27', '1988-02-01', 4.8); 

CREATE TABLE Dictionary (
    id INT IDENTITY PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    displayName NVARCHAR(100) NOT NULL
);

CREATE TABLE Dictionary_Fields (
    id INT IDENTITY PRIMARY KEY,
    dictionaryId INT NOT NULL,
    fieldName NVARCHAR(100) NOT NULL,
    displayName NVARCHAR(100) NOT NULL,
    fieldType NVARCHAR(20) NOT NULL, -- 'text', 'date', 'select', etc.
    CONSTRAINT FK_Dictionary_Fields FOREIGN KEY (dictionaryId) REFERENCES Dictionary(id)
);

INSERT INTO Dictionary (name, displayName) 
VALUES ('Artist', 'Исполнители'), ('Song', 'Песни');

INSERT INTO Dictionary_Fields (dictionaryId, fieldName, displayName, fieldType) VALUES
(1, 'name', 'Имя', 'text'),
(1, 'startDate', 'Дата начала', 'date'),
(1, 'country', 'Страна', 'text'),
(1, 'description', 'Описание', 'textarea'),
(2, 'title', 'Название', 'text'),
(2, 'genre', 'Жанр', 'text'),
(2, 'duration', 'Продолжительность', 'text'),
(2, 'releaseDate', 'Дата релиза', 'date'),
(2, 'rating', 'Рейтинг', 'number');



