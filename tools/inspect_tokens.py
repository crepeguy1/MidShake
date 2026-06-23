import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'python'))

from midshake_tokenizer import Tokenizer

def print_tokens(path):
    text = Path(path).read_text(encoding='utf-8')
    tokens = Tokenizer(text).tokenize()
    for t in tokens:
        print(t)

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('file', nargs='?', default='examples/functions.ms')
    args = p.parse_args()
    print_tokens(args.file)
