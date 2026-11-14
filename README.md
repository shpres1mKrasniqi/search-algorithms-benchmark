# search-algorithms-benchmark

Linear search vs. binary search, benchmarked on synthetic data and on entity names
extracted with a Hugging Face NER model and stored in a Stardog knowledge graph.

## Setup

Requires Python 3.13.

```
py -3.13 -m venv search
.\search\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS/Linux use `python3 -m venv search` and `source search/bin/activate`.

## Tests

```
pytest
```
