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

UNIQUE (method)
);

-- dish table contains list of dishes, categories, and key words
CREATE TABLE dish (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
contributor_id INTEGER NOT NULL,
method_id INTEGER NOT NULL,
image TEXT,
recipe_route TEXT,

UNIQUE (recipe_route),

FOREIGN KEY (contributor_id) REFERENCES contributor (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

FOREIGN KEY (method_id) REFERENCES method (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

-- ingredients table contains list of ingredients for shopping list
CREATE TABLE ingredient (
id INTEGER UNIQUE PRIMARY KEY NOT NULL,
dish_id INTEGER NOT NULL,
quantity REAL,
unit TEXT,
name TEXT NOT NULL,
notes TEXT,

UNIQUE (dish_id, name)

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
