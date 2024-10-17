CREATE DATABASE during_test;
DROP SCHEMA vectordb CASCADE;
CREATE SCHEMA vectordbp;
CREATE TYPE chat_type_enum AS ENUM ('text', 'image', 'video', 'interaction');
CREATE TABLE vectordbp.couple_chat_message (
    couple_chat_message_id BIGINT NOT NULL PRIMARY KEY,
    message_type chat_type_enum NOT NULL,
    content TEXT NOT NULL,
    message_date TIMESTAMP NOT NULL,
    send_member_id UUID NOT NULL,
    couple_id UUID NOT NULL
);
CREATE TABLE vectordbp.pet_chat (
    pet_chat_id BIGINT NOT NULL PRIMARY KEY,
    sender BIGINT NOT NULL,
    content TEXT NOT NULL,
    chat_date TIMESTAMP NOT NULL,
    member_id UUID NOT NULL,
    couple_id UUID NOT NULL
);
CREATE TABLE vectordbp.chunk (
    chunk_id BIGINT NOT NULL PRIMARY KEY,
    vector vector(768) NOT NULL,
    summary TEXT NOT NULL,
    couple_id UUID NOT NULL,
    FOREIGN KEY (couple_id) REFERENCES public.couple(couple_id)
);
CREATE TABLE vectordbp.chunked_couple_chat (
    chunked_couple_chat_id BIGINT NOT NULL PRIMARY KEY,
    chunk_id BIGINT NOT NULL,
    couple_chat_message_id BIGINT NOT NULL,
    FOREIGN KEY (chunk_id) REFERENCES public.chunk(chunk_id),
    FOREIGN KEY (couple_chat_message_id) REFERENCES public.couple_chat_message(couple_chat_message_id)
);
CREATE TABLE public.chunked_row_number (
    chunked_row_number_id BIGINT NOT NULL PRIMARY KEY,
    couple_id UUID NOT NULL,
    row_number BIGINT NOT NULL
);
CREATE TABLE vectordbp.couple (
    couple_id UUID NOT NULL PRIMARY KEY,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    state TEXT NOT NULL
);
CREATE TABLE vectordbp.member_activity
(
    active_date timestamp(6) without time zone,
    activity_id bigint NOT NULL,
    member_id uuid,
    active_type character varying(255),
    CONSTRAINT member_activity_pkey PRIMARY KEY (activity_id),
    CONSTRAINT member_activity_active_type_check CHECK (active_type::text = ANY (ARRAY['LOGIN'::character varying, 'LOGOUT'::character varying]::text[]))
);