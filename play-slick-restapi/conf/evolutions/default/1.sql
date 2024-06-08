# --- !Ups

CREATE TABLE todos (
                       id SERIAL PRIMARY KEY,
                       time TIMESTAMP NOT NULL,
                       description VARCHAR(255) NOT NULL
);

# --- !Downs

DROP TABLE todos;
