import json
import getpass
import argparse

from tqdm import tqdm
from opensearchpy import OpenSearch

HOST = "search-cto-conversations-ko2mpbfa6rzjq65cw5w6xljxbm.us-east-1.es.amazonaws.com"
PORT = 443


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store')
    parser.add_argument('index', action='store')
    parser.add_argument('user', action='store')
    args = parser.parse_args()
    password = getpass.getpass('password: ')
    with open(args.filename, 'rb') as f:
        data = json.loads(f.read().decode('utf8'))
    client = OpenSearch(
        hosts=[{'host': HOST, 'port': PORT}],
        http_compress=True,  # enables gzip compression for request bodies
        http_auth=(args.user, password),
        use_ssl=True,
        verify_certs=True,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )

    for idx, conv in enumerate(tqdm(data)):
        client.index(
            index=args.index,
            body=conv,
            id=idx,
            refresh=True
        )


if __name__ == '__main__':
    main()
