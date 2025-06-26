--USER
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

CREATE TABLE user_photos (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    photo BYTEA,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--ROLS
CREATE TABLE rols (
    id SERIAL PRIMARY KEY,
    rol_resource_key VARCHAR(20) UNIQUE NOT NULL,
    display_name VARCHAR(50) NOT NULL,
    description VARCHAR(255)
    icon VARCHAR(20)
);

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

--PROFILE
CREATE TABLE profiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(user_id),
    age INTEGER NOT NULL,
    height INTEGER NOT NULL CHECK (height > 0),
    gender VARCHAR NOT NULL
);

--EXERCISES
CREATE TABLE exercises (
    exercise_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    muscular_group VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    place VARCHAR(100) NOT NULL,
    photo_guide VARCHAR(255),
    video_guide VARCHAR(255)
);

INSERT INTO exercises (
    name, description, muscular_group, type, place, photo_guide, video_guide
) VALUES
(
    'Push-Up',
    'An upper-body strength exercise performed by raising and lowering the body using the arms.',
    'Chest',
    'Bodyweight',
    'Home',
    'https://github.com/leodra21/media/blob/main/pushup.jpeg?raw=true',
    'https://github.com/leodra21/media/raw/refs/heads/main/pushup.mp4'
),
(
    'Barbell Squat',
    'A compound exercise that targets the lower body by squatting with a barbell across the upper back.',
    'Legs',
    'Weightlifting',
    'Gym',
    'https://github.com/leodra21/media/blob/main/barbellsquat.jpeg?raw=true',
    'https://github.com/leodra21/media/raw/refs/heads/main/barbellsquat.mp4'
),
(
    'Plank',
    'A core strengthening exercise where the body is held in a straight line for a set period of time.',
    'Core',
    'Isometric',
    'Home',
    'https://github.com/leodra21/media/blob/main/plank.jpeg?raw=true',
    'https://github.com/leodra21/media/raw/refs/heads/main/Plank.mp4'
),
(
    'Lat Pulldown',
    'Exercise targeting the back muscles by pulling a bar down toward the chest while seated.',
    'Back',
    'Machine',
    'Gym',
    'https://github.com/leodra21/media/blob/main/latPulldown.jpeg?raw=true',
    'https://github.com/leodra21/media/raw/refs/heads/main/latPulldown.mp4'
);

