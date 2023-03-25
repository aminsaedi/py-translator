#! /usr/bin/env python3

import re
import sys
import json

legacy_messages = {}
try:
    with open('./input_files/legacy_messages.json') as f:
        legacy_messages = json.load(f)
except:
    pass


def camel_to_words(string):
    if string != '':
        result = re.sub('([A-Z])', r' \1', string)
        return result[:1].upper() + result[1:].lower()
    return


def fixer(matchobj):
    text = matchobj.group(0)
    path = text.split(".")
    word = path[-1]
    path = path[1:]

    # copy legacy messages to old_message
    old_message = legacy_messages

    while len(path) > 0:
        old_message = old_message.get(path[0])
        path.pop(0)

    # if type of old_message is string, then it is a legacy message

    # check legacy messages first

    description = ''
    if type(old_message) is str:
        description = " => ".join(text.split('.')[1:])

    word = camel_to_words(word)
    if type(old_message) is str:
        word = old_message
    return f"formatMessage({{ defaultMessage: '{word}', description: 'auto generated {description}'}})"


text_input = str(sys.stdin.read())


result = re.sub('messages\.(\w|\.)+\.\w+', fixer, text_input)
# print(result, file=sys.stdout)

# remove all unprintable characters
result = re.sub(r'[^\x20-\x7e]', r'', result)

sys.stdout.write(result)
