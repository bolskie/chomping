-- chomping.db sqlite3 database schema
PRAGMA foreign_keys = ON;


-- contributor table contains recipe reviewers and data contributors
CREATE TABLE contributor (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
name TEXT NOT NULL,

UNIQUE (name)
);


-- method table contains families of recipes
CREATE TABLE method (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
method TEXT NOT NULL,
gear TEXT,

UNIQUE (method)
);


-- category table contains food categories for recipes
CREATE TABLE category (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
nationality TEXT,
type TEXT,

UNIQUE (nationality, type)
);


-- dish table contains list of dishes, categories, and key words
CREATE TABLE dish (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
contributor_id INTEGER,
category_id INTEGER,
method_id INTEGER,
image TEXT,
recipe_route TEXT,

UNIQUE (recipe_route),

FOREIGN KEY (contributor_id) REFERENCES contributor (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

FOREIGN KEY (category_id) REFERENCES category (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

FOREIGN KEY (method_id) REFERENCES method (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);


-- ingredients table contains list of ingredients for shopping list
CREATE TABLE ingredients (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
dish_id INTEGER NOT NULL,
quantity REAL,
unit TEXT,
ingredient TEXT NOT NULL,
notes TEXT,

UNIQUE (dish_id, ingredient)

FOREIGN KEY (dish_id) REFERENCES dish (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);


-- recipe table contains steps to cook dish
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


-- review table contains data on how long dishes take to cook, servings, and text reviews
CREATE TABLE review (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
dish_id INTEGER NOT NULL,
contributor_id INTEGER NOT NULL,
prep_time INTEGER,
cook_time INTEGER,
total_time INTEGER,
servings INTEGER,
rating INTEGER,
review TEXT,

FOREIGN KEY (dish_id) REFERENCES dish (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);
