import json
from deep_translator import GoogleTranslator
import os


def get_source_lang(full_lang_code):
    """
    Get the source language from the full language code
    :param full_lang_code: full language code
    :return: source language
    """

    if full_lang_code == 'he-IL':
        return 'hebrew'

    return full_lang_code.split('-')[0]


def read_from_file(file_name):
    """
    Read the data from a json file
    :param file_name: name of the file to read from
    :return: dictionary of key value pairs
    """
    old_data = {}
    try:
        with open(f'./dist/{file_name}.json') as f:
            old_data = json.load(f)
    except FileNotFoundError:
        print("File not found", f'./dist/{file_name}.json')
        pass  # create english file

    return old_data


def translate_all(source_data, target_lang):
    """
    Translate all the keys and values in the source_data dictionary to the target_lang
    :param source_data: dictionary of key value pairs
    :param target_lang: target language to translate to
    :return: translated dictionary
    """

    old_data = read_from_file(target_lang)

    translated_data = {}
    translator = GoogleTranslator(
        source='en', target=get_source_lang(target_lang))
    count = 1
    skip_count = 0
    translate_count = 0
    for key, value in source_data.items():

        if key in old_data:
            print("Already translated: " + str(count) + " of " +
                  str(len(source_data)) + f"  {old_data[key]} ")
            translated_data[key] = old_data[key]
            count += 1
            skip_count += 1
            continue

        translation = translator.translate(text=value)
        translated_data[key] = translation
        count += 1
        print("Translated: " + str(count) + " of " +
              str(len(source_data)) + f"  {translation} ")
        translate_count += 1
    print(f"""
    ==========================================
    Translated {translate_count} words
    Skipped {skip_count} words
    ==========================================
    Total: {translate_count + skip_count}
    ==========================================
    """)
    return translated_data


def write_to_file(data, file_name):
    """
    Write the data to a json file
    :param data: dictionary of key value pairs
    :param target_lang: target language to translate to
    :return: None
    """

    # create dist folder if it does not exist
    if not os.path.exists('./dist'):
        os.makedirs('./dist')

    # create english file
    with open('./dist/' + file_name + '.json', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


def update_default_language(extracted_data):
    # This section is for updating the english file (default language)
    old_english_data = read_from_file('en-US')
    # find all that exists in extracted_data but not in old_english_data
    new_words = {k: v for k, v in extracted_data.items()
                 if k not in old_english_data}
    # add new words to old_english_data
    old_english_data.update(new_words)
    # write to file
    write_to_file(old_english_data, 'en-US')


# read json file
with open('./input_files/en.json') as f:
    data = json.load(f)

    # loop through the map and print the key and value
    extracted_data = {}

    for key, value in data.items():
        # if value['defaultMessage'] contains { and } do not add to extracted_data
        if '{' not in value['defaultMessage'] and '}' not in value['defaultMessage']:
            extracted_data[key] = value['defaultMessage']

    # this section is for updating the english file (default language)
    update_default_language(extracted_data)

    print("Enter the full language code (e.g. en-US): ")
    target_lang = input()
    translated_data = translate_all(extracted_data, target_lang)
    write_to_file(translated_data, target_lang)
