import unittest

from to_line import parse_speaker_line

# speaker_line: speaker_list [ '(' except_list ')' ] ':'
# speaker_list: ( (name ',')* name [','] 'and') name
# except_list: '(' 'EXCEPT' speaker_list ')'
# item: name [ except_list ]
# name: r'(?:[A-Z\/\']+ )*(?:[A-Z\/\']+)'

class ParseSpeakerLineCase(unittest.TestCase):
  def test_non_speaker_line(self):
    self.assertIsNone(parse_speaker_line("How does a bastard, orphan, son of a whore and a"))

  def test_single_speaker(self):
    self.assertEqual("HAMILTON", parse_speaker_line("HAMILTON:"))

  def test_two_speakers(self):
    self.assertEqual("ELIZA and HAMILTON", parse_speaker_line("HAMILTON and ELIZA:"))

  def test_multi_speakers(self):
    self.assertEqual("ELIZA, HAMILTON, and PHILIP", parse_speaker_line("HAMILTON, PHILIP and ELIZA:"))

  def test_multi_speakers_with_oxford_comma(self):
    self.assertEqual("ELIZA, HAMILTON, and PHILIP", parse_speaker_line("HAMILTON, PHILIP, and ELIZA:"))

  def test_single_parenthetical(self):
    self.assertEqual("ELIZA, HAMILTON, and PHILIP (COMPANY)", parse_speaker_line("HAMILTON, PHILIP and ELIZA and (COMPANY):"))

  def test_two_parenthetical(self):
    self.assertEqual("ELIZA, HAMILTON, and PHILIP (LAFAYETTE and MULLIGAN)", parse_speaker_line("HAMILTON, PHILIP and ELIZA and (LAFAYETTE and MULLIGAN):"))

  def test_multi_parenthetical(self):
    self.assertEqual("ELIZA, HAMILTON, and PHILIP (BURR, LAFAYETTE, and MULLIGAN)", parse_speaker_line("HAMILTON, PHILIP and ELIZA and (LAFAYETTE, BURR and MULLIGAN):"))

  def test_single_exception_parenthetical(self):
    self.assertEqual("COMPANY (EXCEPT HAMILTON)", parse_speaker_line("COMPANY (EXCEPT HAMILTON):"))

  def test_two_exception_parenthetical(self):
    self.assertEqual("COMPANY (EXCEPT BURR and HAMILTON)", parse_speaker_line("COMPANY (EXCEPT BURR and HAMILTON):"))
    self.assertEqual("COMPANY (EXCEPT BURR)", parse_speaker_line("COMPANY (EXCEPT BURR):"))

  def test_multi_exception_parenthetical(self):
    self.assertEqual("COMPANY (EXCEPT BURR, HAMILTON, and LAFAYETTE)", parse_speaker_line("COMPANY (EXCEPT BURR, LAFAYETTE and HAMILTON):"))

  def test_both_parenthetical_and_exception(self):
    self.assertEqual("COMPANY (EXCEPT HAMILTON and WASHINGTON), ELIZA, and PHILIP (BURR, LAFAYETTE, and MULLIGAN)", parse_speaker_line("COMPANY (EXCEPT HAMILTON and WASHINGTON), PHILIP and ELIZA and (LAFAYETTE, BURR and MULLIGAN):"))


if __name__ == '__main__':
    unittest.main()
