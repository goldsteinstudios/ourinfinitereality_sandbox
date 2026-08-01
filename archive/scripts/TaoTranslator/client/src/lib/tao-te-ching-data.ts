// Tao Te Ching chapter data
// This would typically be loaded from a file or API

export const taoTeChingChapters = [
  {
    number: 1,
    chineseText: '道可道，非常道。名可名，非常名。無，名天地之始；有，名萬物之母。故常無欲，以觀其妙；常有欲，以觀其徼。此兩者，同出而異名，同謂之玄。玄之又玄，眾妙之門。',
    pinyin: 'dào kě dào, fēi cháng dào. míng kě míng, fēi cháng míng. wú, míng tiān dì zhī shǐ; yǒu, míng wàn wù zhī mǔ. gù cháng wú yù, yǐ guān qí miào; cháng yǒu yù, yǐ guān qí jiào. cǐ liǎng zhě, tóng chū ér yì míng, tóng wèi zhī xuán. xuán zhī yòu xuán, zhòng miào zhī mén.',
    title: 'The Tao'
  },
  {
    number: 2,
    chineseText: '天下皆知美之為美，斯惡已。皆知善之為善，斯不善已。故有無相生，難易相成，長短相形，高下相傾，音聲相和，前後相隨。是以聖人處無為之事，行不言之教；萬物作焉而不辞，生而不有，為而不恃，功成而弗居。夫唯弗居，是以不去。',
    pinyin: 'tiān xià jiē zhī měi zhī wéi měi, sī è yǐ. jiē zhī shàn zhī wéi shàn, sī bù shàn yǐ. gù yǒu wú xiāng shēng, nán yì xiāng chéng, cháng duǎn xiāng xíng, gāo xià xiāng qīng, yīn shēng xiāng hé, qián hòu xiāng suí. shì yǐ shèng rén chù wú wéi zhī shì, xíng bù yán zhī jiào; wàn wù zuò yān ér bù cí, shēng ér bù yǒu, wéi ér bù shì, gōng chéng ér fú jū. fū wéi fú jū, shì yǐ bù qù.',
    title: 'The Relativity of Distinctions'
  },
  {
    number: 3,
    chineseText: '不尚賢，使民不爭；不貴難得之貨，使民不為盜；不見可欲，使民心不亂。是以聖人之治，虛其心，實其腹，弱其志，強其骨。常使民無知無欲。使夫智者不敢為也。為無為，則無不治。',
    pinyin: 'bù shàng xián, shǐ mín bù zhēng; bù guì nán dé zhī huò, shǐ mín bù wéi dào; bù jiàn kě yù, shǐ mín xīn bù luàn. shì yǐ shèng rén zhī zhì, xū qí xīn, shí qí fù, ruò qí zhì, qiáng qí gǔ. cháng shǐ mín wú zhī wú yù. shǐ fū zhì zhě bù gǎn wéi yě. wéi wú wéi, zé wú bù zhì.',
    title: 'Without Desire'
  }
];

export function getInitialCharacterFrequencies(): Record<string, number> {
  const frequencies: Record<string, number> = {};
  
  taoTeChingChapters.forEach(chapter => {
    for (const char of chapter.chineseText) {
      if (char.match(/[\u4e00-\u9fff]/)) { // Chinese characters only
        frequencies[char] = (frequencies[char] || 0) + 1;
      }
    }
  });
  
  return frequencies;
}

export function getUniqueCharacters(): string[] {
  const chars = new Set<string>();
  
  taoTeChingChapters.forEach(chapter => {
    for (const char of chapter.chineseText) {
      if (char.match(/[\u4e00-\u9fff]/)) {
        chars.add(char);
      }
    }
  });
  
  return Array.from(chars);
}
