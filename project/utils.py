import os


class ValueNotSetException(Exception):
    pass


class IncorrectValueTypeException(Exception):
    pass


def get_variable_from_env(variable_name, iterable=False, boolean=False):
    """
    Attemps to get a variable value from a .env file, if the variable is not found,
    an exception is raised to warn the user.

    Parameters
    ----------
        variable_name: str
            The variable name for which the value is fetched

        iterable : bool
            Indicates wether to call another function to parse a comma separated string
            into an iterable.

        boolean : bool
            Indicates wether to call another function to parse a string into a boolean
            value.

    Returns
    -------
        string
            The value fetched from the .env file with the given variable name

    END
    ----
    """
    variable_from_env = os.getenv(variable_name)

    if iterable:
        return parse_comma_separated_string_into_list(variable_name, variable_from_env)

    if boolean:
        return parse_string_into_boolean(variable_name, variable_from_env)

    if variable_from_env is None:  # For when the value is not found on the .env file
        raise ValueNotSetException(
            f'You forgot to set the variable "{variable_name}" on your .env file. Set it with: "{variable_name} = SOME_VALUE"'
        )

    return variable_from_env


def parse_comma_separated_string_into_list(variable_name, variable_from_env):
    """
    Attemps to parse a comma separated string value from a variable on a .env file into a list

    If the variable is not found or isn't set properly (as a comma separated string), an exception
    is raised to warn the user.

    Parameters
    ----------
        variable_name: str
            The variable name for which the value is fetched

        variable_from_env : str
            The value of a variable defined in a .env file

    Returns
    -------
        list
            A list full with string values, like: ["value1", "value2", "value3]

    Examples
    --------
        Case 1:
            variable_from_env = "value1, value2, value3"
            returns: ["value1", "value2", "value"]

        Case 2:
            variable_from_env = None
            returns: ValueError

        Case 3:
            variable_from_env = Some other random string that isn't comma separated
            returns: AttributeError

    END
    ----
    """
    # TODO: Refatorar pra funcionar com iteráveis em geral, onde o usuario especifica
    # que tipo de iteravel deve ser gerado, padrão sendo uma lista

    if variable_from_env is None:  # For when the value is not found on the .env file
        raise ValueNotSetException(
            f'You forgot to set the variable "{variable_name}" on your .env file. Set it with: "{variable_name} = value1, value2, value3"'
        )

    if not isinstance(variable_from_env, str) or not "," in variable_from_env:
        raise IncorrectValueTypeException(
            f'The value of the {variable_name} variable on your .env must be a comma separated string, like for example: "value1, value2, value3..."'
        )
    return [string.strip() for string in variable_from_env.split(",")]


def parse_string_into_boolean(variable_name, variable_from_env):
    """
    Attemps to parse a string value from a variable on a .env file into a boolean value

    If the variable is not found or isn't set properly (as either "True" or "False) an exception
    is raised to warn the user.

    Parameters
    ----------
        variable_name: str
            The variable name for which the value is fetched

        variable_from_env : str
            The value of a variable defined in a .env file

    Returns
    -------
        bool
            A boolean value

    Examples
    --------
        Case 1:
            variable_from_env = "True"
            returns: True

        Case 2:
            variable_from_env = "False"
            returns: False

        Case 3:
            variable_from_env = None
            returns: ValueError

        Case 4:
            variable_from_env = Some other random string that isn't either "True" or "False"
            returns: AttributeError

    END
    ----
    """

    STRING_TO_BOOLEAN_VALUES = {"True": True, "False": False}

    if variable_from_env is None:  # For when the value is not found on the .env file
        raise ValueNotSetException(
            f'You forgot to set the variable "{variable_name}" on your .env file. Set it with: "{variable_name} = True" or "{variable_name} = False"'
        )

    if variable_from_env not in ["True", "False"]:
        raise IncorrectValueTypeException(
            f'The value of the "{variable_name}" variable on your .env must be a string of either "True" or "False"'
        )
    return STRING_TO_BOOLEAN_VALUES[variable_from_env]
