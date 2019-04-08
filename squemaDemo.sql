create table Users(user_id serial primary key, first_name varchar(15), last_name varchar(15), email varchar(25) unique, phone varchar(15) unique);

create table Credential(username varchar(15) unique, password varchar(20), user_id integer references Users(user_id), primary key(user_id, username));

create table Activity(activity_id serial, user_id integer references Users(user_id), activity_date timestamp without time zone, primary key(activity_id, user_id));

create table ContactList(user_id integer references Users(user_id), contact_id integer references Users(user_id), primary key(user_id, contact_id));

create table Chat(chat_id serial primary key, chat_name varchar(15), admin integer references Users(user_id));

create table Participant(chat_id integer references Chat(chat_id), user_id integer references Users(user_id), primary key(user_id, chat_id));

create table Post(post_id serial primary key, post_msg varchar(280), post_date timestamp without time zone, user_id integer references Users(user_id), chat_id integer references Chat(chat_id));

create table Hashtag(hashtag_id serial, hashtag_text varchar (15), post_id integer references Post(post_id),  primary key(post_id, hashtag_id));

create table React(user_id integer references Users(user_id), post_id integer references Post(post_id), react_date timestamp without time zone, react_type smallint, primary key (user_id, post_id), check(react_type = 1 OR react_type = -1));

create table Media(media_id serial primary key, post_id integer references Post(post_id), media_type char(1), location varchar(200), check(media_type = 'V' OR media_type = 'P' OR media_type = 'M'));

create table Reply(reply_id serial primary key, reply_msg varchar(280), reply_date timestamp without time zone, user_id integer references Users(user_id),  post_id integer references Post(post_id));

--IN CASE YOU WANT TO DELETE EVERYTHING
--sudo -u postgres psql -c "DROP SCHEMA public CASCADE;
--create SCHEMA public;
--grant usage on schema public to public;
--grant create on schema public to public;" pictochatdb


create table Users(user_id serial primary key, first_name varchar(15), last_name varchar(15), email varchar(25) unique, phone varchar(15) unique);
insert into Users(first_name, last_name, email, phone) values ('Renier', 'Velazco', 'renier.velazco@upr.edu', '787-247-4930');
insert into Users(first_name, last_name, email, phone) values ('Julian', 'Cuevas', 'julian.cuevas@upr.edu', '787-607-4678');
insert into Users(first_name, last_name, email, phone) values ('Cristian', 'Torres', 'cristian.torres@upr.edu', '787-218-2447');
insert into Users(first_name, last_name, email, phone) values ('Jose', 'Santi', 'jose.santi@upr.edu', '787-607-4920');
insert into Users(first_name, last_name, email, phone) values ('Manuel', 'Collazo', 'manuel.collazo@upr.edu', '787-253-2447');



create table Credential(username varchar(15) unique, password varchar(20), user_id integer references Users(user_id), primary key(username, user_id));
insert into Credential(username, password, user_id) values ('reniercito', 'reniercito', 1);
insert into Credential(username, password, user_id) values ('juliansito', 'reniercito', 2);
insert into Credential(username, password, user_id) values ('cristiansote', 'cristiansote', 3);
insert into Credential(username, password, user_id) values ('joselito', 'joselito', 4);
insert into Credential(username, password, user_id) values ('manuelito', 'manuelito', 5);


create table Activity(activity_id serial, user_id integer references Users(user_id), activity_date timestamp without time zone, primary key(activity_id, user_id));
insert into Activity(user_id, activity_date) values (1, TIMESTAMP '2019-4-7 12:30:56');
insert into Activity(user_id, activity_date) values (2, TIMESTAMP '2019-4-7 12:33:25');
insert into Activity(user_id, activity_date) values (3, TIMESTAMP '2019-4-7 12:40:10');
insert into Activity(user_id, activity_date) values (4, TIMESTAMP '2019-4-7 12:47:12');
insert into Activity(user_id, activity_date) values (5, TIMESTAMP '2019-4-7 12:59:30');
insert into Activity(user_id, activity_date) values (5, TIMESTAMP '2019-4-8 14:30:56');
insert into Activity(user_id, activity_date) values (4, TIMESTAMP '2019-4-8 15:33:25');
insert into Activity(user_id, activity_date) values (3, TIMESTAMP '2019-4-9 16:40:10');
insert into Activity(user_id, activity_date) values (2, TIMESTAMP '2019-4-9 18:47:12');
insert into Activity(user_id, activity_date) values (1, TIMESTAMP '2019-4-9 19:59:30');
insert into Activity(user_id, activity_date) values (4, TIMESTAMP '2019-4-10 15:33:25');
insert into Activity(user_id, activity_date) values (3, TIMESTAMP '2019-4-10 16:40:10');
insert into Activity(user_id, activity_date) values (2, TIMESTAMP '2019-4-10 18:47:12');


