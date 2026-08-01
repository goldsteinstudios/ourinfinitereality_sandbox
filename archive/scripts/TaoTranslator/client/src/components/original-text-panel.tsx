import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Eye, Info } from "lucide-react";
import { parseChineseText } from "@/lib/pinyin";
import type { CharacterWithMapping } from "@shared/schema";

interface OriginalTextPanelProps {
  chapter?: {
    number: number;
    chineseText: string;
    pinyin: string;
    title: string;
  };
  showPinyin: boolean;
  onTogglePinyin: () => void;
  onCharacterSelect: (char: string) => void;
  selectedCharacter: CharacterWithMapping | null;
}

export default function OriginalTextPanel({
  chapter,
  showPinyin,
  onTogglePinyin,
  onCharacterSelect,
  selectedCharacter
}: OriginalTextPanelProps) {
  const [showCharacterInfo, setShowCharacterInfo] = useState(false);

  if (!chapter) {
    return (
      <div className="flex-1 bg-white border-r border-gray-200 flex items-center justify-center">
        <div className="text-center text-gray-500">
          <p>Select a chapter to begin translation</p>
        </div>
      </div>
    );
  }

  const parseTextToLines = (text: string, pinyinText: string) => {
    // Split by punctuation to create natural line breaks
    const sentences = text.split(/([。；，！？])/);
    const pinyinSentences = pinyinText.split(/([。；，！？])/);
    const lines = [];
    
    for (let i = 0; i < sentences.length; i += 2) {
      if (sentences[i] && sentences[i].trim()) {
        lines.push({
          chinese: sentences[i] + (sentences[i + 1] || ''),
          pinyin: (pinyinSentences[i] || '') + (pinyinSentences[i + 1] || '')
        });
      }
    }
    
    return lines;
  };

  const lines = parseTextToLines(chapter.chineseText, chapter.pinyin);

  const renderCharacter = (char: string, index: number) => {
    const isSelected = selectedCharacter?.character === char;
    const isMapped = selectedCharacter?.mapping !== null && selectedCharacter?.character === char;
    const isChinese = char.match(/[\u4e00-\u9fff]/);
    
    if (!isChinese) {
      return (
        <span key={index} className="chinese-text">
          {char}
        </span>
      );
    }

    return (
      <span
        key={index}
        className={`chinese-text cursor-pointer transition-colors ${
          isSelected
            ? 'bg-blue-200 border-b-2 border-blue-500'
            : isMapped
            ? 'bg-accent bg-opacity-20 border-b-2 border-accent hover:bg-opacity-30'
            : 'hover:bg-gray-100'
        }`}
        onClick={() => onCharacterSelect(char)}
        title={showCharacterInfo ? `${char} - Click to map` : ''}
      >
        {char}
      </span>
    );
  };

  return (
    <div className="flex-1 bg-white border-r border-gray-200">
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <h3 className="font-medium text-gray-900">
            Original Text (Chapter {chapter.number})
          </h3>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={onTogglePinyin}
            >
              <Eye className="mr-1" size={14} />
              {showPinyin ? 'Hide' : 'Show'} Pinyin
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowCharacterInfo(!showCharacterInfo)}
            >
              <Info className="mr-1" size={14} />
              Character Info
            </Button>
          </div>
        </div>
      </div>
      
      <div className="p-6 overflow-y-auto" style={{ minHeight: 'calc(100vh - 64px)' }}>
        <div className="chinese-text text-2xl leading-loose">
          {lines.map((line, lineIndex) => (
            <div key={lineIndex} className="mb-6">
              <div className="mb-2">
                {line.chinese.split('').map((char, charIndex) => 
                  renderCharacter(char, `${lineIndex}-${charIndex}`)
                )}
              </div>
              
              {showPinyin && (
                <div className="pinyin-text text-base opacity-60 mb-4">
                  {line.pinyin}
                </div>
              )}
            </div>
          ))}
        </div>
        
        {chapter.title && (
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h4 className="text-sm font-medium text-gray-700 mb-1">Chapter Title</h4>
            <p className="text-gray-600">{chapter.title}</p>
          </div>
        )}
      </div>
    </div>
  );
}
