import json
from deep_translator import GoogleTranslator
import re
import os
from pprint import pprint

from excel_extractor import get_enums_flat_list


def get_source_lang(full_lang_code):
    """
    Get the source language from the full language code
    :param full_lang_code: full language code
    :return: source language
    """

    if full_lang_code == 'he-IL':
        return 'hebrew'

    return full_lang_code.split('-')[0]


def normalizer(text):
    # split the string into words using underscores as separators
    words = text.split('_')

    # capitalize the first letter of each word and convert the rest to lowercase
    output_str = ' '.join([word.capitalize() for word in words])

    return output_str


def translate_enum_block(target_lang):
    # Create a dictionary to store the translated enums
    translated_enums = {}

    # read current language file if it exists do not translate
    try:
        with open(f'./dist/enums/{target_lang}.json', 'r') as f:
            translated_enums = json.load(f)
    except FileNotFoundError:
        pass

    enums_list = get_enums_flat_list()

    without_underscores = [re.sub(r'_', ' ', enum) for enum in enums_list]

    if target_lang != 'en-US':
        translations = GoogleTranslator(
            source="en", target=get_source_lang(target_lang)).translate_batch(without_underscores)
    else:
        # use normalizer to capitalize the first letter of each word
        translations = [normalizer(value) for value in without_underscores]

    for value, translation in zip(enums_list, translations):
        if value not in translated_enums:
            translated_enums[value] = translation

    return translated_enums


def read_from_file(file_name):
    """
    Read the data from a json file
    :param file_name: name of the file to read from
    :return: dictionary of key value pairs
    """
    old_data = {}
    try:
        with open(f'./dist/enums/{file_name}.json') as f:
            old_data = json.load(f)
    except FileNotFoundError:
        print("File not found", f'./dist/{file_name}.json')
        pass  # create english file

    return old_data


print("Enter the target language code (e.g. 'fr-CA' for French):")
target_lang = input()

result = translate_enum_block(target_lang)
old_data = read_from_file(target_lang)


# merge the old and new data
result = {**old_data,  **result}

if not os.path.exists('./dist/enums'):
    os.makedirs('./dist/enums')
with open(f'./dist/enums/{target_lang}.json', 'w') as file:
    json.dump(result, file, indent=2, ensure_ascii=False)
