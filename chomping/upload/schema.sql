-- chomping.db sqlite3 database schema
PRAGMA foreign_keys = ON;

-- recipe contributors
CREATE TABLE contributor (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
name TEXT NOT NULL,

UNIQUE (name)
);

-- families of recipes to sort by gear
CREATE TABLE method (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
name TEXT NOT NULL,

UNIQUE (method)
);

-- list of dishes/meals
CREATE TABLE dish (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
contributor_id INTEGER NOT NULL,
method_id INTEGER NOT NULL,
recipe_route TEXT,
image TEXT,

UNIQUE (recipe_route),

FOREIGN KEY (contributor_id) REFERENCES contributor (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

FOREIGN KEY (method_id) REFERENCES method (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

-- list of ingredients for recipe display and shopping list
CREATE TABLE ingredient (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
quantity REAL,
unit TEXT,
name TEXT NOT NULL,

UNIQUE (quantity, unit, name)
);

-- steps to cook dish
CREATE TABLE recipe (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
dish_id INTEGER NOT NULL,
step INTEGER NOT NULL,
direction TEXT NOT NULL,
image TEXT,

UNIQUE (dish_id, step),

FOREIGN KEY (dish_id) REFERENCES dish (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

-- intermediary table to link recipe steps to ingredients
CREATE TABLE int_ingredient_recipe_step (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
recipe_id INTEGER NOT NULL,
ingredient_id iNTEGER NOT NULL,
brackets_number INTEGER,

UNIQUE (recipe_id, ingredient_id),

FOREIGN KEY (recipe_id) REFERENCES recipe (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

FOREIGN KEY (ingredient_id) REFERENCES ingredient (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);
