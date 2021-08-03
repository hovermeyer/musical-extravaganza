from collections import defaultdict
import json
import os
from to_word import normalize

from xml.etree import ElementTree

from utils import MUSICAL, DATA_DIR, BY_WORD_DIRECTORY, sort_numerically

def merge_word_lookups(w1, w2):
  for word, indices in w2.items():
    w1[word].extend(indices)
  return w1

def format_line(line, song_index, line_index):
  result = []
  words = []
  word_lookup = defaultdict(list)
  word_index = 0
  for child in line:
    if child.tag == "p":
      result.append(child.text)
    elif child.tag == "word":
      words.append(child.text)
      result.append(f"{{{word_index}}}")
      word_lookup[child.attrib["normalized"]].append((song_index, line_index, word_index))
      word_index += 1
    else:
      raise ValueError(f"Unknown tag: <{child.tag}>")
  # print("".join([child.text for child in line if child.tag == "p"]))
  return "".join(result), words, word_lookup

def process_line(line, song_index, line_index):
  format_string, words, word_lookup = format_line(line, song_index, line_index)
  result = {
    "speaker": line.attrib["speaker"],
    "format": format_string,
    "words": words,
  }
  if "start-of-section" in line.attrib:
    result["start-of-section"] = True
  return result, word_lookup

def process_file(filepath, song_index):
  with open(filepath, 'r') as fin:
    contents = fin.read()
  parsed = ElementTree.fromstring(contents)

  word_lookup = defaultdict(list)

  lines = []
  for line_index, line in enumerate(parsed.iter('line')):
    line, line_word_lookup = process_line(line, song_index, line_index)
    lines.append(line)
    word_lookup = merge_word_lookups(word_lookup, line_word_lookup)

  return {
    "title": parsed.attrib['title'],
    "lines": lines,
  }, word_lookup

def main(files_to_process):
  word_lookup = defaultdict(list)

  songs = []
  for song_index, file in enumerate(files_to_process):
    song, song_word_lookup = process_file(file, song_index)
    songs.append(song)
    word_lookup = merge_word_lookups(word_lookup, song_word_lookup)

  word_lookup = dict(word_lookup)

  result = {
    "Title": MUSICAL,
    "SongDetails": songs,
    "WordDetails": word_lookup,
  }

  output_filepath = os.path.join(DATA_DIR, f"{MUSICAL.lower()}.json")
  with open(output_filepath, 'w') as fout:
    json.dump(result, fout, indent=2)


if __name__ == "__main__":
  files_to_process = [os.path.join(parent, file) for parent, _dirs, files in os.walk(BY_WORD_DIRECTORY) for file in sort_numerically(files) if file.endswith(".xml")]
  main(files_to_process)
