"""
Sutra Collector — gathers Buddhist texts and metadata for a specific teacher.

Orchestrates FoJin Bridge calls to collect:
1. Teacher's KG entity and relations (lineage, school, texts)
2. Core texts associated with the teacher
3. Text content (selected juans)
4. Dictionary terms related to the teacher's tradition
"""

import json
import os
from typing import Optional

from fojin_bridge import FojinBridge, create_bridge


def collect_teacher_data(
    teacher_name: str,
    tradition: Optional[str] = None,
    bridge: Optional[FojinBridge] = None,
) -> dict:
    """Collect all available data about a teacher from FoJin."""
    if bridge is None:
        bridge = create_bridge()

    result = {
        "entity": None,
        "lineage": [],
        "texts": [],
        "content_samples": [],
        "terms": [],
    }

    # Step 1: Find teacher in KG
    kg_results = bridge.search_kg_entities(teacher_name, entity_type="person")
    if kg_results.get("results"):
        entity = kg_results["results"][0]
        result["entity"] = entity
        detail = bridge.get_kg_entity(entity["id"])
        result["entity"] = detail
        for rel in detail.get("relations", []):
            if rel["predicate"] in (
                "teacher_of", "student_of", "lineage_holder",
                "transmitted_to", "received_from",
            ):
                result["lineage"].append(rel)

    # Step 2: Search for associated texts
    text_results = bridge.search_texts(teacher_name, size=50)
    if text_results.get("results"):
        result["texts"] = text_results["results"]

    # Step 3: Collect content samples from top texts
    for text in result["texts"][:5]:
        text_id = text.get("id")
        if not text_id:
            continue
        try:
            content = bridge.get_text_content(text_id, juan_num=1)
            result["content_samples"].append({
                "text_id": text_id,
                "title": text.get("title_zh", ""),
                "content": content.get("content", "")[:3000],
            })
        except Exception:
            continue

    # Step 4: Collect tradition-specific terms
    if tradition:
        tradition_terms = {
            "汉传": ["净土", "禅", "般若", "菩提", "念佛"],
            "南传": ["vipassana", "satipatthana", "anicca", "dukkha", "anatta"],
            "藏传": ["菩提道次第", "空性", "菩提心", "止观", "三主要道"],
        }
        for term in tradition_terms.get(tradition, []):
            dict_results = bridge.search_dictionary(term, size=5)
            if dict_results.get("results"):
                result["terms"].extend(dict_results["results"])

    return result


def collect_specific_texts(
    cbeta_ids: list,
    bridge: Optional[FojinBridge] = None,
) -> list:
    """Collect full content for specific texts by CBETA ID."""
    if bridge is None:
        bridge = create_bridge()

    texts = []
    id_map = bridge.lookup_cbeta_ids(",".join(cbeta_ids))

    for cbeta_id, text_id in id_map.items():
        if not text_id:
            continue
        text_meta = bridge.get_text(text_id)
        juan_list = bridge.get_text_juans(text_id)

        text_data = {
            "cbeta_id": cbeta_id,
            "text_id": text_id,
            "title": text_meta.get("title_zh", ""),
            "juans": [],
        }

        for juan in juan_list.get("juans", [])[:10]:
            content = bridge.get_text_content(text_id, juan["juan_num"])
            text_data["juans"].append({
                "juan_num": juan["juan_num"],
                "content": content.get("content", ""),
            })

        texts.append(text_data)

    return texts


def save_collected_data(data: dict, output_path: str) -> str:
    """Save collected data to JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return os.path.abspath(output_path)
