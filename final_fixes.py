import json

MANIFEST_PATH = r"C:\Users\Asus\Desktop\flashcards\manifest.json"

fixes = {
    "images/cursul-13-acnee-si-rozacee/p06_02.jpeg": "Rozacee stadiul I (eritem și telangiectazii, fără papule)",
    "images/cursul-13-acnee-si-rozacee/p06_03.jpeg": "Rozacee stadiul II incipient (papule pe fond eritematos)",
    "images/cursul-4-infectii-micotice/p07_09.png": "Microsporie (tinea capitis)",
    "images/cursul-4-infectii-micotice/p07_10.png": "Tricofitie (tinea capitis)",
    "images/cursul-5-epizoonoze/p02_00.png": "Scabie - șanțul acarian (spațiul interdigital IV)",
    "images/cursul-5-epizoonoze/p02_01.png": "Scabie - șanțul acarian cu veziculă perlată",
    "images/cursul-5-epizoonoze/p03_02.png": "Scabie plantară la copii",
    "images/cursul-5-epizoonoze/p03_03.png": "Scabie nodulară (formă hiperergică)",
    "images/cursul-5-epizoonoze/p04_04.png": "Scabie - șanțul acarian (regiunea radiocarpiană)",
    "images/cursul-5-epizoonoze/p05_05.png": "Pediculoza capitis (paraziți și lindeni pe firul de păr)",
    "images/cursul-5-epizoonoze/p05_06.png": "Pediculoza corporis cronică (melanodermie pediculozică)",
    "images/cursul-8-afectiuni-buloase/p04_03.jpeg": "Pemfigoid bulos - leziunea inițială clasică",
    "images/cursul-9-ulcere-membre-inferioare/p04_01.jpeg": "Dermohipodermită varicoasă (lipodermatoscleroză)",
    "images/cursul-10-tumori-benigne/p04_02.jpeg": "Keratoacantom",
}

manifest = json.load(open(MANIFEST_PATH, encoding='utf-8'))
by_file = {it['file']: it for it in manifest}
changed = 0
for file, label in fixes.items():
    if file not in by_file:
        print("MISSING:", file)
        continue
    by_file[file]['label'] = label
    changed += 1

with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Applied {changed} manual fixes.")
