import os
import re
import sys

import unidecode

from xml.etree import ElementTree

from utils import BY_WORD_DIRECTORY, SYNONYM_DIRECTORY, load_synonyms, save_synonyms, update_unknown_words_file, sort_numerically

ENGLISH_WORD_LIST = os.path.join("data", "words_alpha.txt")

def load_word_list():
  print(f"Loading English word list")
  with open(ENGLISH_WORD_LIST, 'r') as fin:
    words = set((line.strip() for line in fin))
  print(f"Loaded {len(words)} English words")
  return words

def save_session(synonyms, unknown_words):
  save_synonyms(synonyms)
  update_unknown_words_file(unknown_words)

def known_word(word, synonyms, english_word_list):
  return word in synonyms or word in english_word_list

def check_normalized_word(normalized_word, synonyms, english_word_list):
  if known_word(normalized_word, synonyms, english_word_list):
    return normalized_word

  normalized_word_with_g = normalized_word + 'g'
  if known_word(normalized_word_with_g, synonyms, english_word_list):
    return normalized_word

  return None

def process_line(line, synonyms, english_word_list):
  unknown_words = set()
  for word in line.iter('word'):
    normalized = word.attrib["normalized"]
    found = check_normalized_word(normalized, synonyms, english_word_list)
    if not found:
      unknown_words.add(normalized)
  return synonyms, unknown_words

def process_file(filepath, synonyms, english_word_list):
  print(f"Processing `{filepath}`")

  unknown_words = set()
  with open(filepath, 'r') as fin:
    contents = fin.read()
    root = ElementTree.fromstring(contents)
    sections = root.find('sections')
    if sections is None:
      print(f"WARN: Couldn't find <sections> in `{filepath}`")
      return
    for child in sections:
      if child.tag != 'line':
        continue
      synonyms, unknowns = process_line(child, synonyms, english_word_list)
      unknown_words = unknown_words.union(unknowns)
  return unknown_words

def go(files_to_process):
  synonyms = load_synonyms()
  english_word_list = load_word_list()

  unknown_words = set()
  try:
    for filepath in files_to_process:
      unknown_words = unknown_words.union(process_file(filepath, synonyms, english_word_list))
    print(f"Found {len(unknown_words)} unknown words")
    print(sorted(unknown_words))

  finally:
    save_session(synonyms, unknown_words)
    print("Done!")

if __name__ == "__main__":
  if len(sys.argv) == 1:
    files_to_process = [os.path.join(parent, file) for parent, _dirs, files in os.walk(BY_WORD_DIRECTORY) for file in sort_numerically(files) if file.endswith(".xml")]
    go(files_to_process)
  elif len(sys.argv) == 2:
    filepath = sys.argv[1]
    go([filepath])
