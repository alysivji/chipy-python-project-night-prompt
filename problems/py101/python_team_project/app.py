from __future__ import unicode_literals
import sys

from prompt_toolkit import prompt, AbortAction
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
import meetup.api
import statistics

def get_names():
    client = meetup.api.Client('3f6d3275d3b6314e73453c4aa27')

    rsvps=client.GetRsvps(event_id='239174106', urlname='_ChiPy_')
    member_id = ','.join([str(i['member']['member_id']) for i in rsvps.results])
    members = client.GetMembers(member_id=member_id)

    names = []
    for member in members.results:
        try:
            names.append(member['name'])
        except:
            pass # ignore those who do not have a complete profile

    return names


command_completer = WordCompleter(['add'], ignore_case=True)

entered_names = []
median_lines = None

def execute(command):
    if command.startswith('add'):
        name_lines = command.split('add ')[1]
        num_lines = name_lines.rsplit()[-1]
        name = name_lines.rsplit()[:-1]
        name_part = ' '.join(name)
        entered_names.append((name_part, num_lines))

    if command.startswith('list'):
        to_print = [f'{x[0]}, {x[1]}' for x in entered_names]
        print('People added so far:',*to_print, sep="\n")
        print('Number of people:',len(entered_names))

        median_lines = statistics.median([int(x[1]) for x in entered_names])
        print('Median line count:', median_lines)

    if command.startswith('teams'):
        median_lines = statistics.median(int([x[1]) for x in entered_names])
        newbies = [x[0] for x in entered_names if x[1] < median_lines]
        experienced = [x[0] for x in entered_names if x[1] >= median_lines]

        print('Newbies: ', newbies)
        print('Experienced: ', experienced)
    return "You issued:" + command


def main():
    history = InMemoryHistory()

    while True:
        try:
            text = prompt('> ',
                          completer=command_completer,
                          history=history,
                          on_abort=AbortAction.RETRY)
            messages = execute(text)

            print(messages)
        except EOFError:
            break  # Control-D pressed.

    print('GoodBye!')


if __name__ == '__main__':
    main()
