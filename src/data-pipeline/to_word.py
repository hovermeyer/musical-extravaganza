import os
import re
import sys

import unidecode

from xml.etree import ElementTree

from utils import BY_LINE_DIRECTORY, BY_WORD_DIRECTORY, sort_numerically, load_synonyms

                          # Initialism    | Regular word
VALID_WORD = re.compile(r'([A-Za-z0-9]\.){2,}|([A-Za-z0-9][A-Za-z0-9\'’]*)?[A-Za-z0-9]+')

SYNONYMS = load_synonyms()

def normalize(word):
  normalized_word = unidecode.unidecode(word)
  normalized_word = normalized_word.lower()
  normalized_word = re.sub(r'[^a-z0-9]', '', normalized_word)
  normalized_word = SYNONYMS.get(normalized_word, normalized_word)
  return normalized_word

def decode(content):
  decoded_content = unidecode.unidecode(content.replace('—', '-').replace('…', ' '))
  assert len(content) == len(decoded_content), f"Decoded content is not the same length: {repr(content)} ({len(content)}) -> {repr(decoded_content)} ({len(decoded_content)})"
  return decoded_content

def regex_partition(content, separator):
  decoded_content = decode(content)
  separator_match = re.search(separator, decoded_content)
  if not separator_match:
    return content, '', ''

  matched_separator = content[separator_match.start():separator_match.end()]
  parts = content.split(matched_separator, 1)

  return parts[0], matched_separator, parts[1]

def detokenize(results):
  return ''.join([x.text for x in results])

def make_element(tag, text, attrs=None):
  attrs = attrs or {}
  element = ElementTree.Element(tag, attrs)
  element.text = text
  return element

def tokenize(line):
  results = []

  pre_word, word, rest = regex_partition(line, VALID_WORD)
  if pre_word:
    results.append(make_element('p', pre_word))
  if word:
    results.append(make_element('word', word, { "normalized": normalize(word) }))
  while rest:
    pre_word, word, rest = regex_partition(rest, VALID_WORD)
    if pre_word:
      results.append(make_element('p', pre_word))
    if word:
      results.append(make_element('word', word, { "normalized": normalize(word) }))

  if detokenize(results) != line:
    print(detokenize(results))
    print(line)
    import pdb
    pdb.set_trace()
  return results

def process_line(line):
  input = line.text
  line.text = ''
  for child in tokenize(input):
    line.append(child)

def process_file(filepath):
  print(f"Processing `{filepath}`")

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
      process_line(child)
  output_path = os.path.join(BY_WORD_DIRECTORY, os.path.basename(filepath))
  new_root = ElementTree.ElementTree(root)
  new_root.write(output_path)

def go(files_to_process):
  try:
    for filepath in files_to_process:
      process_file(filepath)
  finally:
    print("Done!")

if __name__ == "__main__":
  if len(sys.argv) == 1:
    files_to_process = [os.path.join(parent, file) for parent, _dirs, files in os.walk(BY_LINE_DIRECTORY) for file in sort_numerically(files) if file.endswith(".xml")]
    go(files_to_process)
  elif len(sys.argv) == 2:
    filepath = sys.argv[1]
    go([filepath])
