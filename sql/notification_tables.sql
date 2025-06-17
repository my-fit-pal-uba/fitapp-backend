CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    description VARCHAR(300) NOT NULL,
    date TIMESTAMP NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    user_id INT NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id) 
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Aca se podria agregar una columna para indicar que archivo de audio use la notificacion