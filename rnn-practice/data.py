"""
Part of Character-level RNN
To predict which language a name is from based on the spelling
Credit: http://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html
"""

import glob
import unicodedata
import string
import torch


all_letters = string.ascii_letters + " .,;'"
n_letters = len(all_letters)

# Build the category_lines dictionary, a list of names per language
category_lines = {}
all_categories = []

def findFiles(path):
    return glob.glob(path)

# print(findFiles('data/names/*.txt'))

# Turn a Unicode string to plain ASCII, thanks to http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
  return ''.join(
      c for c in unicodedata.normalize('NFD', s)
      if unicodedata.category(c) != 'Mn'
      and c in all_letters
    )
# print(unicodeToAscii('Ślusàrski'))

# read a file and split into lines
def readLines(filename):
    lines = open(filename, encoding='utf-8').read().strip().split('\n')
    return [unicodeToAscii(line) for line in lines]

for filename in findFiles('data/names/*.txt'):
    category = filename.split('/')[-1].split('.')[0]
    all_categories.append(category)
    lines = readLines(filename)
    category_lines[category] = lines

n_categories = len(all_categories)
# print(category_lines['Italian'][:5])

# Find letter index from all_letters, e.g. "a" = 0
def letterToIndex(letter):
    return all_letters.find(letter)

# Just for demonstration, turn a letter into a <1 x n_letters> Tensor
def letterToTensor(letter):
    tensor = torch.zeros(1, n_letters)
    tensor[0][letterToIndex(letter)] = 1
    return tensor

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor


if __name__ == '__main__':
    # print(letterToTensor('J'))
    # print(lineToTensor('JackJones').size())
    # print(n_categories)

    import random
    from torch.autograd import Variable
    category = random.choice(all_categories)
    print(Variable(torch.LongTensor([all_categories.index(category)])))
    