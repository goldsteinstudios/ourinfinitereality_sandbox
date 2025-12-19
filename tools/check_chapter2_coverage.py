"""Check which Chapter 2 characters are already in the database"""

from translation_engine import CHARACTER_OPERATIONS
import re

# Chapter 2 text
chapter2_text = '''天下皆知美之為美斯惡已皆知善之為善斯不善已故有無相生難易相成長短相形高下相傾音聲相和前後相隨是以聖人處無為之事行不言之教萬物作焉而不辭生而不有為而不恃功成而弗居夫唯弗居是以不去唯弗居是以不去'''

# Get unique characters
unique_chars = sorted(set(re.findall(r'[\u4e00-\u9fff]', chapter2_text)))

# Check which are already in database
already_in_db = [c for c in unique_chars if c in CHARACTER_OPERATIONS]
missing_from_db = [c for c in unique_chars if c not in CHARACTER_OPERATIONS]

print(f'Chapter 2 unique characters: {len(unique_chars)}')
print(f'Already in database: {len(already_in_db)}/{len(unique_chars)}')
print(f'Need to add: {len(missing_from_db)}')

print(f'\nAlready covered: {"".join(already_in_db)}')
print(f'\nNEED TO ADD ({len(missing_from_db)} characters): {"".join(missing_from_db)}')
print(f'\nMissing characters as list:')
for char in missing_from_db:
    print(f'  {char}')
