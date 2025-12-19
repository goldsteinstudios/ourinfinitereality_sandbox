"""Test translation engine on Chapter 2 key passages"""

from translation_engine import TranslationEngine

engine = TranslationEngine()

print("="*80)
print("CHAPTER 2 TRANSLATION ENGINE TEST")
print("="*80)

test_passages = [
    ("天下皆知美之為美", "All under heaven know beauty as beauty"),
    ("斯惡已", "This becomes ugliness"),
    ("有無相生", "Existence and non-existence give birth to each other"),
    ("難易相成", "Difficult and easy complete each other"),
    ("長短相形", "Long and short form each other"),
    ("高下相傾", "High and low incline toward each other"),
    ("音聲相和", "Sound and voice harmonize with each other"),
    ("前後相隨", "Front and back follow each other"),
    ("是以聖人處無為之事", "Therefore the sage dwells in the affair of non-action"),
    ("行不言之教", "Practices the teaching of no words"),
    ("萬物作焉而不辭", "Ten thousand things arise and he does not decline"),
    ("功成而弗居", "Merit complete but does not dwell"),
    ("夫唯弗居是以不去", "Only by not dwelling, therefore does not depart"),
]

for chinese, traditional in test_passages:
    print(f"\n{'─'*80}")
    print(f"Chinese: {chinese}")
    print(f"Traditional: {traditional}")
    print(f"{'─'*80}\n")

    layers = engine.translate_multilayer(chinese)

    for layer in layers:
        print(f"[{layer.level.upper().replace('_', ' ')}]")
        print(layer.content)
        print()
