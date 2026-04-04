# buddha-skill

An AgentSkills-standard generator for AI teaching personas based on historical Buddhist masters, powered by [FoJin](https://fojin.app) — a Buddhist text aggregation platform.

---

## Seriousness Statement

This project is built out of respect for Buddhist traditions. All persona content is generated faithfully from historical documents. It makes no doctrinal judgments and claims no sectarian authority. Generated content is intended for study and reference only. For formal practice guidance, please seek out a qualified teacher and rely on genuine, living instruction.

This project does not simulate any living religious leader.

---

## Features

- **Three pre-built teachers**: Theravada (Ajahn Chah), Chinese (Master Yinguang), Tibetan (Tsongkhapa) — ready to use out of the box
- **FoJin data bridge**: Connected to [fojin.app](https://fojin.app) with 503 data sources, 10K+ texts, 678K+ semantic embeddings, and a 31K-entity knowledge graph
- **AgentSkills standard**: Compliant with the AgentSkills specification; can be invoked as a sub-skill by other agents
- **Dual-mode output**: Each teacher generates both `teaching.md` (doctrinal system) and `voice.md` (teaching style)
- **Incremental evolution**: Existing teachers can be enhanced by appending new source texts via incremental merging
- **Version management**: Built-in versioning with timestamps, supporting rollback to any prior version

---

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Use a Pre-built Teacher

In any AgentSkills-compatible environment:

```
/ajahn-chah     — Ajahn Chah (Theravada · Thai Forest Tradition)
/yinguang       — Master Yinguang (Chinese Buddhism · Pure Land)
/tsongkhapa     — Tsongkhapa (Tibetan · Gelug School)
```

### Generate a Custom Teacher

```
/create-teacher Xunyun
```

Or use natural language:

```
Create a teaching persona for Master Xunyun
```

The system will guide you through a three-step intake, then automatically collect data from FoJin and generate the doctrinal analysis and style files.

---

## Pre-built Teachers

### Ajahn Chah (1918-1992)

A Thai Forest Tradition monk and one of the most influential Theravada teachers of the 20th century.
Known for direct, accessible meditation instruction using everyday analogies to explain impermanence, suffering, and non-self.
Primary sources: SuttaCentral Pali Canon, including Mahāsatipaṭṭhāna Sutta, Dhammacakkappavattana Sutta, and related core texts.
Invoke: `/ajahn-chah`

### Master Yinguang (1861-1940)

The 13th Patriarch of the Chinese Pure Land school and a central figure in its modern revival.
His writing is sincere and straightforward; he guided countless practitioners through correspondence, collected in the three volumes of the Yinguang Fashi Wenchao.
Primary sources: CBETA Chinese Buddhist Canon, including the Wenchao volumes and the three Pure Land sutras.
Invoke: `/yinguang`

### Tsongkhapa (ཙོང་ཁ་པ, 1357-1419)

Founder of the Gelug school of Tibetan Buddhism and one of the most systematically rigorous commentators in Buddhist history.
The Lam Rim Chen Mo constructs a complete graduated path integrating sutra and tantra with precise doctrinal clarity.
Primary sources: Lam Rim Chen Mo, sNgags Rim Chen Mo, Lam gTso rNam gSum, and related works.
Invoke: `/tsongkhapa`

---

## Architecture

```
User request
    │
    ▼
SKILL.md (AgentSkills entry point)
    │
    ├─ Pre-built teachers ────────────► prebuilt/{slug}/
    │                                        ├── SKILL.md
    │                                        ├── teaching.md
    │                                        ├── voice.md
    │                                        └── meta.json
    │
    └─ Custom generation
          │
          ├─ prompts/intake.md          (information intake)
          │
          ├─ tools/sutra_collector.py
          │       │
          │       └──► FoJin API ───► knowledge graph + semantic search + text
          │
          ├─ prompts/sutra_analyzer.md  (doctrinal analysis)
          ├─ prompts/voice_analyzer.md  (style analysis)
          ├─ prompts/teaching_builder.md
          ├─ prompts/voice_builder.md
          │
          ├─ tools/teacher_builder.py   (persona construction)
          ├─ tools/skill_writer.py      (file writing)
          └─ tools/version_manager.py  (version management)
                │
                ▼
          teachers/{slug}/
              ├── SKILL.md
              ├── teaching.md
              ├── voice.md
              └── meta.json
```

---

## Relationship to FoJin

[FoJin](https://fojin.app) is a Buddhist text aggregation platform integrating 503 data sources, 10K+ texts, 678K+ semantic vector embeddings, and a knowledge graph of 31K entities. It covers major corpora including CBETA Chinese Buddhist Canon, SuttaCentral Pali Canon and translations, and 84000 Tibetan Buddhist translations.

buddha-skill connects to the FoJin API via `tools/fojin_bridge.py` to enable:

- Knowledge graph entity retrieval (teacher biography, lineage, school)
- Semantic similarity search (doctrinally relevant sutras)
- Source passage extraction with provenance tracking

All citations include traceable FoJin links to ensure transparency of sources.

---

## Sensitivity Boundaries

**What this project explicitly does not do:**

- Simulate any living religious leader
- Pass judgment on the relative merits of different schools or traditions
- Provide personal practice diagnoses (karma readings, past lives, etc.)
- Claim or simulate supernatural powers or auspicious experiences
- Engage with politically charged religious topics
- Offer medical advice of any kind

**What this project explicitly does:**

- Quote source texts faithfully without distortion or embellishment
- Attach traceable citations (FoJin links) to every response
- Acknowledge clearly when a question falls outside the project's scope
- Encourage users to seek out qualified teachers and authentic practice

---

## Contributing

Contributions are welcome: new pre-built teachers (follow the format in `prebuilt/`), corrections to source attributions, or improvements to the toolchain.

Before submitting, please verify: sources are traceable, content is faithful to historical documents, and no sectarian bias is introduced.

---

## License

MIT License

---

## Acknowledgments

- [FoJin](https://fojin.app) — core data infrastructure
- [colleague-skill](https://github.com/xr843/colleague-skill) — AgentSkills architecture inspiration
- [CBETA](https://cbeta.org) — digitized Chinese Buddhist Canon
- [SuttaCentral](https://suttacentral.net) — Pali Canon and multilingual translations
- [84000](https://84000.co) — Tibetan Buddhist translation project
