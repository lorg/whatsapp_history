import json
import argparse
import datetime
import collections


def analyze(filename, start):
    c = collections.Counter()
    with open(filename, 'r') as f:
        messages = json.load(f)
        if start is None:
            c.update(m['sender'] for m in messages)
        else:
            start = datetime.date.fromisoformat(start)
            c.update(m['sender'] for m in messages if datetime.datetime.fromisoformat(
                m['timestamp']).date() >= start)
    for sender, msg_counter in c.most_common():
        print(f'{sender}: *{msg_counter}*')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store')
    parser.add_argument('--start', action='store')
    args = parser.parse_args()
    analyze(args.filename, args.start)


if __name__ == '__main__':
    main()