CREATE TABLE exercise_ratings (
    user_id     INTEGER NOT NULL,
    exercise_id  INTEGER NOT NULL,
    rating      NUMERIC(2,1) NOT NULL,
    PRIMARY KEY (user_id, exercise_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
);

--CALORIES
CREATE TABLE calories_history (
    record_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    calories FLOAT NOT NULL,

    CONSTRAINT fk_calories_user FOREIGN KEY (user_id) 
        REFERENCES users(user_id) ON DELETE CASCADE,

    CONSTRAINT uq_user_date_calories UNIQUE (user_id, date)
);

--WEIGHT
CREATE TABLE weight_history (
    record_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    weight FLOAT NOT NULL,

    CONSTRAINT fk_weight_user FOREIGN KEY (user_id) 
        REFERENCES users(user_id) ON DELETE CASCADE,

    CONSTRAINT uq_user_date_weight UNIQUE (user_id, date)
); 

--SERIES
CREATE TABLE series (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  exercise_id INTEGER NOT NULL,
  reps INTEGER NOT NULL,
  weight NUMERIC(5,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
);

--ROUTINES
CREATE TABLE routines (
    routine_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    muscular_group VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    series INTEGER
);

CREATE TABLE routine_exercises (
    routine_id INTEGER REFERENCES Routines(routine_id),
    exercise_id INTEGER REFERENCES Exercises(exercise_id),
    PRIMARY KEY (routine_id, exercise_id)
);

CREATE TABLE done_routines (
    user_id     INTEGER NOT NULL,
    routine_id  INTEGER NOT NULL,
    done_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, routine_id, done_at),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (routine_id) REFERENCES routines(routine_id)
);

CREATE TABLE routine_ratings (
    user_id     INTEGER NOT NULL,
    routine_id  INTEGER NOT NULL,
    rating      NUMERIC(2,1) NOT NULL,
    PRIMARY KEY (user_id, routine_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (routine_id) REFERENCES routines(routine_id)
); 


--DISH
CREATE TABLE meal_categories (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    CONSTRAINT uq_meal_category_description UNIQUE (description)
);

CREATE TABLE diet (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL, 
    observation TEXT,
    CONSTRAINT uq_diet_name UNIQUE (name)
);

CREATE TABLE dishes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    calories FLOAT CHECK (calories >= 0), 
    proteins FLOAT CHECK (proteins >= 0), 
    carbs FLOAT CHECK (carbs >= 0), 
    fat FLOAT CHECK (fat >= 0),
    weight_in_g FLOAT CHECK (weight_in_g >= 0),
    CONSTRAINT uq_dish_name UNIQUE (name)
);

CREATE TABLE dish_categories (
    dish_id INT REFERENCES dishes(id) ON DELETE CASCADE,
    category_id INT REFERENCES meal_categories(id) ON DELETE CASCADE,
    PRIMARY KEY (dish_id, category_id),
    CONSTRAINT fk_dishcategories_dish FOREIGN KEY (dish_id) REFERENCES dishes(id),
    CONSTRAINT fk_dishcategories_category FOREIGN KEY (category_id) REFERENCES meal_categories(id)
);

CREATE TABLE diet_dishes (
    id SERIAL PRIMARY KEY,
    dish_id INT NOT NULL, 
    diet_id INT NOT NULL, 
    meal_category_id INT NOT NULL,
    serving_size_g FLOAT CHECK (serving_size_g > 0),
    CONSTRAINT fk_dietdishes_dish 
        FOREIGN KEY (dish_id) 
        REFERENCES dishes(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_dietdishes_diet 
        FOREIGN KEY (diet_id) 
        REFERENCES diet(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_dietdishes_mealcategory 
        FOREIGN KEY (meal_category_id) 
        REFERENCES meal_categories(id)
        ON DELETE RESTRICT,
    CONSTRAINT unique_dish_diet_meal 
        UNIQUE (dish_id, diet_id, meal_category_id)
);

CREATE TABLE dishes_history (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    dish_id INT NOT NULL,
    consumption_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    serving_size_g FLOAT CHECK (serving_size_g > 0),
    calories FLOAT CHECK (calories >= 0),
    protein FLOAT CHECK (protein >= 0),
    carbohydrates FLOAT CHECK (carbohydrates >= 0),
    fats FLOAT CHECK (fats >= 0),
    
    CONSTRAINT fk_dishhistory_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_dishhistory_dish FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE RESTRICT
);

INSERT INTO meal_categories (description) VALUES
('Desayuno'),
('Almuerzo'),
('Cena'),
('Snack'),
('Postre');

INSERT INTO dishes (name, description, calories, proteins, carbs, fat, weight_in_g) VALUES
('Tostadas con aguacate', 'Pan integral con aguacate y semillas de chía.', 250, 6, 20, 14, 150),
('Pechuga a la plancha', 'Pechuga de pollo a la plancha con especias.', 300, 35, 0, 10, 180),
('Ensalada César', 'Ensalada con lechuga, pollo, aderezo y crutones.', 400, 20, 25, 18, 220),
('Yogur con frutas', 'Yogur natural con frutas frescas y miel.', 180, 8, 22, 5, 130),
('Arroz con leche', 'Postre típico con arroz, leche y canela.', 320, 7, 60, 6, 200);
('Omelette de espinaca', 'Huevos batidos con espinaca y queso bajo en grasa.', 210, 15, 3, 14, 120),
('Salmón al horno', 'Filete de salmón horneado con limón y eneldo.', 350, 30, 0, 22, 170),
('Ensalada de quinoa', 'Quinoa con tomate, pepino, garbanzos y aceite de oliva.', 280, 9, 38, 9, 200),
('Barra de cereal', 'Barra de avena, frutos secos y miel.', 150, 3, 25, 4, 40),
('Fruta fresca', 'Porción de frutas variadas de temporada.', 90, 1, 22, 0, 120),
('Tarta de manzana', 'Tarta casera de manzana con canela.', 270, 3, 45, 9, 100);


-- Tostadas con aguacate → Desayuno
INSERT INTO dish_categories (dish_id, category_id) VALUES (1, 1);

-- Pechuga a la plancha → Almuerzo y Cena
INSERT INTO dish_categories (dish_id, category_id) VALUES (2, 2), (2, 3);

-- Ensalada César → Almuerzo
INSERT INTO dish_categories (dish_id, category_id) VALUES (3, 2);

-- Yogur con frutas → Desayuno y Snack
INSERT INTO dish_categories (dish_id, category_id) VALUES (4, 1), (4, 4);

-- Arroz con leche → Postre
INSERT INTO dish_categories (dish_id, category_id) VALUES (5, 5);

-- Omelette de espinaca → Desayuno
INSERT INTO dish_categories (dish_id, category_id) VALUES (6, 1);

-- Salmón al horno → Almuerzo y Cena
INSERT INTO dish_categories (dish_id, category_id) VALUES (7, 2), (7, 3);

-- Ensalada de quinoa → Almuerzo
INSERT INTO dish_categories (dish_id, category_id) VALUES (8, 2);

-- Barra de cereal → Snack
INSERT INTO dish_categories (dish_id, category_id) VALUES (9, 4);

-- Fruta fresca → Desayuno y Snack
INSERT INTO dish_categories (dish_id, category_id) VALUES (10, 1), (10, 4);

-- Tarta de manzana → Postre
INSERT INTO dish_categories (dish_id, category_id) VALUES (11, 5);

--GOALS
CREATE TABLE goal_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    goal_value NUMERIC(5,2) NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

--TRAINER
CREATE TABLE trainer_client (
    client_id INT PRIMARY KEY,
    trainer_id INT NOT NULL,
    CONSTRAINT fk_client FOREIGN KEY (client_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_trainer FOREIGN KEY (trainer_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE client_dishes (
    client_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    PRIMARY KEY (client_id, dish_id),
    FOREIGN KEY (client_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE
);

CREATE TABLE client_exercises (
    client_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    PRIMARY KEY (client_id, exercise_id),
    FOREIGN KEY (client_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id) ON DELETE CASCADE
); 


--NOTIFICATIONS
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