create table ContactList(user_id integer references Users(user_id), contact_id integer references Users(user_id), primary key(user_id, contact_id));
insert into ContactList(user_id, contact_id) values(1, 2);
insert into ContactList(user_id, contact_id) values(1, 4);
insert into ContactList(user_id, contact_id) values(1, 5);
insert into ContactList(user_id, contact_id) values(2, 1);
insert into ContactList(user_id, contact_id) values(2, 3);
insert into ContactList(user_id, contact_id) values(3, 2);
insert into ContactList(user_id, contact_id) values(3, 5);
insert into ContactList(user_id, contact_id) values(4, 1);
insert into ContactList(user_id, contact_id) values(4, 5);
insert into ContactList(user_id, contact_id) values(5, 1);
insert into ContactList(user_id, contact_id) values(5, 2);
insert into ContactList(user_id, contact_id) values(5, 4);


create table Chat(chat_id serial primary key, chat_name varchar(15), admin integer references Users(user_id));
insert into Chat(chat_name, admin) values('OS', 1);
insert into Chat(chat_name, admin) values('Arqui', 2);
insert into Chat(chat_name, admin) values('Algoritmo', 3);
insert into Chat(chat_name, admin) values('DB', 4);
insert into Chat(chat_name, admin) values('Filosofia', 5);


create table Participant(chat_id integer references Chat(chat_id), user_id integer references Users(user_id), primary key(chat_id, user_id));
insert into Participant(chat_id,user_id) values(1, 1);
insert into Participant(chat_id,user_id) values(1, 2);
insert into Participant(chat_id,user_id) values(1, 3);
insert into Participant(chat_id,user_id) values(2, 3);
insert into Participant(chat_id,user_id) values(2, 4);
insert into Participant(chat_id,user_id) values(2, 5);
insert into Participant(chat_id,user_id) values(3, 1);
insert into Participant(chat_id,user_id) values(3, 2);
insert into Participant(chat_id,user_id) values(3, 3);
insert into Participant(chat_id,user_id) values(3, 4);
insert into Participant(chat_id,user_id) values(3, 5);
insert into Participant(chat_id,user_id) values(4, 1);
insert into Participant(chat_id,user_id) values(4, 2);
insert into Participant(chat_id,user_id) values(4, 3);
insert into Participant(chat_id,user_id) values(4, 4);
insert into Participant(chat_id,user_id) values(4, 5);
insert into Participant(chat_id,user_id) values(5, 3);



create table Post(post_id serial primary key, post_msg varchar(280), post_date timestamp without time zone, user_id integer references Users(user_id), chat_id integer references Chat(chat_id));
insert into Post(post_msg, post_date, user_id, chat_id) values
('Hey! Miren donde estoy', TIMESTAMP '2019-3-28 14:30:12', 1, 1), ('En la trucka para Cabo Rojo', TIMESTAMP '2019-3-29 14:32:12', 1, 1),
('Familia! Cuando es la fiesta? Miren lo que llevo', TIMESTAMP '2019-4-01 10:21:27', 4, 3),
('Para el que pidio foto del examen viejo!', TIMESTAMP '2019-4-03 15:23:44', 3, 4),
('El mejor meme que existe', TIMESTAMP '2019-4-03 17:12:54', 1, 5);

create table Hashtag(hashtag_id serial, hashtag_text varchar (15), post_id integer references Post(post_id),  primary key(post_id, hashtag_id));
insert into Hashtag(hashtag_text, post_id) values
('#chilling', 2), ('#chilling', 3), ('#chilling', 4), ('#chilling', 5),
('#VamoaBeber', 1), ('#VamoaBeber', 3) ('#VamoaBeber', 5),
('#PaElClutch', 1), ('#PaElClutch', 2),
('#FuckingMuerto', 1);

create table React(user_id integer references Users(user_id), post_id integer references Post(post_id), react_date timestamp without time zone, react_type smallint, primary key (user_id, post_id), check(react_type = 1 OR react_type = -1));
insert into React(user_id, post_id, react_date, react_type) values
(3, 1, TIMESTAMP '2019-3-28 14:30:45', 1),
(2, 1, TIMESTAMP '2019-3-28 14:31:30', 1),
(5, 2, TIMESTAMP '2019-4-01 10:59:20', 1),
(1, 3, TIMESTAMP '2019-4-03 17:15:54', 1),
(5, 4, TIMESTAMP '2019-4-03 17:16:34', -1);

create table Media(media_id serial primary key, post_id integer references Post(post_id), media_type char(1), location varchar(200), check(media_type = 'V' OR media_type = 'P' OR media_type = 'M'));
insert into Media(post_id, media_type, location) values
(1, 'P', '/static/img-1-playa.png'),
(2, 'P', '/static/img-2-truck.png'),
(3, 'P', '/static/img-3-whiskey.png'),
(4, 'P', '/static/img-4-DB.png');
(5, 'P', '/static/img-5-meme.png');


create table Reply(reply_id serial primary key, reply_msg varchar(280), reply_date timestamp without time zone, user_id integer references Users(user_id),  post_id integer references Post(post_id));
insert into Reply(reply_msg, reply_date, user_id, post_id) values
('Nice mano! Se ve chevere', TIMESTAMP '2019-3-28 14:31:20', 3, 1),
('Super cool man', TIMESTAMP '2019-3-28 14:32:05', 2, 1),
('No se, pero mas vale que lleven ron!', TIMESTAMP '2019-4-01 11:00:57', 5, 2),
('Si no hay, no me esperen!', TIMESTAMP '2019-4-01 11:05:14', 5, 2),
('Mano, un millon de gracias', TIMESTAMP '2019-4-03 17:15:14', 1, 3);
