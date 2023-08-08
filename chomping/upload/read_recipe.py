#!/usr/bin/env python

"""read_recipe.py: read and parse recipe from json format into memory"""

__author__ = "bolskie"
__copyright__ = "copyright 2023, Jack Briskie"

import pathlib
import json
from typing import Union


def read_recipe_file(recipe_name: str) -> dict:
    """read recipe from json file format to dictionary.

    :param recipe_name: file name of json recipe
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


def read_recipe_info(recipe_data: dict) -> dict:
    """read recipe information from raw json file data.

    :param recipe_data: dictionary of recipe data returned from read_recipe_file
    :returns: dictionary of recipe information
    """
    # read pertinent information from input data and store to output dictionary
    recipe_info = dict(
        contributor=recipe_data.get("contributorName"),
        method=recipe_data.get("cookingMethod"),
        title=recipe_data.get("recipeTitle"),
    )
    return recipe_info


def read_recipe_steps(recipe_data: dict) -> list:
    """read recipe steps and instructions from raw json file data.

    :param recipe_data: dictionary of recipe data returned from read_recipe_file
    :returns: list of recipe steps and instructions
    """
    # read pertinent information from data dictionary, stored natively as list
    recipe_steps = recipe_data.get("recipe")
    return recipe_steps


def find_ingredient_indices(recipe_step: str) -> Union[list[tuple, ...], None]:
    """find index locations of ingredients and quantities from a recipe step.

    :param recipe_step: single value of recipe steps list output from read_recipe_steps
    :returns: index of ingredient locations as a nested list of tuples
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

    # return results as list of tuples if they exist
    if ingredient_start_idx:
        output_idx = list(zip(ingredient_start_idx, ingredient_stop_idx))
    else:
        output_idx = None

    return output_idx


def get_ingredient_data(
    recipe_step: str, ingredient_bracket_indices: list[tuple, ...]
) -> list[tuple, ...]:
    """read one or more sets of ingredient and quantity data from a recipe step based on input index.

    :param recipe_step: single value of recipe steps list output from read_recipe_steps
    :param ingredient_bracket_indices: list of (start, stop) indices of ingredient location in string
    :returns: recipe value data stored as a nested list of tuples
    """
    ingredient_idx, ingredient_tuples = 0, []  # initialize loop index and storage list
    # select ingredient data from string based on index location
    while ingredient_idx < len(ingredient_bracket_indices):
        # slice recipe list from found bracket indices
        select_ingredient_data = recipe_step[
            ingredient_bracket_indices[ingredient_idx][0]
            + 1 : ingredient_bracket_indices[ingredient_idx][1]
        ]

        # find indices of semicolon characters
        first_semicolon_idx = select_ingredient_data.index(";")
        second_semicolon_index = (
            first_semicolon_idx
            + select_ingredient_data[first_semicolon_idx + 1 :].index(";")
            + 1
        )

        # select and format data separated by semicolons
        select_quantity = float(select_ingredient_data[0:first_semicolon_idx])
        select_unit = str(
            select_ingredient_data[first_semicolon_idx + 1 : second_semicolon_index]
        )
        select_ingredient_name = str(
            select_ingredient_data[second_semicolon_index + 1 :]
        )

        # append data to output list and iterate loop
        data_tuple = (select_quantity, select_unit, select_ingredient_name)
        ingredient_tuples.append(data_tuple)
        ingredient_idx += 1

    return ingredient_tuples
