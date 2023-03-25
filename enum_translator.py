import json
from deep_translator import GoogleTranslator
import re


def normalizer(text):
    # split the string into words using underscores as separators
    words = text.split('_')

    # capitalize the first letter of each word and convert the rest to lowercase
    output_str = ' '.join([word.capitalize() for word in words])

    return output_str


def translate_enum_block(enums_list, target_lang):
    # Create a dictionary to store the translated enums
    translated_enums = {}

    # read current language file if it exists do not translate
    try:
        with open(f'./dist/enums/{target_lang}.json', 'r') as f:
            translated_enums = json.load(f)
    except FileNotFoundError:
        pass

    # Loop through each enum block and translate the values
    for enum_block in enums_list:
        # Extract the enum name and values
        enum_lines = enum_block.strip().split('\n')
        enum_name = enum_lines[0].split(' ')[1]
        enum_values = [line.strip().replace('_', ' ')
                       for line in enum_lines[1:-1] if line.strip()]

        if target_lang != 'en':
            translations = GoogleTranslator(
                source="en", target=target_lang).translate_batch(enum_values)
        else:
            # use normalizer to capitalize the first letter of each word
            translations = [normalizer(value) for value in enum_values]

        print(translations)

        for value, translation in zip(enum_values, translations):
            if value not in translated_enums:
                translated_enums[value] = translation

    return translated_enums


# Read the input file containing the enums
with open('./input_files/enums.txt', 'r') as file:
    enums_str = file.read()

# Split the input file into separate enum blocks
enums_list = re.findall(r'enum\s+\w+\s*{.*?}', enums_str, re.DOTALL)


print("Enter the target language code (e.g. 'fr' for French):")
target_lang = input()

result = translate_enum_block(enums_list, target_lang)

# Output the translated enums as a JSON file
with open(f'./dist/enums/{target_lang}.json', 'w') as file:
    json.dump(result, file, indent=2, ensure_ascii=False)
