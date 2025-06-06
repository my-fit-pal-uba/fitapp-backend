DROP TABLE IF EXISTS diet_dishes;
DROP TABLE IF EXISTS dish_categories;
DROP TABLE IF EXISTS dishes;
DROP TABLE IF EXISTS diet;
DROP TABLE IF EXISTS meal_categories;

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
    notes TEXT,
    CONSTRAINT fk_dishhistory_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_dishhistory_dish FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE RESTRICT
);
