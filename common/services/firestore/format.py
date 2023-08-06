import copy
from datetime import date, datetime
from decimal import Decimal
import uuid

from pydantic import condecimal


def format_dict(dictionary):
    output_dictionary = copy.deepcopy(dictionary)

    for key, value in dictionary.items():
        if isinstance(value, dict):
            output_dictionary[key] = format_dict(value)

        elif isinstance(value, list):
            output_list = []
            for val in value:
                if isinstance(val, dict):
                    output_list += [format_dict(val)]
                elif isinstance(val, datetime) or isinstance(val, date):
                    output_list += [str(val)]
                else:
                    output_list += [val]
            output_dictionary[key] = output_list

        elif isinstance(value, date) or isinstance(value, datetime):
            output_dictionary[key] = str(value)

        elif isinstance(value, uuid.UUID):
            output_dictionary[key] = str(value)

        elif isinstance(value, Decimal):
            output_dictionary[key] = str(value)

    return output_dictionary
