#!/usr/bin/env python

"""read_recipe.py: read recipe from json format into memory"""

__author__ = "bolskie"
__copyright__ = "copyright 2023, Jack Briskie"

import pathlib
import json


def read_recipe_file(recipe_name: str) -> dict:
    """read recipe from json file format to dictionary.

    :param recipe_name: file name of json recipe, input version 0.01
    :returns: dictionary of recipe steps
    """
    # determine path to recipe data
    main_directory = pathlib.Path(__file__).parent.resolve()
    data_directory = main_directory / "data"
    file_name = "".join((recipe_name, ".json"))
    file_path = data_directory / file_name

    # read recipe data from file
    with open(file_path) as json_file:
        recipe_dict = json.load(json_file)

    return recipe_dict
