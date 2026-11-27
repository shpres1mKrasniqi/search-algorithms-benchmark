import csv

from ner_extract import extract_entities, filter_entities, save_entities_csv


def test_filter_entities_removes_duplicates_low_scores_and_short_names():
    raw_entities = [
        {"word": "Berlin", "entity_group": "LOC", "score": 0.99},
        {"word": "Berlin", "entity_group": "LOC", "score": 0.95},
        {"word": "Google", "entity_group": "ORG", "score": 0.91},
        {"word": "AI", "entity_group": "ORG", "score": 0.99},
        {"word": "Unknown", "entity_group": "MISC", "score": 0.99},
        {"word": "London", "entity_group": "LOC", "score": 0.89},
    ]

    assert filter_entities(raw_entities) == {
        ("Berlin", "LOC"),
        ("Google", "ORG"),
    }


def test_extract_entities_chunks_and_deduplicates():
    calls = []

    def fake_ner(chunk, batch_size):
        calls.append((chunk, batch_size))
        return [
            [{"word": "Paris", "entity_group": "LOC", "score": 0.99}],
            [{"word": "Apple", "entity_group": "ORG", "score": 0.95}],
        ]

    entities = extract_entities(["one", "two", "three"], fake_ner)

    assert entities == [("Apple", "ORG"), ("Paris", "LOC")]
    assert len(calls) == 1


def test_save_entities_csv(tmp_path):
    output = tmp_path / "entities.csv"
    entities = [("Berlin", "LOC"), ("Google", "ORG")]

    save_entities_csv(entities, str(output))

    with output.open(newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    assert rows == [
        ["label", "type"],
        ["Berlin", "LOC"],
        ["Google", "ORG"],
    ]
