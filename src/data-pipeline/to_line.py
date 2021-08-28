import os
import re
import sys

from utils import BY_LINE_DIRECTORY, MANUAL_DIRECTORY, MUSICAL, sort_numerically

import pyparsing as pp

NORMALIZED_SPEAKER_NAMES = {
  'Hamilton': {
    'COMPANY': 'Company',
    'FULL COMPANY': 'Company',
    'MALE COMPANY': 'Male Company',
    'EXCEPT': 'except',

    'FULL ENSEMBLE': 'Ensemble',
    'ENSEMBLE': 'Ensemble',
    'ENSEMBLE MEN': 'Ensemble Men',
    'ENSEMBLE WOMEN': 'Ensemble Women',
    'MALE ENSEMBLE': 'Male Ensemble',
    'MEN': 'Men',
    'WOMEN': 'Women',
    'ALL MEN': 'All Men',
    'ALL WOMEN': 'All Women',

    'ENSEMBLE MAN': 'Ensemble Man',
    'ANOTHER ENSEMBLE MAN': 'Another Ensemble Man',

    'AARON BURR': 'Aaron Burr',
    'BURR': 'Aaron Burr',
    'ALEXANDER HAMILTON': 'Alexander Hamilton',
    'HAMILTON': 'Alexander Hamilton',
    'ALEXANDER HAMILTON': 'Alexander Hamilton',
    'JOHN LAURENS': 'John Laurens',
    'LAURENS': 'John Laurens',
    'JOHN LAURENS': 'John Laurens',
    'HERCULES MULLIGAN': 'Hercules Mulligan',
    'MULLIGAN': 'Hercules Mulligan',
    'MARQUIS DE LAFAYETTE': 'Marquis de Lafayette',
    'LAFAYETTE': 'Marquis de Lafayette',
    'GEORGE WASHINGTON': 'George Washington',
    'WASHINGTON': 'George Washington',
    'WASH': 'George Washington',
    'THOMAS JEFFERSON': 'Thomas Jefferson',
    'JEFFERSON': 'Thomas Jefferson',
    'JAMES MADISON': 'James Madison',
    'MADISON': 'James Madison',
    'ELIZA HAMILTON': 'Eliza Hamilton',
    'ELIZA': 'Eliza Hamilton',

    'ANGELICA SCHUYLER': 'Angelica Schuyler',
    'ANGELICA': 'Angelica Schuyler',
    'PEGGY': 'Peggy Schuyler',

    'LAURENS/PHILLIP': 'Laurens/Phillip',
    'LEE': 'Charles Lee',
    'KING GEORGE III': 'King George III',

    'PHILIP': 'Philip Hamilton',

    'MARIA REYNOLDS': 'Maria Reynolds',
    'MARIA': 'Maria Reynolds',
    'JAMES': 'James Reynolds',
    'MARTHA': 'Martha Washington',
    'DOLLY': 'Dolly Madison',
    'GEORGE': 'George Eacker',
    'SEABURY': 'Samuel Seabury',

    'DEEP VOICE': 'DEEP VOICE',
    'DOCTOR': 'Dr. David Hosack',

    'MULLIGAN/MADISON': 'Mulligan/Madison',
    'LAFAYETTE/JEFFERSON': 'Lafayette/Jefferson',
  },
  'Joseph': {
    'NAPHTALI': 'NAPHTALI',
    'REUBEN\'S WIFE': 'REUBEN\'S WIFE',
    'REUBEN': 'REUBEN',
    'ENSEMBLE': 'ENSEMBLE',
    'MALE ENSEMBLE': 'MALE ENSEMBLE',
    'CHILDREN': 'CHILDREN',
    'FEMALE ENSEMBLE': 'FEMALE ENSEMBLE',
    'NARRATOR': 'NARRATOR',
    'JOSEPH': 'JOSEPH',
    'JACOB': 'JACOB',
    'BROTHERS': 'BROTHERS',
  }
}

SHORT_SPEAKER_NAMES = {
  'Hamilton': {
    'Aaron Burr': 'Burr',
    'Alexander Hamilton': 'Hamilton',
    'John Laurens': 'Laurens',
    'Hercules Mulligan': 'Mulligan',
    'Marquis de Lafayette': 'Lafayette',
    'George Washington': 'Washington',
    'Thomas Jefferson': 'Jefferson',
    'James Madison': 'Madison',
    'Eliza Hamilton': 'Eliza',
    'Angelica Schuyler': 'Angelica',
    'Peggy Schuyler': 'Peggy',
    'Charles Lee': 'Lee',
    'Philip Hamilton': 'Philip',
    'Maria Reynolds': 'Maria',
    'James Reynolds': 'James',
    'Martha Washington': 'Martha',
    'Dolly Madison': 'Dolly',
    'George Eacker': 'Eacker',
    'Samuel Seabury': 'Seabury',
    'Dr. David Hosack': 'Doctor',
  }
}

PARENTHETICAL = re.compile(r'\(([^)]+)\)')

PARENTHETICAL_SPEAKERS = re.compile(r'\((?!EXCEPT)([^)]+)\)')

