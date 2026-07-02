import fitz
import json
import os
import re
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

MIN_RECT = 70  # points, min displayed width/height to consider a "real" clinical photo

GENERIC_HEADERS = {
    "DEFINITIE", "DEFINITIE GENERALA SI CLASIFICARE", "EPIDEMIOLOGIE", "ETIOLOGIE",
    "ETIOPATOGENIE", "PATOGENIE", "FIZIOPATOLOGIE", "TABLOU CLINIC", "FORME CLINICE",
    "FORME CLINICE SPECIALE", "DIAGNOSTIC", "DIAGNOSTIC DIFERENTIAL", "DIAGNOSTIC POZITIV",
    "PARACLINIC", "TRATAMENT", "COMPLICATII", "PROFILAXIE", "EVOLUTIE", "PROGNOSTIC",
    "CLASIFICARE", "INTRODUCERE", "GENERALITATI", "CUPRINS", "BIBLIOGRAFIE",
    "MANIFESTARI CLINICE", "MANIFESTARI", "INVESTIGATII", "INVESTIGATII PARACLINICE",
    "EXAMEN CLINIC", "EXAMENE PARACLINICE", "CRITERII DE DIAGNOSTIC", "ASPECTE CLINICE",
    "NOTE", "OBSERVATII", "REZUMAT", "CONCLUZII", "MECANISM", "POZE", "IMAGINI",
    "SIMPTOMATOLOGIE", "SEMNE CLINICE", "CAUZE", "FACTORI DE RISC", "PATOGENEZA",
}


def strip_diacritics(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')


def normalize_heading(text):
    t = re.sub(r'^[A-Za-z]\)\s*', '', text.strip())
    t = re.sub(r'^\d+(\.\d+)*[a-z]?\.?\s*', '', t)
    return t.strip()


def is_generic(text):
    text = normalize_heading(text)
    first_raw = text.split('—')[0].split('-')[0].strip().rstrip('.:')
    key = strip_diacritics(first_raw).upper().strip().rstrip('.:')
    return key in GENERIC_HEADERS


def get_heading_candidates(page):
    d = page.get_text('dict')
    candidates = []
    for b in d['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            txt = ''.join(s['text'] for s in l['spans']).strip()
            if not txt:
                continue
            sizes = [s['size'] for s in l['spans'] if s['text'].strip()]
            if not sizes:
                continue
            size = max(sizes)
            if size >= 11.3 and len(txt) <= 70 and not txt.startswith(('–', '-', '•')):
                candidates.append({'y': l['bbox'][1], 'text': txt, 'size': size})
    candidates.sort(key=lambda c: c['y'])
    return candidates


def slugify(name):
    name = name.replace(".pdf", "")
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = re.sub(r'[^a-zA-Z0-9]+', '-', name).strip('-').lower()
    return name


def get_lines(page):
    d = page.get_text('dict')
    lines = []
    for b in d['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            txt = ''.join(s['text'] for s in l['spans']).strip()
            if txt:
                lines.append({'bbox': l['bbox'], 'text': txt})
    return lines


def find_caption(lines, rect):
    # collect lines directly above the image, same column, walking upward
    # while consecutive gaps stay small
    above = [ln for ln in lines
              if ln['bbox'][3] <= rect.y0 + 4
              and ln['bbox'][2] > rect.x0 - 15
              and ln['bbox'][0] < rect.x1 + 15]
    above.sort(key=lambda l: -l['bbox'][1])  # closest to image first (largest y)
    chunk = []
    prev_top = None
    for ln in above:
        gap = (rect.y0 if prev_top is None else prev_top) - ln['bbox'][3]
        if gap > 40:
            break
        chunk.append(ln)
        prev_top = ln['bbox'][1]
    chunk.reverse()
    return ' '.join(c['text'] for c in chunk)


def extract_label(caption):
    if '—' not in caption and '--' not in caption:
        return None
    # real captions are full descriptive sentences; short dashed phrases
    # ("TABLOU CLINIC — FORME") are section headers, not image captions
    if len(caption) < 40:
        return None
    sep = '—' if '—' in caption else '--'
    pre = caption.split(sep)[0].strip()
    if len(pre) < 15 or is_generic(pre):
        return None
    label = caption.split(sep)[-1].strip()
    label = label.split('.')[0].strip()
    label = label.rstrip('.,;: ')
    if not label or len(label) < 3 or len(label) > 90:
        return None
    return label[0].upper() + label[1:]


def main():
    manifest = []
    os.makedirs(OUT_IMG_DIR, exist_ok=True)
    total_imgs = 0
    for pdf_name in PDFS:
        path = os.path.join(SRC_DIR, pdf_name)
        course_title = pdf_name.replace('.pdf', '')
        slug = slugify(pdf_name)
        course_out = os.path.join(OUT_IMG_DIR, slug)
        os.makedirs(course_out, exist_ok=True)

        doc = fitz.open(path)
        idx = 0
        current_heading = None
        for page_index in range(doc.page_count):
            page = doc[page_index]
            lines = get_lines(page)
            imgs = page.get_images(full=True)
            placed = []
            for img in imgs:
                xref = img[0]
                rects = page.get_image_rects(xref)
                for r in rects:
                    if r.width < MIN_RECT or r.height < MIN_RECT:
                        continue
                    placed.append((xref, r))

            headings = get_heading_candidates(page)
            placed.sort(key=lambda item: item[1].y0)

            hi = 0
            for xref, r in placed:
                # advance heading tracker to the last heading that appears
                # before this image's vertical position on the page
                while hi < len(headings) and headings[hi]['y'] <= r.y0:
                    htxt = normalize_heading(headings[hi]['text'])
                    if htxt and not is_generic(htxt):
                        current_heading = htxt
                    hi += 1

                caption = find_caption(lines, r)
                label = extract_label(caption)
                if not label:
                    label = current_heading
                if not label:
                    continue
                try:
                    base = doc.extract_image(xref)
                except Exception:
                    continue
                ext = base['ext']
                fname = f"p{page_index+1:02d}_{idx:02d}.{ext}"
                fpath = os.path.join(course_out, fname)
                with open(fpath, 'wb') as f:
                    f.write(base['image'])
                manifest.append({
                    'course': course_title,
                    'page': page_index + 1,
                    'file': f"images/{slug}/{fname}",
                    'label': label,
                    'caption': caption,
                })
                idx += 1
                total_imgs += 1
        print(f"{pdf_name}: {idx} labeled images")

    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"TOTAL: {total_imgs} images -> {MANIFEST_PATH}")


if __name__ == '__main__':
    main()
