from .ai_provider import generate_text, generate_json


def enhance(text: str, language: str = "auto-detect from source") -> str:
    system = ("Reorganize notes for readability while retaining the source language and script. Never translate. "
              "Preserve all source facts and keep [unclear] markers. Do not add facts, examples, formulas or citations "
              "that are not present. Clearly label any structural headings you introduce. Language hint: " + language)
    return generate_text("Create a readable, well-structured version of these notes without changing their meaning:\n\n" + text, system=system)


def suggestions(text: str, depth: str = "detailed", purpose: str = "personal learning") -> list[dict]:
    if depth not in {"basic", "detailed", "comprehensive"}:
        depth = "detailed"
    prompt = f'''Review these notes for possible missing points. Depth: {depth}. Purpose: {purpose}. Respond in the source language and script.
For students, consider missing definitions, subtopics, steps, examples, formulas and revision concepts. Clearly distinguish possible gaps from optional enrichment.
Return JSON: {{"suggestions":[{{"category":"explicit_omission|potential_gap|optional_enrichment","title":"...","content":"...","rationale":"...","evidence":"...","confidence":0.0}}]}}
Use explicit_omission only when the notes signal an omission or unfinished item. Potential gaps must be qualified. Optional enrichment is not required content. Do not duplicate existing content. Never invent citations, facts, formulas or references. Return [] if nothing is defensible.
NOTES:\n{text}'''
    items = generate_json(prompt, system="You are a cautious notes-review assistant. The uploaded source notes are authoritative.").get("suggestions", [])
    allowed = {"explicit_omission", "potential_gap", "optional_enrichment"}
    clean = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict) or item.get("category") not in allowed:
            continue
        try: confidence = max(0.0, min(1.0, float(item.get("confidence", 0))))
        except (TypeError, ValueError): confidence = 0.0
        clean.append({"category":item["category"],"title":str(item.get("title","Suggestion"))[:255],"content":str(item.get("content","")),"rationale":str(item.get("rationale","")),"evidence":str(item.get("evidence","")),"confidence":confidence})
    return clean


def study_aids(text: str, kind: str) -> dict:
    if kind == "summary":
        task = "Create a useful student study summary with key concepts, headings, definitions, steps and formulas."
    else:
        task = "Create 8 multiple-choice questions based only on the notes. Each question must have four options, answer_index (0-3), and an explanation."
    prompt = f'''{task} Respond in the same language and script as the notes. Do not translate or add unsupported facts. Return a JSON object.\nNOTES:\n{text}'''
    return generate_json(prompt, system="Create accurate, source-grounded study aids. Do not invent facts or answers.")


def enhance_pages(pages: list[str]) -> list[str]:
    """Create clean, structured notes for all pages in one AI call.

    The source text remains stored separately in raw_ocr/faithful_text.
    This function may reorganize but must not add unsupported facts.
    """
    if not pages:
        return []
    prompt = """Create complete, well-structured study notes from the supplied page transcriptions.
Return exactly one enhanced text for every input page, in the same order, as JSON:
{"pages":[{"page":1,"text":"..."},{"page":2,"text":"..."}]}

Rules:
- Preserve the original language and script. Do not translate.
- Preserve every factual point, definition, example, formula, equation, heading, list item and table entry.
- Improve spelling only when the intended source word is unambiguous.
- Organize with clear headings, bullets and readable spacing.
- Do not invent missing explanations, examples, facts, citations or formulas.
- If handwriting was uncertain, retain [unclear] rather than guessing.
- Keep page boundaries: do not move content between pages.
- If a page has no text, return an empty string for that page.
- Output one page entry for every input page.

SOURCE PAGES:
"""
    for index, text in enumerate(pages, 1):
        prompt += f"\\n\\n--- SOURCE PAGE {index} ---\\n{text}"
    data = generate_json(
        prompt,
        system="You are LoveNotes, a meticulous editor of handwritten study notes. Source fidelity is more important than stylistic polish."
    )
    rows = data.get("pages", [])
    by_page = {}
    for row in rows if isinstance(rows, list) else []:
        if isinstance(row, dict):
            try:
                number = int(row.get("page", 0))
            except (TypeError, ValueError):
                continue
            if 1 <= number <= len(pages):
                by_page[number] = str(row.get("text", "")).strip()
    if len(by_page) != len(pages):
        raise RuntimeError("The AI did not return every page. Your original transcription has been saved; retry complete-notes generation.")
    return [by_page[i] for i in range(1, len(pages) + 1)]
