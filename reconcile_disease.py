# -*- coding: utf-8 -*-
import json
import re
from add_disease import canon

MANIFEST = r"C:\Users\Asus\Desktop\flashcards\manifest.json"


def tail_diagnosis(desc):
    """The textbook caption ends with '— <diagnosis>' for that exact photo.
    Return that trailing diagnosis phrase (ground truth), or None."""
    if "—" not in desc:
        return None
    tail = desc.split("—")[-1].strip()
    tail = tail.split(".")[0].strip()
    tail = tail.strip(" ()").rstrip(".,;: ")
    if len(tail) < 4 or len(tail) > 90:
        return None
    # a real caption diagnosis is a short noun phrase, not a descriptive clause
    if len(tail.split()) > 6:
        return None
    low = tail.lower()
    VERBS = ("marche", "observ", "sugere", "prezint", "asociaz", "determin",
             "reprezint", "eviden", "consecin", "extindere", "necesit")
    if any(v in low for v in VERBS):
        return None
    return tail


def main():
    m = json.load(open(MANIFEST, encoding="utf-8"))
    changes = []
    for it in m:
        tail = tail_diagnosis(it["description"])
        if not tail:
            continue
        new = canon(it["course"], tail)
        if new and new != it["disease"]:
            changes.append((it["file"], it["disease"], new, tail))
            it["disease"] = new

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)

    print(f"Reconciled {len(changes)} disease labels to match their photo's textbook caption:\n")
    for f, old, new, tail in changes:
        print(f"  {f.split('/')[-1]:16} {old}  ->  {new}   [caption: …— {tail[:40]}]")


if __name__ == "__main__":
    main()
