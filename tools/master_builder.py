"""
Teacher Builder — orchestrates the full teacher skill generation pipeline.

Flow:
1. Collect data via sutra_collector
2. Analyze via prompt templates (sutra_analyzer + voice_analyzer)
3. Build via prompt templates (teaching_builder + voice_builder)
4. Write via skill_writer
"""

import json
import os
from typing import Optional

from fojin_bridge import FojinBridge, create_bridge
from sutra_collector import collect_teacher_data, collect_specific_texts
from skill_writer import create_teacher, DISCLAIMER


PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts")


def load_prompt(name: str) -> str:
    """Load a prompt template by name."""
    path = os.path.join(PROMPTS_DIR, f"{name}.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_analysis_prompt(
    template_name: str,
    teacher_name: str,
    data: dict,
) -> str:
    """Build a complete analysis prompt by filling template with collected data."""
    template = load_prompt(template_name)

    entity_info = ""
    if data.get("entity"):
        e = data["entity"]
        entity_info = f"名称: {e.get('name_zh', teacher_name)}\n"
        entity_info += f"类型: {e.get('entity_type', '未知')}\n"
        if e.get("description"):
            entity_info += f"描述: {e['description']}\n"
        if e.get("properties"):
            for k, v in e["properties"].items():
                entity_info += f"{k}: {v}\n"

    lineage_info = ""
    for rel in data.get("lineage", []):
        lineage_info += f"- {rel['predicate']}: {rel.get('target_name', '未知')}\n"

    texts_info = ""
    for t in data.get("texts", [])[:20]:
        texts_info += f"- 《{t.get('title_zh', '未知')}》({t.get('cbeta_id', '')})\n"

    content_samples = ""
    for sample in data.get("content_samples", []):
        content_samples += f"\n### 《{sample['title']}》\n{sample['content'][:2000]}\n"

    terms_info = ""
    for term in data.get("terms", [])[:30]:
        terms_info += f"- {term.get('headword', '')}: {term.get('definition', '')[:100]}\n"

    prompt = template.replace("{teacher_name}", teacher_name)
    prompt = prompt.replace("{entity_info}", entity_info)
    prompt = prompt.replace("{lineage_info}", lineage_info)
    prompt = prompt.replace("{texts_info}", texts_info)
    prompt = prompt.replace("{content_samples}", content_samples)
    prompt = prompt.replace("{terms_info}", terms_info)

    return prompt


def build_teacher_prompt(
    template_name: str,
    teacher_name: str,
    analysis_result: str,
) -> str:
    """Build a generation prompt from analysis results."""
    template = load_prompt(template_name)
    prompt = template.replace("{teacher_name}", teacher_name)
    prompt = prompt.replace("{analysis_result}", analysis_result)
    return prompt


def generate_teacher_skill(
    name: str,
    tradition: str,
    school: str,
    era: str,
    languages: list,
    teaching_content: str,
    voice_content: str,
    output_dir: str = "teachers",
    fojin_entity_id: Optional[str] = None,
    sources: Optional[list] = None,
) -> str:
    """Write the final teacher skill to disk."""
    base_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), output_dir
    )
    return create_teacher(
        base_dir=base_dir,
        name=name,
        tradition=tradition,
        school=school,
        era=era,
        languages=languages,
        teaching_content=teaching_content,
        voice_content=voice_content,
        fojin_entity_id=fojin_entity_id,
        sources=sources,
    )
