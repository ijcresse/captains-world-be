CREATE DATABASE captains_world;
USE captains_world;
CREATE TABLE t_drink_types(
    c_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    c_drink_type VARCHAR(10)
);
CREATE TABLE t_drink(
    c_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    c_name VARCHAR(200),
    c_drink_type ENUM('other', 'sake', 'spirit', 'wine', 'beer') DEFAULT 'other',
    c_sake_type ENUM('none', 'futsushu_honjozo', 'ginjo_tokubetsu', 'junmai', 'daiginjo', 'specialty') DEFAULT 'none',
    c_description TEXT,
    c_date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    c_date_crafted TIMESTAMP,
    c_date_enjoyed TIMESTAMP,
    c_date_updated TIMESTAMP,
    c_date_deleted TIMESTAMP,
    c_image_url VARCHAR(255),
    c_is_deleted BOOLEAN DEFAULT 0
);
CREATE TABLE t_tag(
    c_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    c_tag_name VARCHAR(200)
);
CREATE TABLE t_drink_tag(
    c_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fk_drink_id INT NOT NULL,
    fk_tag_id INT NOT NULL
);
CREATE TABLE t_users(
    c_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    c_username VARCHAR(255) NOT NULL,
    c_email VARCHAR(255),
    c_password VARCHAR(255) NOT NULL,
    c_last_login TIMESTAMP
);
CREATE TABLE t_sessions(
    c_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    c_session_name VARCHAR(255) NOT NULL,
    c_login_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
