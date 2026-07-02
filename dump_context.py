import fitz
import json
import os

SRC_DIR = r"C:\Users\Asus\Desktop\Dermatologie"
MANIFEST_PATH = r"C:\Users\Asus\Desktop\flashcards\manifest.json"
OUT_DIR = r"C:\Users\Asus\Desktop\flashcards\context"

os.makedirs(OUT_DIR, exist_ok=True)

manifest = json.load(open(MANIFEST_PATH, encoding='utf-8'))

def is_dash_sourced(it):
    cap = it['caption']
    if '—' not in cap and '--' not in cap:
        return False
    sep = '—' if '—' in cap else '--'
    tail = cap.split(sep)[-1].strip().split('.')[0].strip().rstrip('.,;: ')
    if tail:
        tail = tail[0].upper() + tail[1:]
    return tail == it['label']

by_course = {}
for it in manifest:
    by_course.setdefault(it['course'], []).append(it)

for course, items in by_course.items():
    pdf_path = os.path.join(SRC_DIR, course + ".pdf")
    doc = fitz.open(pdf_path)
    pages_needed = sorted(set(it['page'] for it in items))
    out = {"course": course, "pages": {}}
    for p in pages_needed:
        page = doc[p - 1]
        out["pages"][str(p)] = page.get_text("text")

    out["images"] = []
    for it in sorted(items, key=lambda x: (x['page'], x['file'])):
        out["images"].append({
            "file": it["file"],
            "page": it["page"],
            "current_label": it["label"],
            "caption_found": it["caption"],
            "reliable": is_dash_sourced(it),
        })

    fname = os.path.join(OUT_DIR, course.replace(" ", "_") + ".json")
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(fname)
