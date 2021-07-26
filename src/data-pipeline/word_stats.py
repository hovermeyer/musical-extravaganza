import os
import re
import csv
import sys

from collections import Counter
from xml.etree import ElementTree

from utils import BY_WORD_DIRECTORY, DATA_DIR, sort_numerically

def process_file(filepath):
  print(f"Processing `{filepath}`")

  with open(filepath, 'r') as fin:
    contents = fin.read()
    root = ElementTree.fromstring(contents)
    words = [word.text for word in root.iter('word')]
    words_counter = Counter(words)
    normalized = [word.attrib['normalized'] for word in root.iter('word')]
    normalized_words_counter = Counter(normalized)
  return words_counter, normalized_words_counter

def go(files_to_process):
  all_words_counter = Counter([])
  all_normalized_words_counter = Counter([])
  try:
    for filepath in files_to_process:
      words_counter, normalized_words_counter = process_file(filepath)
      all_words_counter += words_counter
      all_normalized_words_counter += normalized_words_counter
    with open(os.path.join(DATA_DIR, "word_counts.csv"), 'w') as csvfile:
      writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
      for word, count in sorted(all_words_counter.items()):
        writer.writerow([word, count])
    with open(os.path.join(DATA_DIR, "normalized_word_counts.csv"), 'w') as csvfile:
      writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
      for word, count in sorted(all_normalized_words_counter.items()):
        writer.writerow([word, count])
  finally:
    print("Done!")

if __name__ == "__main__":
  if len(sys.argv) == 1:
    files_to_process = [os.path.join(parent, file) for parent, _dirs, files in os.walk(BY_WORD_DIRECTORY) for file in sort_numerically(files) if file.endswith(".xml")]
    go(files_to_process)
  elif len(sys.argv) == 2:
    filepath = sys.argv[1]
    go([filepath])
