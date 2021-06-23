import click
import itertools
import math
import pathlib
import pandas as pd

from tqdm import tqdm
from typing import Dict, Iterable, List, Set

import utils


def load_nested_values_from_csv(input_file: pathlib.Path,
                                extract_column: str) -> Set[str]:
    df = pd.read_csv(input_file, usecols=[extract_column])
    # dropping rows without value for extracted column
    df = df[df[extract_column].notna()]
    # converting string into list of values
    df[extract_column] = df[extract_column].apply(lambda x: eval(x))
    return set(itertools.chain(*df[extract_column].values))

def save_names_to_file(names: Iterable[str], filepath: pathlib.Path):
    names = [name.title().rsplit(' ', 1) for name in names]
    df = pd.DataFrame(names, columns=['firstname', 'lastname'])
    df.to_csv(filepath, index=False)


def delete_items_with_repeating_values(input_dict: Dict[str, Set[str]]) -> None:
    """ Deletes keys from input_dict which have common part in their value.
    Shorter keys are delete and longer are kept back """

    # total number of combinations: n! / r! / (n - r)!
    total_iters = math.factorial(len(input_dict)) \
                  / math.factorial(len(input_dict) - 2) / 2

    for name_a, name_b in tqdm(itertools.combinations(input_dict.keys(), 2),
                               total=total_iters):
        if name_a not in input_dict or name_b not in input_dict:
            continue
        if len(input_dict[name_a] & input_dict[name_b]):
            shorter_name = sorted([name_a, name_b], key=lambda s: len(s))[0]
            del input_dict[shorter_name]


def extract_unique_names(names: Set[str]) -> List[str]:
    # initial steps- normalizing all names
    names = set(map(str.lower, names))
    names = set(map(utils.all_whitespace_to_space, names))
    names = set(map(utils.delete_dots, names))

    # creating dict with normalized names as key
    # and set of name variants as value
    names_dict = {name: {name,
                         utils.delete_hyphen(name),
                         utils.convert_to_initials_form(name),
                         utils.convert_to_initial_name_and_surname(name)} for
                  name in names}

    delete_items_with_repeating_values(names_dict)
    return list(names_dict.keys())


@click.command()
@click.argument('input-file', type=click.Path(exists=True))
@click.argument('output-file', type=click.Path())
def main(input_file: str, output_file: str) -> None:
    """ Extracts unique authors from csv file\n
    :param input_file: Path to input file\n
    :param output_file: Path to output file\n
    """
    input_file = pathlib.Path(input_file)
    output_file = pathlib.Path(output_file)
    data = load_nested_values_from_csv(input_file, 'authors')
    unique_names = extract_unique_names(data)
    unique_names = sorted(map(str.title, unique_names))
    save_names_to_file(unique_names, output_file)


if __name__ == '__main__':
    main()
