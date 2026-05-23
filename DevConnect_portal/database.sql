CREATE DATABASE new;

USE new;

CREATE TABLE developers(

    id INT PRIMARY KEY AUTO_INCREMENT,

    name VARCHAR(100),

    email VARCHAR(100) UNIQUE,

    skill VARCHAR(100),

    experience VARCHAR(100),

    password VARCHAR(300),

    profile_image VARCHAR(255)

);