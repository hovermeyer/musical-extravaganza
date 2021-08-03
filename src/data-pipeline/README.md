# Usage

Requires Python 3.9.

Change `MUSICAL` in `utils.py` to the name of the musical you want to process.

```bash
pip install -r requirements.txt
python to_line.py && python to_word.py && python word_stats.py && python to_frontend.py && python synonym_tool.py && python synonym_tool.py
```

## Output

* `data/<musical>/<musical>.json`: A JSON file suitable for the front-end to consume.
* `data/<musical>/normalized_word_counts.csv`: A count of instances of each normalized word.
* `data/<musical>/word_counts.csv`: A count of instances of each word as it appears exactly in the source.
* `data/<musical>/unknown.txt`: A list of normalized words that did not match an entry in `data/words_alpha.txt`

# Data Formats

### `data/<musical>/manual`
A directory of `.yml` files that contain the lyrics as they appear on http://themusicallyrics.com/
One file per song. Filenames must be in the format `<index> - Song name.yml`, where index is the number of the song in the musical.
These are not actually YAML files, but the syntax highlighting works well with lyrics:

```yaml
AARON BURR:
How does a bastard, orphan, son of a whore and a
```

### `data/<musical>/by-line`
A directory of XML files (one per song) that describe the speaker and lines within the song

```xml
<line speaker="BURR" start-of-section="true">How does a bastard, orphan, son of a whore and a</line>
```

### `data/<musical>/by-word`
A directory of XML files (one per song) that expand on the `by-line` files, also describing the words and their normalized forms.

```xml
<line speaker="BURR" start-of-section="true"><word normalized="how">How</word><p> </p><word normalized="does">does</word><p> </p><word normalized="a">a</word><p> </p><word normalized="bastard">bastard</word><p>, </p><word normalized="orphan">orphan</word><p>, </p><word normalized="son">son</word><p> </p><word normalized="of">of</word><p> </p><word normalized="a">a</word><p> </p><word normalized="whore">whore</word><p> </p><word normalized="and">and</word><p> </p><word normalized="a">a</word></line>
```

### `data/<musical>/synonyms/<iso_datetime>.csv`

Sometimes, you want to override the word normalization to something that is easier to type (e.g. `practly` -> `practically`)
The scripts will load the latest datetime file in this directory and use it when normalizing words.

```csv
practly,practically
```

### `data/words_alpha.txt`
A English dictionary word list. Used to check the normalized versions of the words in order to generate `data/<musical>/unknown.txt`


