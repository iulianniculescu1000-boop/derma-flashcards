# -*- coding: utf-8 -*-
import fitz
import json
import os
import re

SRC_DIR = r"C:\Users\Asus\Desktop\Dermatologie"
MANIFEST = r"C:\Users\Asus\Desktop\flashcards\manifest.json"

KEYWORDS = ("se observ", "la nivel", "se decel", "se eviden", "in regiun",
            "în regiun", "secventa", "secvenţa", "secvența", "aspect",
            "la palpare", "prezinta", "prezintă", "eruptie", "erupție",
            "leziun", "placard", "multipl", "numeros")

COURSE_FILES = {}


def course_pdf(course):
    return os.path.join(SRC_DIR, course + ".pdf")


def get_blocks(page):
    d = page.get_text("dict")
    raw = []
    for b in d["blocks"]:
        if b["type"] != 0:
            continue
        txt = " ".join("".join(s["text"] for s in l["spans"]) for l in b["lines"]).strip()
        txt = re.sub(r"\s+", " ", txt)
        if txt:
            raw.append({"bbox": list(b["bbox"]), "text": txt})

    # merge vertically-adjacent, column-overlapping blocks so a caption sentence
    # split across several PDF text-blocks becomes one candidate
    raw.sort(key=lambda b: b["bbox"][1])
    merged = []
    for b in raw:
        if merged:
            p = merged[-1]
            px0, py0, px1, py1 = p["bbox"]
            bx0, by0, bx1, by1 = b["bbox"]
            hov = min(px1, bx1) - max(px0, bx0)
            gap = by0 - py1
            end_punct = p["text"].rstrip().endswith((".", ";", ":")) or "—" in p["text"]
            if hov > 0.4 * min(px1 - px0, bx1 - bx0) and -4 <= gap <= 24 and "•" not in b["text"] and not end_punct:
                p["text"] = (p["text"] + " " + b["text"]).strip()
                p["bbox"] = [min(px0, bx0), min(py0, by0), max(px1, bx1), max(py1, by1)]
                continue
        merged.append({"bbox": list(b["bbox"]), "text": b["text"]})
    return merged


def is_body(txt):
    if "•" in txt:
        return True
    if len(txt) > 360:
        return True
    if re.match(r"^[A-Z]\)\s", txt):
        return True
    # all-caps heading
    letters = [c for c in txt if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.7 and len(txt) < 60:
        return True
    return False


def starts_keyword(txt):
    low = txt.lower()
    return any(low.startswith(k) for k in KEYWORDS)


def clean_desc(txt):
    txt = txt.strip()
    # trim to end of the sentence that carries the diagnosis if a dash exists
    txt = re.sub(r"\s+", " ", txt)
    return txt


def find_description(page, rect):
    ix0, iy0, ix1, iy1 = rect.x0, rect.y0, rect.x1, rect.y1
    iw = ix1 - ix0
    best = None
    best_score = 1e9
    for b in get_blocks(page):
        bx0, by0, bx1, by1 = b["bbox"]
        txt = b["text"]
        if is_body(txt):
            continue
        if len(txt) < 25:
            continue
        # horizontal (column) overlap with the image
        overlap = min(ix1, bx1) - max(ix0, bx0)
        bcx = (bx0 + bx1) / 2
        col_ok = overlap > 0.35 * iw or (ix0 - 20 <= bcx <= ix1 + 20)
        if not col_ok:
            continue
        # vertical gap: below or above the image
        if by0 >= iy1 - 6:            # block is below the image
            gap = by0 - iy1
        elif by1 <= iy0 + 6:          # block is above the image
            gap = iy0 - by1
        else:
            continue
        if gap > 90:
            continue
        score = gap
        if starts_keyword(txt):
            score -= 40
        if "—" in txt or "--" in txt:
            score -= 15
        if by0 >= iy1 - 6:            # slight preference for captions below
            score -= 5
        if score < best_score:
            best_score = score
            best = txt
    return clean_desc(best) if best else None


def main():
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    docs = {}
    filled = 0
    fallback = 0
    for it in manifest:
        course = it["course"]
        if course not in docs:
            docs[course] = fitz.open(course_pdf(course))
        doc = docs[course]
        page = doc[it["page"] - 1]

        mobj = re.search(r"_x(\d+)\.", it["file"])
        desc = None
        if mobj:
            xref = int(mobj.group(1))
            rects = page.get_image_rects(xref)
            if rects:
                desc = find_description(page, rects[0])

        if not desc:
            # fall back to the existing caption if it's a real sentence
            cap = it.get("caption", "").strip()
            if len(cap) > 40 and not is_body(cap):
                desc = clean_desc(cap)

        if desc:
            it["description"] = desc
            filled += 1
        else:
            it["description"] = it["label"]  # last resort: the detailed label
            fallback += 1

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"descriptions filled from PDF/caption: {filled}, fallback to label: {fallback}, total {len(manifest)}")


if __name__ == "__main__":
    main()
