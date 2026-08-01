import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Edit, History, RotateCcw } from "lucide-react";
import type { CharacterWithMapping } from "@shared/schema";

interface TranslationPanelProps {
  chapter?: {
    number: number;
    chineseText: string;
    pinyin: string;
    title: string;
  };
  characters: CharacterWithMapping[];
  selectedCharacter: CharacterWithMapping | null;
}

export default function TranslationPanel({
  chapter,
  characters,
  selectedCharacter
}: TranslationPanelProps) {
  const [editMode, setEditMode] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  useEffect(() => {
    if (selectedCharacter) {
      setLastUpdated(new Date());
    }
  }, [selectedCharacter]);

  if (!chapter) {
    return (
      <div className="flex-1 bg-surface flex items-center justify-center">
        <div className="text-center text-gray-500">
          <p>Translation will appear here</p>
        </div>
      </div>
    );
  }

  // Create a mapping of characters to their translations
  const characterMappings = characters.reduce((acc, char) => {
    if (char.mapping?.contextual) {
      acc[char.character] = {
        translation: char.mapping.contextual,
        pinyin: char.pinyin
      };
    }
    return acc;
  }, {} as Record<string, { translation: string; pinyin: string }>);

  const renderTranslatedText = () => {
    const sentences = chapter.chineseText.split(/([。；，！？])/);
    const translations = [];

    for (let i = 0; i < sentences.length; i += 2) {
      if (sentences[i] && sentences[i].trim()) {
        const sentence = sentences[i];
        const punctuation = sentences[i + 1] || '';
        
        // Simple translation logic - replace mapped characters
        let translatedSentence = '';
        let lastIndex = 0;
        
        for (let j = 0; j < sentence.length; j++) {
          const char = sentence[j];
          const mapping = characterMappings[char];
          
          if (mapping) {
            translatedSentence += sentence.slice(lastIndex, j);
            translatedSentence += `<span class="bg-accent bg-opacity-20 px-1 rounded cursor-pointer" title="Mapped from: ${char} (${mapping.pinyin})">${mapping.translation}</span>`;
            lastIndex = j + 1;
          }
        }
        
        translatedSentence += sentence.slice(lastIndex);
        translations.push(translatedSentence + punctuation);
      }
    }

    return translations;
  };

  const translatedSentences = renderTranslatedText();
  const formatTime = (date: Date) => {
    const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
    if (seconds < 60) return `${seconds} seconds ago`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes} minutes ago`;
    const hours = Math.floor(minutes / 60);
    return `${hours} hours ago`;
  };

  return (
    <div className="flex-1 bg-surface">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="font-medium text-gray-900">
            Translation (Chapter {chapter.number})
          </h3>
          <div className="flex items-center space-x-2">
            <Button
              variant={editMode ? "default" : "outline"}
              size="sm"
              onClick={() => setEditMode(!editMode)}
            >
              <Edit className="mr-1" size={14} />
              Edit Mode
            </Button>
            <Button variant="outline" size="sm">
              <History className="mr-1" size={14} />
              History
            </Button>
          </div>
        </div>
      </div>
      
      <div className="p-6 overflow-y-auto" style={{ minHeight: 'calc(100vh - 64px)' }}>
        <div className="prose max-w-none text-gray-800 leading-relaxed">
          {translatedSentences.map((sentence, index) => (
            <p key={index} className="mb-4" dangerouslySetInnerHTML={{ __html: sentence }} />
          ))}
          
          {translatedSentences.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <p>Start mapping characters to see the translation appear here.</p>
              <p className="text-sm mt-2">Select characters in the original text to begin.</p>
            </div>
          )}
          
          {/* Auto-update indicator */}
          {lastUpdated && (
            <div className="mt-6 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center text-sm text-blue-700">
                <RotateCcw className="mr-2 text-blue-500" size={16} />
                Translation updated automatically based on mapping changes
                <Badge variant="secondary" className="ml-2 text-xs">
                  {formatTime(lastUpdated)}
                </Badge>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
