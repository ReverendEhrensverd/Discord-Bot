CREATE DATABASE IF NOT EXISTS inf19;

CREATE TABLE IF NOT EXISTS discord_users(

userID bigint not null unique primary key ,
userName varchar[50] not null ,
userNumber smallint not null

);



CREATE TABLE IF NOT EXISTS ping_score(

userID
score
userName
userNumber
userNickname

);