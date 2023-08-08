#!/usr/bin/env python

"""read_recipe.py: read recipe from json format into memory"""

__author__ = "bolskie"
__copyright__ = "copyright 2023, Jack Briskie"

import pathlib
import json


def read_recipe_file(recipe_name: str) -> dict:
    """read recipe from json file format to dictionary.

    :param recipe_name: file name of json recipe, input version 0.01
    :returns: dictionary of recipe data
    """
    # determine path to recipe data
    main_directory = pathlib.Path(__file__).parent.resolve()
    data_directory = main_directory / "data"
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
