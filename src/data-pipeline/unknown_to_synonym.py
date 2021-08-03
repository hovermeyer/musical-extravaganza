import re
import sys

from utils import UNKNOWN_WORD_LIST, load_synonyms, save_synonyms

CHOICES = {
  'a': 'Answer',
  'n': 'Skip',
  'y': 'Ok',
  '?': 'Help',
}

def print_help():
  print(CHOICES)

def answer(word):
  answer = None
  print(f"What is word?: `{word}`")
  try:
    answer = sys.stdin.readline().strip()
  except KeyboardInterrupt:
    pass
  return answer

def normalize_word(word):
  return word.lower()

def process_unknown_word(word, synonyms):
  choice = None
  while not choice in CHOICES:
    choice = input(f"What do you want to do about?: `{word}` ({ '/'.join(CHOICES.keys()) })\n").strip()

  if choice == 'a':
    entered_word = answer(word)
    if entered_word:
      normalized_word = normalize_word(entered_word)
      synonyms[word] = normalized_word
  elif choice == 'y':
    synonyms[word] = word
  elif choice == '?':
    print_help()

  return synonyms

def main():
  synonyms = load_synonyms()
  try:
    with open(UNKNOWN_WORD_LIST, 'r') as fin:
      for word in [word.strip() for word in fin]:
        if word in synonyms:
          continue
        synonyms = process_unknown_word(word, synonyms)
  finally:
    save_synonyms(synonyms)



if __name__ == "__main__":
  main()
