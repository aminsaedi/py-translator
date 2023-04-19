import json
from deep_translator import GoogleTranslator


# read ./dist/enums/en-US.json

with open('./dist/enums/en-US.json', 'r') as f:
    enums = json.load(f)

# translate the values to hebrew,french,farsi and save them in ./dist/enums/he-IL.json,./dist/enums/fr-CA.json,./dist/enums/fa-IR.json

for lang in ['hebrew', 'fr-CA', 'fa-IR']:
    translations = GoogleTranslator(source="en", target=lang.split(
        '-')[0]).translate_batch(list(enums.values()))
    with open(f'./dist/en2/{lang}.json', 'w') as f:
        json.dump(dict(zip(enums.keys(), translations)),
                  f, indent=4, ensure_ascii=False)