def to_sentence(speaker_list):
  speaker_list = sorted(speaker_list, key=lambda x: f'zzz{x}' if x.startswith("(") else x)
  if len(speaker_list) < 2:
    return ''.join(speaker_list)
  elif len(speaker_list) == 2:
    return f"{', '.join(speaker_list[0:-1])} and {speaker_list[-1]}"
  else:
    return f"{', '.join(speaker_list[0:-1])}, and {speaker_list[-1]}"

def normalize_speaker(speaker):
  names = NORMALIZED_SPEAKER_NAMES.get(MUSICAL, None)
  short_names = SHORT_SPEAKER_NAMES.get(MUSICAL, None)

  normalized_name = names[speaker] if names else speaker
  short_name = short_names.get(normalized_name, normalized_name) if short_names else normalized_name
  return short_name.upper()

speaker_list = pp.Forward()
name = pp.Regex(r'(?:[A-Z\/\']+ )*(?:[A-Z\/\']+)')
exception_list = (pp.Suppress('(') + pp.Suppress('EXCEPT') + speaker_list + pp.Suppress(')'))
item = pp.Group(name.setResultsName("name") + pp.Optional(exception_list).setResultsName("exceptions"))
speaker_list <<= item + pp.Optional(
  pp.ZeroOrMore(pp.Suppress(',') + item) +
  pp.Optional(pp.Optional(pp.Suppress(',')) + pp.Suppress('and') + item)
)
parenthetical = (pp.Suppress('(') + speaker_list + pp.Suppress(')')).setResultsName("parenthetical")
speaker_line = speaker_list.setResultsName("speakers") + pp.Optional(pp.Optional(pp.Suppress('and')) + parenthetical) + pp.Suppress(':')

def format_name(name):
  return normalize_speaker(name)

def format_exception_list(list):
  return f" (EXCEPT {format_speaker_list(list)})" if len(list) > 0 else ""

def format_parenthetical_list(list):
  return f" ({format_speaker_list(list)})" if len(list) > 0 else ""

def format_item(item):
  return f"{format_name(item['name'])}{format_exception_list(item.get('exceptions', []))}"

def format_speaker_list(speaker_list):
  return to_sentence([format_item(item) for item in speaker_list])

def format_speaker_line(parsed):
  return f"{format_speaker_list(parsed['speakers'])}{format_parenthetical_list(parsed.get('parenthetical', []))}"

def parse_speaker_line(line):
  try:
    parsed = speaker_line.parseString(line, parseAll=True)
  except pp.ParseException:
    parsed = None

  if parsed:
    pass
  else:
    return None

  return format_speaker_line(parsed)

def normalize_parenthetical(speakers, line):
  try:
    parsed = speaker_line.parseString(speakers + ':', parseAll=True)
  except Exception as ex:
    import pdb
    pdb.set_trace()

  parenthetical_in_speakers = 'parenthetical' in parsed
  parenthetical_in_line = PARENTHETICAL.search(line)
  parenthetical_is_entire_line = parenthetical_in_line and re.sub(PARENTHETICAL, '', line).strip() == ''

  if parenthetical_in_speakers and not parenthetical_in_line:
    speakers = format_speaker_list(parsed['speakers'])
    return [speakers, line]
  elif parenthetical_in_speakers and parenthetical_is_entire_line:
    print(f"Warning: found parenthetical that is entire line. Is it concurrent?: {line}")
    return [format_speaker_list(parsed['parenthetical']), parenthetical_in_line.group(1)]
  else:
    return [speakers, line]

def dump_song(filepath, song):
  filename = os.path.basename(filepath)
  title = re.match(r'\d+ - (.*?)\.yml', filename).group(1)

  name, _ext = os.path.splitext(filename)
  output_path = os.path.join(BY_LINE_DIRECTORY, f"{name}.xml")

  with open(output_path, 'w') as fout:
    header = '<?xml version="1.0" encoding="UTF-8"?>\n' \
      '<?xml-model href="by-line.xsd"?>\n' \
      f'  <song title="{title}">\n' \
      '    <sections>\n'
    fout.write(header)

    previous_speakers = set()
    previous_speaker = None
    for speaker, line in song:
      if speaker in previous_speakers:
        speaker = SHORT_SPEAKER_NAMES.get(speaker, speaker)
      if speaker != previous_speaker:
        fout.write(f'      <line speaker="{speaker}" start-of-section="true">{line}</line>\n')
      else:
        fout.write(f'      <line speaker="{speaker}">{line}</line>\n')
      previous_speaker = speaker
      previous_speakers.add(speaker)
    footer = '    </sections>\n' \
      '  </song>\n'
    fout.write(footer)

def to_line_file(filepath):
  song = []

  speakers = None
  with open(filepath, 'r') as fin:
    for line in fin:
      line = line.strip()
      if line == '':
        continue
      is_speaker_line = parse_speaker_line(line)
      if is_speaker_line:
        speakers = is_speaker_line
        continue
      else:
        normalized_speakers, line = normalize_parenthetical(speakers, line)
        song.append([normalized_speakers, line])

  dump_song(filepath, song)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    for parent, _dirs, files in os.walk(MANUAL_DIRECTORY):
      for file in sort_numerically([file for file in files if file.endswith(".yml")]):
        filepath = os.path.join(parent, file)
        print(f"Processing `{filepath}`")
        to_line_file(filepath)
  elif len(sys.argv) == 2:
    filepath = sys.argv[1]
    to_line_file(filepath)
