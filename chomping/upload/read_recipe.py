#!/usr/bin/env python

"""read_recipe.py: read recipe from json format into memory"""

__author__ = "bolskie"
__copyright__ = "copyright 2023, Jack Briskie"

import pathlib
import json
from typing import Union


def read_recipe_file(recipe_name: str) -> dict:
    """read recipe from json file format to dictionary.

    :param recipe_name: file name of json recipe, input version 0.01
    :returns: dictionary of recipe data
    """
    # determine path to recipe data
    this_directory = pathlib.Path(__file__).parent.resolve()
    data_directory = this_directory.parent.parent.resolve() / "data"
    file_name = "".join((recipe_name, ".json"))
    file_path = data_directory / file_name

    # read recipe data from file
    with open(file_path) as json_file:
        recipe_data = json.load(json_file)

    return recipe_data


def read_recipe_steps(recipe_data: dict) -> list:
    """read recipe steps and instructions from raw json file data.

    :param recipe_data: dictionary of recipe data returned from read_recipe_file
    :returns: list of recipe steps and instructions
    """
    # read pertinent information from data dictionary, stored natively as list
    recipe_steps = recipe_data.get("recipe")
    return recipe_steps


def get_ingredient_data(recipe_step: str) -> Union[list[tuple, ...], None]:
    """read one or more ingredients and quantities from a recipe step.

    :param recipe_step: single value of recipe steps list output from read_recipe_steps
    :returns: recipe value data stored as a nested tuple of tuples
    """
    # initialize loop indices and lists to store ingredient indices
    string_start_idx = 0
    ingredient_start_idx, ingredient_stop_idx = [], []

    # select ingredient indices from input string
    while string_start_idx < len(recipe_step):
        select_recipe_string = recipe_step[string_start_idx:]

        # find ingredient index via string match, catch error if no ingredient data is found
        try:
            each_ingredient_start_idx = select_recipe_string.index("{")
        except ValueError:
            break
        each_ingredient_stop_idx = select_recipe_string.index("}")

        # append each set of result indices to lists
        ingredient_start_idx.append(each_ingredient_start_idx)
        ingredient_stop_idx.append(each_ingredient_stop_idx)
        string_start_idx = each_ingredient_stop_idx  # set next search from ending index of this ingredient

    # read and format ingredient data from found string indices
    ingredient_idx, ingredient_tuples = 0, []  # initialize loop index and storage list
    print(ingredient_start_idx, ingredient_stop_idx)
    if ingredient_start_idx:
        # select ingredient data
        while ingredient_idx < len(ingredient_start_idx):
            ingredient_data_idx = 0
            # slice recipe list from found bracket indices
            select_ingredient_data = recipe_step[ingredient_start_idx[ingredient_idx] + 1: ingredient_stop_idx[ingredient_idx]]

            # find indices of semicolon characters
            first_semicolon_idx = select_ingredient_data.index(";")
            second_semicolon_index = first_semicolon_idx + select_ingredient_data[first_semicolon_idx + 1:].index(";") + 1

            # select and format data separated by indices
            select_quantity = float(select_ingredient_data[ingredient_data_idx: first_semicolon_idx])
            select_unit = str(select_ingredient_data[first_semicolon_idx + 1: second_semicolon_index])
            select_ingredient_name = str(select_ingredient_data[second_semicolon_index + 1:])

            # append data to output list and iterate loop
            data_tuple = (select_quantity, select_unit, select_ingredient_name)
            print(data_tuple)
            ingredient_tuples.append(data_tuple)
            ingredient_idx += 1

    # if no ingredients are found in the string search, return None
    else:
        ingredient_tuples = None

    return ingredient_tuples


if __name__ == "__main__":
    DATANAME = 'rigatoni_with_vodka_sauce'
    read_file = read_recipe_file(DATANAME)
    read_steps = read_recipe_steps(read_file)
    myStepTest = read_steps[3]
    read_ingreds = get_ingredient_data(myStepTest)
