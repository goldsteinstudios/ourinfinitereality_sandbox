// Simple pinyin conversion utilities
// In a production app, you'd use a proper library like pinyin-pro

const pinyinMap: Record<string, string> = {
  '道': 'dào',
  '可': 'kě',
  '非': 'fēi',
  '常': 'cháng',
  '名': 'míng',
  '無': 'wú',
  '天': 'tiān',
  '地': 'dì',
  '之': 'zhī',
  '始': 'shǐ',
  '有': 'yǒu',
  '萬': 'wàn',
  '物': 'wù',
  '母': 'mǔ',
  '故': 'gù',
  '欲': 'yù',
  '觀': 'guān',
  '其': 'qí',
  '妙': 'miào',
  '徼': 'jiào',
  '此': 'cǐ',
  '兩': 'liǎng',
  '者': 'zhě',
  '同': 'tóng',
  '出': 'chū',
  '而': 'ér',
  '異': 'yì',
  '玄': 'xuán',
  '又': 'yòu',
  '眾': 'zhòng',
  '門': 'mén',
  '人': 'rén',
  '不': 'bù',
  '美': 'měi',
  '為': 'wéi',
  '善': 'shàn',
  '是': 'shì',
  '以': 'yǐ',
  '皆': 'jiē',
  '知': 'zhī',
  '惡': 'è',
  '難': 'nán',
  '相': 'xiāng',
  '成': 'chéng',
  '長': 'zhǎng',
  '短': 'duǎn',
  '形': 'xíng',
  '高': 'gāo',
  '下': 'xià',
  '傾': 'qīng',
  '音': 'yīn',
  '聲': 'shēng',
  '和': 'hé',
  '前': 'qián',
  '後': 'hòu',
  '隨': 'suí',
  '處': 'chù',
  '無': 'wú',
  '事': 'shì',
  '行': 'xíng',
  '言': 'yán',
  '教': 'jiào',
  '作': 'zuò',
  '弗': 'fú',
  '辭': 'cí',
  '生': 'shēng',
  '恃': 'shì',
  '功': 'gōng',
  '居': 'jū',
  '夫': 'fū',
  '唯': 'wéi',
  '弗': 'fú',
  '去': 'qù',
};

export function toPinyin(character: string): string {
  return pinyinMap[character] || character;
}

export function convertTextToPinyin(text: string): string {
  return text.split('').map(char => {
    if (pinyinMap[char]) {
      return pinyinMap[char];
    }
    return char;
  }).join(' ');
}

export function searchByPinyin(query: string, characters: string[]): string[] {
  const lowerQuery = query.toLowerCase();
  return characters.filter(char => {
    const pinyin = toPinyin(char).toLowerCase();
    return pinyin.includes(lowerQuery);
  });
}

export function parseChineseText(text: string): { character: string; pinyin: string }[] {
  return text.split('').map(char => ({
    character: char,
    pinyin: toPinyin(char)
  }));
}
