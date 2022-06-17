
import re
import json
import math
import datetime
import argparse
import collections
import dataclasses
import typing
from typing import List, Set

from tqdm import tqdm
# import nltk


LINE_RE = r'\[(?P<day>\d+)\.(?P<month>\d+)\.(?P<year>\d+), (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)] (?P<sender>[^:]+): (?P<body>.+)$'
CONVESATION_BREAK_SECONDS = 90*60

BAD_WORDS = ['Sicherheitsnummer', 'Nachricht']

MAKE_READABLE = False


@dataclasses.dataclass
class Message:
    timestamp: datetime.datetime
    sender: str
    body: str


@dataclasses.dataclass
class Conversation:
    start: datetime.datetime
    end: datetime.datetime
    messages: List[Message] = dataclasses.field(default_factory=list)
    participants: Set[str] = dataclasses.field(default_factory=set)
    words: List[str] = dataclasses.field(default_factory=list)
    top_words: List[str] = dataclasses.field(default_factory=list)


def extract_words(conversation: Conversation):
    words: List[str] = []
    for message in conversation.messages:
        words.extend(word for word in nltk.tokenize.word_tokenize(
            message.body) if word.isalpha())
    conversation.words = words


def process_tfidf(conversations: List[Conversation]):
    word_to_document_count: typing.Counter[str] = collections.Counter()
    for conversation in conversations:
        for word in set(conversation.words):
            word_to_document_count[word] += 1
    num_conversations = len(conversations)
    for conversation in conversations:
        word_counts = collections.Counter(conversation.words)
        word_to_tfidf = {}
        for word, tf in word_counts.items():
            idf = math.log10(num_conversations / word_to_document_count[word])
            tfidf = tf * idf
            word_to_tfidf[word] = tfidf
        conversation.top_words = sorted(
            word_to_tfidf, key=lambda word: word_to_tfidf[word], reverse=True)[:10]


class ConvesationEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Message, Conversation)):
            return dataclasses.asdict(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def analyze(filename, output_filename):
    messages = []
    last_message_timestamp = None

    conversations: List[Conversation] = []
    with open(filename, 'r') as f:
        for i, line in enumerate(tqdm(f)):
            if any(word.lower() in line.lower() for word in BAD_WORDS):
                continue
            match = re.match(LINE_RE, line)
            if not match:
                continue
            g = match.groupdict()
            if g['sender'] in ['CTOs']:
                continue
            timestamp = datetime.datetime(
                int(g['year']), int(g['month']), int(g['day']), int(g['hour']), int(g['minute']), int(g['second']))
            message = Message(timestamp, g['sender'], g['body'])
            messages.append(message)
            # if (not conversations) or (message.timestamp - conversations[-1].end).total_seconds() > CONVESATION_BREAK_SECONDS:
            #     conversations.append(Conversation(
            #         start=message.timestamp, end=message.timestamp))
            # conversations[-1].messages.append(message)
            # conversations[-1].participants.add(message.sender)

    # for conversation in conversations:
    #     extract_words(conversation)
    # process_tfidf(conversations)
    with open(output_filename, 'wb') as f:
        f.write(json.dumps(messages,
                           cls=ConvesationEncoder, indent=4).encode('utf8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store')
    parser.add_argument('output', action='store')
    args = parser.parse_args()
    analyze(args.filename, args.output)


if __name__ == '__main__':
    main()
