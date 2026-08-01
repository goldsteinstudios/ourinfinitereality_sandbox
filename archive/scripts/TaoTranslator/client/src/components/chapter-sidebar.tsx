import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { BookOpen, TrendingUp } from "lucide-react";
import type { ChapterWithProgress } from "@shared/schema";

interface ChapterSidebarProps {
  chapters: ChapterWithProgress[];
  selectedChapter: number;
  onChapterSelect: (chapter: number) => void;
  lexiconStats?: {
    totalChars: number;
    mappedChars: number;
    pendingChars: number;
    progressPercent: number;
  };
}

export default function ChapterSidebar({
  chapters,
  selectedChapter,
  onChapterSelect,
  lexiconStats
}: ChapterSidebarProps) {
  return (
    <div className="w-64 bg-white border-r border-gray-200 overflow-y-auto">
      {/* Chapter Selection */}
      <div className="p-4 border-b border-gray-100">
        <h3 className="font-medium text-gray-900 mb-3">Chapters</h3>
        <div className="space-y-1 max-h-96 overflow-y-auto">
          {chapters.map((chapter) => {
            const isSelected = chapter.number === selectedChapter;
            const progress = chapter.progress?.completionPercentage || 0;
            
            return (
              <div
                key={`chapter-${chapter.id}`}
                className={`flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors ${
                  isSelected ? 'bg-blue-50 border border-blue-200' : ''
                }`}
                onClick={() => onChapterSelect(chapter.number)}
              >
                <span className={`font-medium ${isSelected ? 'text-primary' : 'text-gray-700'}`}>
                  Chapter {chapter.number}
                </span>
                <div className="flex items-center space-x-2">
                  <span className="text-xs text-gray-500">{progress}%</span>
                  <div 
                    className={`w-2 h-2 rounded-full ${
                      progress > 80 ? 'bg-success' : progress > 20 ? 'bg-warning' : 'bg-gray-300'
                    }`}
                  />
                </div>
              </div>
            );
          })}
          
          {chapters.length < 81 && (
            <div className="text-center py-2">
              <span className="text-xs text-gray-400">
                ... {81 - chapters.length} more chapters
              </span>
            </div>
          )}
        </div>
      </div>
      
      {/* Lexicon Stats */}
      <div className="p-4">
        <h3 className="font-medium text-gray-900 mb-3">Lexicon Overview</h3>
        {lexiconStats && (
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Total Characters</span>
              <Badge variant="secondary" className="font-mono">
                {lexiconStats.totalChars}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Mapped</span>
              <Badge className="bg-success text-white font-mono">
                {lexiconStats.mappedChars}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Pending</span>
              <Badge className="bg-warning text-white font-mono">
                {lexiconStats.pendingChars}
              </Badge>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
              <div 
                className="bg-primary h-2 rounded-full transition-all" 
                style={{ width: `${lexiconStats.progressPercent}%` }}
              />
            </div>
          </div>
        )}
        
        <Button 
          className="w-full mt-4" 
          variant="outline"
          size="sm"
        >
          <BookOpen className="mr-2" size={16} />
          View Full Lexicon
        </Button>
      </div>
    </div>
  );
}
