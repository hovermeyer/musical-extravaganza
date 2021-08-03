import csv
import os
import re

from datetime import datetime, timezone

MUSICAL = "Hamilton"
# MUSICAL = "Joseph"
DATA_DIR = os.path.join("data", MUSICAL)
RAW_DIRECTORY = os.path.join(DATA_DIR, "raw")
MANUAL_DIRECTORY = os.path.join(DATA_DIR, "manual")
BY_LINE_DIRECTORY = os.path.join(DATA_DIR, "by-line")
BY_WORD_DIRECTORY = os.path.join(DATA_DIR, "by-word")
SYNONYM_DIRECTORY = os.path.join(DATA_DIR, "synonyms")
MANUAL_SYNONYM_FILE = os.path.join(DATA_DIR, "synonyms", "manual_synonyms.csv")
UNKNOWN_WORD_LIST = os.path.join(DATA_DIR, "unknown.txt")

def sort_key(filepath):
  match = re.match(r'^\d+', filepath)
  return int(match.group(0)) if match else 0

def sort_numerically(filepaths):
  return sorted(filepaths, key=sort_key)

def load_synonyms():
  latest = None
  for parent, _dirs, files in os.walk(SYNONYM_DIRECTORY):
    if len(files) > 0:
      latest = os.path.join(parent, sorted(files)[-1])

  synonyms = {}
  if latest:
    print(f"Loading data from previous run: `{latest}`")
    with open(latest, 'r') as csvfile:
      reader = csv.reader(csvfile)
      for raw, normalized in reader:
        synonyms[raw] = normalized
    print(f"Loaded {len(synonyms)} synonym pairs")
  else:
    print(f"No previous file found. Starting fresh")

  if os.path.exists(MANUAL_SYNONYM_FILE):
    with open(MANUAL_SYNONYM_FILE, 'r') as csvfile:
      reader = csv.reader(csvfile)
      for raw, normalized in reader:
        synonyms[raw] = normalized

  return synonyms

def update_unknown_words_file(unknown_words):
  with open(UNKNOWN_WORD_LIST, 'w') as fout:
    for word in sorted(unknown_words):
      fout.write(f"{word}\n")

def save_synonyms(synonyms):
  filepath = os.path.join(SYNONYM_DIRECTORY, f"{datetime.now(timezone.utc).isoformat(timespec='seconds')}_synonyms.csv")
  print(f"Saving {len(synonyms)} synonym pairs to `{filepath}`")
  with open(filepath, 'w') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    for raw, normalized in synonyms.items():
      writer.writerow([raw, normalized])
