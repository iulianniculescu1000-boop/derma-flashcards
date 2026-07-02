# -*- coding: utf-8 -*-
import json

MANIFEST = r"C:\Users\Asus\Desktop\flashcards\manifest.json"


def canon(course, label):
    L = label.lower()

    def has(*subs):
        return any(s.lower() in L for s in subs)

    if course.startswith("Cursul 2-"):
        if has("zoster", "involutiei"):
            return "Herpes zoster"
        if has("molluscum"):
            return "Molluscum contagiosum"
        return "Herpes simplex"

    if course.startswith("Cursul 3-"):
        if has("impetigo"):
            return "Impetigo"
        if has("ectim"):
            return "Ectimă"
        if has("cheilita angular", "perleș strept"):
            return "Cheilită angulară streptococică (perleș)"
        if has("erizipel"):
            return "Erizipel"
        if has("antracoid", "carbuncul"):
            return "Furuncul antracoid (carbuncul)"
        if has("furuncul"):
            return "Furuncul"
        if has("hidrosadenit"):
            return "Hidrosadenită supurativă"

    if course.startswith("Cursul 4-"):
        if has("tinea corporis"):
            return "Tinea corporis"
        if has("tinea cruris"):
            return "Tinea cruris"
        if has("tinea faciei"):
            return "Tinea faciei"
        if has("tinea manum", "tinea manuum"):
            return "Tinea manuum"
        if has("tinea pedis", "mocasin"):
            return "Tinea pedis"
        if has("microsporie"):
            return "Microsporie (tinea capitis)"
        if has("tricofitie"):
            return "Tricofiție (tinea capitis)"
        if has("favus"):
            return "Favus"
        if has("kerion"):
            return "Kerion Celsi"
        if has("barbae", "element  cheie", "element cheie"):
            return "Tinea barbae"
        if has("intertrigo candidozic"):
            return "Intertrigo candidozic"
        if has("scutece"):
            return "Candidoză de scutece (dermatită)"
        if has("cheilită angulară candidoz", "pseudomembranoase candidoz"):
            return "Cheilită angulară candidozică (perleș)"
        if has("stomatită candidoz", "muguet"):
            return "Stomatită candidozică (muguet)"
        if has("vulvovaginit"):
            return "Vulvovaginită candidozică"
        if has("pitiriazis versicolor"):
            return "Pitiriazis versicolor"

    if course.startswith("Cursul 5-"):
        if has("scabie"):
            return "Scabie"
        if has("pediculoza capitis", "pediculoză capitis"):
            return "Pediculoză capitis"
        if has("pediculoza corporis", "pediculoză corporis"):
            return "Pediculoză corporis"
        if has("larva migrans"):
            return "Larva migrans cutanată"

    if course.startswith("Cursul 6-"):
        if has("contact iritativ", "iritativă cronică", "iritativ"):
            return "Eczemă de contact iritativă"
        if has("contact alergică"):
            return "Eczemă de contact alergică"
        if has("alergică sistemică"):
            return "Eczemă alergică sistemică"
        if has("numulară"):
            return "Eczemă numulară"
        if has("dishidroz", "pompholyx"):
            return "Eczemă dishidrozică (dishidroză)"
        if has("microbiană"):
            return "Eczemă microbiană"
        if has("de stază"):
            return "Eczemă de stază"
        if has("seboreică"):
            return "Eczemă seboreică"
        if has("asteatotică", "craquelé"):
            return "Eczemă asteatotică"
        if has("dermografism"):
            return "Dermografism (urticarie factice)"
        if has("urticaria la presiune", "urticarie la presiune"):
            return "Urticarie la presiune"
        if has("urticaria la frig", "urticarie la frig"):
            return "Urticarie la frig"
        if has("colinergică"):
            return "Urticarie colinergică"
        if has("urticarie cronică spontană", "urticaria cronică"):
            return "Urticarie cronică spontană"
        if has("angioedem"):
            return "Angioedem"

    if course.startswith("Cursul 8-"):
        if has("epidermofragilitate", "pemfigus"):
            return "Pemfigus vulgar"
        if has("pemfigoid"):
            return "Pemfigoid bulos"
        if has("herpetiform"):
            return "Dermatită herpetiformă (Duhring)"

    if course.startswith("Cursul 9-"):
        if has("edem venos"):
            return "Edem venos cronic"
        if has("dermatită ocră", "dermatită purpurică"):
            return "Dermatită ocră şi purpurică"
        if has("eczemă de stază", "eczema de stază"):
            return "Eczemă de stază"
        if has("dermohipodermit", "lipodermatoscleroz"):
            return "Lipodermatoscleroză"
        if has("atrofie albă"):
            return "Atrofie albă (Milian)"
        if has("ulcer venos"):
            return "Ulcer venos"
        if has("ulcer arterial"):
            return "Ulcer arterial"

    if course.startswith("Cursul 10-"):
        if has("keratoză seboreică", "keratoze seboreice"):
            return "Keratoză seboreică"
        if has("keratoacantom"):
            return "Keratoacantom"
        if has("siringoam", "siringom"):
            return "Siringoame"
        if has("milia"):
            return "Milia"
        if has("chist epidermoid"):
            return "Chist epidermoid"
        if has("chist trichilemal", "chist pilar"):
            return "Chist trichilemal (pilar)"
        if has("cheloid"):
            return "Cheloid"
        if has("fibrom", "fibroam"):
            return "Fibrom moale"
        if has("lipomatoz"):
            return "Lipomatoză"
        if has("lipom"):
            return "Lipom"
        if has("hemangiom"):
            return "Hemangiom"
        if has("granulom piogenic"):
            return "Granulom piogenic (botriomicom)"

    if course.startswith("Cursul 11-"):
        if has("keratoze actinice", "keratoză actinică"):
            return "Keratoză actinică"
        if has("arsenicale"):
            return "Keratoze arsenicale"
        if has("radiodermit"):
            return "Radiodermită cronică"
        if has("corn cutanat"):
            return "Corn cutanat"
        if has("nev "):
            return "Nev nevocelular"
        if L.startswith("nevi") or L.startswith("nev"):
            return "Nev nevocelular"
        if has("cbc", "bazaliomatoas", "placă scleroticé"):
            return "Carcinom bazocelular (CBC)"
        if has("csc"):
            return "Carcinom spinocelular (CSC)"
        if has("melanom", "haluce sau police", "dubreuilh"):
            return "Melanom malign"

    if course.startswith("Cursul 12-"):
        if has("condyloma", "regiunile perianală"):
            return "Condyloma acuminatum"
        if has("gonoree", "gonococic"):
            return "Gonoree"
        if has("șancru dur", "sifilis primar"):
            return "Sifilis primar (șancru dur)"
        if has("sifilis secundar"):
            return "Sifilis secundar"
        if has("gomă sifilit", "terțiar"):
            return "Sifilis terțiar (gomă)"
        if has("limfogranulomatoz", "jgheab"):
            return "Limfogranulomatoză veneriană (LGV)"
        if has("șancru moale"):
            return "Șancru moale (șancroid)"

    if course.startswith("Cursul 13-"):
        if has("comedonian"):
            return "Acnee comedoniană"
        if has("papulo") and has("pustuloasă"):
            return "Acnee papulo-pustuloasă"
        if has("nodulo-chistică"):
            return "Acnee nodulo-chistică"
        if has("rozacee"):
            return "Rozacee"

    return None  # unmatched -> flag


def main():
    m = json.load(open(MANIFEST, encoding='utf-8'))
    unmatched = []
    for it in m:
        d = canon(it['course'], it['label'])
        if d is None:
            unmatched.append(it)
            d = it['label']
        it['disease'] = d
    with open(MANIFEST, 'w', encoding='utf-8') as f:
        json.dump(m, f, ensure_ascii=False, indent=2)

    from collections import Counter, defaultdict
    print("UNMATCHED:", len(unmatched))
    for it in unmatched:
        print("  ", it['course'][:18], "|", it['label'][:50])

    print("\nDisease counts per course:")
    by = defaultdict(set)
    for it in m:
        by[it['course']].add(it['disease'])
    for c in sorted(by, key=lambda x: int(x.split('-')[0].replace('Cursul', '').strip())):
        print(f"  {c}: {len(by[c])} diseases -> {sorted(by[c])}")


if __name__ == '__main__':
    main()
