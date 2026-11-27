import csv
import os

from datasets import load_dataset
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "dslim/bert-base-NER")
DATASET_NAME = os.getenv("DATASET_NAME", "fancyzhx/ag_news")
NUM_ARTICLES = int(os.getenv("NUM_ARTICLES", "500"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "100"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "16"))
MIN_SCORE = float(os.getenv("MIN_SCORE", "0.90"))
KEEP_TYPES = {"PER", "ORG", "LOC"}


def load_articles(n=NUM_ARTICLES):
    dataset = load_dataset(DATASET_NAME, split=f"train[:{n}]")
    return list(dataset["text"])


def build_ner_pipeline():
    return pipeline("ner", model=MODEL_NAME, aggregation_strategy="first")


def filter_entities(raw_entities):
    found = set()
    for entity in raw_entities:
        name = entity["word"].strip()
        entity_type = entity["entity_group"]

        if entity["score"] < MIN_SCORE:
            continue
        if entity_type not in KEEP_TYPES:
            continue
        if len(name) < 3:
            continue
        if not name[0].isalnum():
            continue

        found.add((name, entity_type))
    return found


def extract_entities(articles, ner):
    unique = set()
    for start in range(0, len(articles), CHUNK_SIZE):
        chunk = articles[start:start + CHUNK_SIZE]
        results = ner(chunk, batch_size=BATCH_SIZE)
        for raw_entities in results:
            unique |= filter_entities(raw_entities)
        print(f"Processed {min(start + CHUNK_SIZE, len(articles))}/{len(articles)} "
              f"articles, {len(unique)} unique entities so far")
    return sorted(unique)


def save_entities_csv(entities, path="data/entities.csv"):
    """Write unique entity names and types to a CSV for the Stardog pipeline."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["label", "type"])
        writer.writerows(entities)

    return path


if __name__ == "__main__":
    articles = load_articles()
    ner = build_ner_pipeline()
    entities = extract_entities(articles, ner)
    output_path = save_entities_csv(entities)

    print(f"\nFound {len(entities)} unique (name, type) pairs")
    print(f"Saved entities to {output_path}")
    for name, entity_type in entities[:15]:
        print(f"{entity_type:4} {name}")
