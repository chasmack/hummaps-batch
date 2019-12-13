DROP DATABASE IF EXISTS production;
DROP USER IF EXISTS pgadmin;
DROP USER IF EXISTS hummaps;

CREATE USER pgadmin WITH
  LOGIN NOSUPERUSER NOINHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;

CREATE USER hummaps WITH
  LOGIN NOSUPERUSER NOINHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;

CREATE DATABASE production
    WITH 
    OWNER = pgadmin
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;