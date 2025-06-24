CREATE TABLE rols (
    id SERIAL PRIMARY KEY,
    rol_resource_key VARCHAR(20) UNIQUE NOT NULL,
    display_name VARCHAR(50) NOT NULL,
    description VARCHAR(255)
);


-- Insertar los roles
INSERT INTO rols (rol_resource_key, display_name, description) VALUES
('fitness_buddy', 'Fitness Buddy', 'Usuario que busca entrenar y encontrar compañeros'),
('personal_trainer', 'Personal Trainer', 'Profesional que ofrece servicios de entrenamiento');


CREATE TABLE user_rols (
    user_id INT NOT NULL,
    rol_id INT NOT NULL,
    PRIMARY KEY (user_id, rol_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (rol_id) REFERENCES rols(id)
);

ALTER TABLE rols
ADD COLUMN icon VARCHAR(20);
