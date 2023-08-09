-- insert_int_ingredient_recipe_step.sql
-- insert data into intermediary table linking recipe steps and ingredients

INSERT INTO int_ingredient_recipe_step (
recipe_id,
ingredient_id,
brackets_number
) VALUES (?, ?, ?)
;




-- intermediary table to link recipe steps to ingredients
CREATE TABLE int_ingredient_recipe_step (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
recipe_id INTEGER NOT NULL,
ingredient_id iNTEGER NOT NULL,
string_position INTEGER,

UNIQUE (recipe_id, ingredient_id),

FOREIGN KEY (recipe_id) REFERENCES recipe (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

FOREIGN KEY (ingredient_id) REFERENCES ingredient (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);
