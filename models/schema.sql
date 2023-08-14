/*
basic db structure:
t_users:
    id, name, register date
t_drink:
    id, name, type (enum), date_year_crafted, date_posted, date_updated, date_deleted, is_deleted, description
t_tag:
    id, name
t_drink_tag:
    id, fk_drink_id, fk_tag_id
t_drink_search:
    id, fk_drink_id, str_representation

common use cases:
fetch drink list. limit and offset
    -get id, name, type, year, date posted
fetch drink id. need id only
    -get all info, incl tags
    -use t_drink.id as fk_drink_id in t_drink_tag to get all tags associated with the drink
    -then fetch all unique tags (they better be unique!) with the given fk_tag_ids
    -return list of tags and append to the response payload
search drinks. search terms is a space delineated string, assuming AND between terms. no spellchecking
    -the trouble is, how do i search on tags?
        -can do it the ssam way and create a string based on all aspects of the drink.
            -then flag that column for fulltext searching..?
            -or perhaps run CONTAINS on each drink
            -things will be small scale enough to the point where this should be fine.
create drink
    -
update drink
*/

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