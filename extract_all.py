import fitz
import json
import os
import re
import hashlib
import unicodedata

SRC_DIR = r"C:\Users\Asus\Desktop\Dermatologie"
OUT_IMG_DIR = r"C:\Users\Asus\Desktop\flashcards\images"
MANIFEST_PATH = r"C:\Users\Asus\Desktop\flashcards\manifest.json"

PDFS = [
    "Cursul 13-Acnee si Rozacee.pdf",
    "Cursul 2-Infectii virale.pdf",
    "Cursul 3-Infectii Bacteriene.pdf",
    "Cursul 4-Infectii Micotice.pdf",
    "Cursul 5-Epizoonoze.pdf",
    "Cursul 6-Eczeme si Urticarie.pdf",
    "Cursul 8-Afectiuni Buloase.pdf",
    "Cursul 9-Ulcere Membre Inferioare.pdf",
    "Cursul 10-Tumori Benigne.pdf",
    "Cursul 11-Tumori Maligne.pdf",
    "Cursul 12-BTS.pdf",
]

MIN_RECT = 70

# ---- reuse labeling helpers from extract.py ----
from extract import (get_lines, find_caption, extract_label,
                     get_heading_candidates, normalize_heading, is_generic, slugify)


def build_hash_label_map():
    """Map md5(image-bytes) -> existing corrected label, so we preserve
    the 170 already-reviewed labels when re-extracting."""
    m = json.load(open(MANIFEST_PATH, encoding='utf-8'))
    hmap = {}
    for it in m:
        path = os.path.join(r"C:\Users\Asus\Desktop\flashcards", it['file'].replace('/', os.sep))
        if os.path.exists(path):
            h = hashlib.md5(open(path, 'rb').read()).hexdigest()
            hmap[h] = it['label']
    return hmap


def wipe_images():
    import shutil
    if os.path.isdir(OUT_IMG_DIR):
        shutil.rmtree(OUT_IMG_DIR)
    os.makedirs(OUT_IMG_DIR, exist_ok=True)


def main():
    hash_label = build_hash_label_map()  # must run before wiping the old files
    wipe_images()
    manifest = []
    new_count = 0
    reused_count = 0

    for pdf_name in PDFS:
        path = os.path.join(SRC_DIR, pdf_name)
        course_title = pdf_name.replace('.pdf', '')
        slug = slugify(pdf_name)
        course_out = os.path.join(OUT_IMG_DIR, slug)
        os.makedirs(course_out, exist_ok=True)

        doc = fitz.open(path)
        seen_xref = set()
        current_heading = None

        for page_index in range(doc.page_count):
            page = doc[page_index]
            lines = get_lines(page)
            headings = get_heading_candidates(page)

            placed = []
            for img in page.get_images(full=True):
                xref = img[0]
                for r in page.get_image_rects(xref):
                    if r.width < MIN_RECT or r.height < MIN_RECT:
                        continue
                    placed.append((xref, r))
            placed.sort(key=lambda item: item[1].y0)

            hi = 0
            for xref, r in placed:
                while hi < len(headings) and headings[hi]['y'] <= r.y0:
                    htxt = normalize_heading(headings[hi]['text'])
                    if htxt and not is_generic(htxt):
                        current_heading = htxt
                    hi += 1

                if xref in seen_xref:
                    continue
                seen_xref.add(xref)

                try:
                    base = doc.extract_image(xref)
                except Exception:
                    continue
                img_bytes = base['image']
                ext = base['ext']
                h = hashlib.md5(img_bytes).hexdigest()

                caption = find_caption(lines, r)
                auto_label = extract_label(caption) or current_heading

                if h in hash_label:
                    label = hash_label[h]
                    needs = False
                    reused_count += 1
                else:
                    label = auto_label  # may be None
                    needs = True
                    new_count += 1

                fname = f"p{page_index+1:02d}_x{xref}.{ext}"
                fpath = os.path.join(course_out, fname)
                with open(fpath, 'wb') as f:
                    f.write(img_bytes)

                manifest.append({
                    'course': course_title,
                    'page': page_index + 1,
                    'file': f"images/{slug}/{fname}",
                    'label': label if label else "",
                    'caption': caption,
                    'needs_label': needs,
                })

    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"TOTAL images: {len(manifest)}  reused_labels={reused_count}  new={new_count}")
    from collections import Counter
    c = Counter(it['course'] for it in manifest if it['needs_label'])
    print("New (need label) per course:")
    for k, v in c.items():
        print(f"  {v:3d}  {k}")


if __name__ == '__main__':
    main()
