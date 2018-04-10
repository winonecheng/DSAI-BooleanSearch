import csv
import re

eng_dict = dict()
ch2_dict = dict()
ch3_dict = dict()

def tokenize(str):
    eng_match = re.findall(r'[a-zA-Z]{2,}', str)
    ch2_match = re.findall(r'(?=([\u4e00-\u9fff]{2}))', str)
    ch3_match = re.findall(r'(?=([\u4e00-\u9fff]{3}))', str)
    return [eng_match, ch2_match, ch3_match]


def build_inverted_index(eng_match, ch2_match, ch3_match, index):
    for gram in ch2_match:
        if gram not in ch2_dict:
            ch2_dict[gram] = [index]
        else:
            ch2_dict[gram].append(index)

    for gram in ch3_match:
        if gram not in ch3_dict:
            ch3_dict[gram] = [index]
        else:
            ch3_dict[gram].append(index)

    for gram in eng_match:
        if gram not in eng_dict:
            eng_dict[gram] = [index]
        else:
            eng_dict[gram].append(index)


def bool_search(words, oper):
    index = list()
    for word in words:
        match = re.search('[a-zA-Z]', word)
        if match:
            index.append(eng_dict[word])
        elif len(word) == 2:
            index.append(ch2_dict[word])
        elif len(word) == 3:
            index.append(ch3_dict[word])
            
    if oper is 'and':
        return list(set(index[0]).intersection(*index[1:]))
    elif oper is 'or':
        return list(set(index[0]).union(*index[1:]))
    elif oper is 'not':
        return list(set(index[0]).difference(*index[1:]))


if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                       default='source.csv',
                       help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()

    with open(args.source, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        index = 1
        for row in reader:
            matches = tokenize(row[1])
            build_inverted_index(*matches, index)
            index += 1

    with open(args.query, 'r') as f:
        with open(args.output, 'w') as fout:
            for row in f.readlines():
                row = row.strip()
                if 'and' in row:
                    words = re.split(r' and ', row)
                    result = bool_search(words, 'and')

                elif 'or' in row:
                    words = re.split(r' or ', row)
                    result = bool_search(words, 'or')

                elif 'not' in row:
                    words = re.split(r' not ', row)
                    result = bool_search(words, 'not')

                if len(result) != 0:
                    fout.write(','.join([str(index) for index in sorted(result)]) + '\n')
                else:
                    fout.write('0\n')
            
            # Remove the last new line
            fout.seek(fout.tell()-1)
            fout.truncate()
