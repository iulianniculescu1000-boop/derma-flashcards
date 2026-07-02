import json
import glob
import os

MANIFEST_PATH = r"C:\Users\Asus\Desktop\flashcards\manifest.json"
CONTEXT_DIR = r"C:\Users\Asus\Desktop\flashcards\context"

manifest = json.load(open(MANIFEST_PATH, encoding='utf-8'))
by_file = {it['file']: it for it in manifest}

changed = 0
for path in glob.glob(os.path.join(CONTEXT_DIR, "*_corrected.json")):
    corrections = json.load(open(path, encoding='utf-8'))
    for file, label in corrections.items():
        if file in by_file:
            if by_file[file]['label'] != label:
                changed += 1
            by_file[file]['label'] = label
        else:
            print("WARNING: unknown file in", path, "->", file)

with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Applied corrections, {changed} labels changed. Total entries: {len(manifest)}")
