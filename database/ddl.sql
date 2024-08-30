CREATE DATABASE during_test;
DROP SCHEMA vectordb CASCADE;
CREATE SCHEMA vectordb;
CREATE TYPE chat_type_enum AS ENUM ('text', 'image', 'video', 'interaction');
CREATE TABLE vectordb.couple_chat_message (
    couple_chat_id BIGINT NOT NULL PRIMARY KEY,
    chat_type chat_type_enum NOT NULL,
    context TEXT NOT NULL,
    chat_date TIMESTAMP NOT NULL,
    send_member_id UUID NOT NULL,
    couple_id UUID NOT NULL
);
CREATE TYPE sender_type_enum AS ENUM ('gomdu', 'user');
CREATE TABLE vectordb.pet_chat_history (
    pet_chat_history_id BIGINT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL
);
CREATE TABLE vectordb.pet_chat_message (
    pet_chat_id BIGINT NOT NULL PRIMARY KEY,
    sender sender_type_enum NOT NULL,
    content TEXT NOT NULL,
    chat_date TIMESTAMP NOT NULL,
    pet_chat_history_id BIGINT NOT NULL,
    member_id UUID NOT NULL,
    couple_id UUID NOT NULL,
    FOREIGN KEY (pet_chat_history_id) REFERENCES vectordb.pet_chat_history(pet_chat_history_id)
);
CREATE TABLE vectordb.chunk (
    chunk_id BIGINT NOT NULL PRIMARY KEY,
    vector vector(1536) NOT NULL,
    summary TEXT NOT NULL,
    couple_id UUID NOT NULL
);
CREATE TABLE vectordb.chunked_couple_chat (
    chunk_id BIGINT NOT NULL,
    couple_chat_id BIGINT NOT NULL,
    FOREIGN KEY (chunk_id) REFERENCES vectordb.chunk(chunk_id),
    FOREIGN KEY (couple_chat_id) REFERENCES vectordb.couple_chat_message(couple_chat_id)
);