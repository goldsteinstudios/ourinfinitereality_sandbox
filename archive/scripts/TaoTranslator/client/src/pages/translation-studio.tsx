import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { Search, Download, Settings, Languages } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import ChapterSidebar from "@/components/chapter-sidebar";
import OriginalTextPanel from "@/components/original-text-panel";
import TranslationPanel from "@/components/translation-panel";
import MappingPanel from "@/components/mapping-panel";
import ExportModal from "@/components/export-modal";
import { taoTeChingChapters } from "@/lib/tao-te-ching-data";
import type { CharacterWithMapping } from "@shared/schema";

export default function TranslationStudio() {
  const [selectedChapter, setSelectedChapter] = useState(1);
  const [selectedCharacter, setSelectedCharacter] = useState<CharacterWithMapping | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [showExportModal, setShowExportModal] = useState(false);
  const [showPinyin, setShowPinyin] = useState(true);
  const queryClient = useQueryClient();

  // Initialize data on first load
  useEffect(() => {
    const initializeData = async () => {
      try {
        // Check if chapters already exist
        const response = await apiRequest("GET", "/api/chapters");
        const existingChapters = await response.json();
        
        if (existingChapters.length === 0) {
          // Create chapters if they don't exist
          for (const chapter of taoTeChingChapters) {
            await apiRequest("POST", "/api/chapters", chapter);
          }
        }
      } catch (error) {
        console.log("Error initializing chapters:", error);
      }
    };

    initializeData();
  }, []);

  const { data: chapters } = useQuery({
    queryKey: ["/api/chapters"],
    select: (data) => data || []
  });

  const { data: characters = [] } = useQuery({
    queryKey: ["/api/characters"],
    select: (data) => data || []
  });

  const { data: lexiconStats } = useQuery({
    queryKey: ["/api/lexicon/stats"],
    select: (data) => data || { totalChars: 0, mappedChars: 0, pendingChars: 0, progressPercent: 0 }
  });

  const searchMutation = useMutation({
    mutationFn: async (query: string) => {
      const response = await apiRequest("GET", `/api/characters?search=${encodeURIComponent(query)}`);
      return response.json();
    }
  });

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    if (query.trim()) {
      searchMutation.mutate(query);
    }
  };

  const handleCharacterSelect = async (char: string) => {
    try {
      // First try to get existing character
      let response = await apiRequest("GET", `/api/characters/${encodeURIComponent(char)}`);
      let characterData;
      
      if (!response.ok) {
        // Character doesn't exist, create it
        const { toPinyin } = await import("@/lib/pinyin");
        const newCharacter = {
          character: char,
          pinyin: toPinyin(char),
          frequency: 1,
          firstChapter: selectedChapter
        };
        
        console.log("Creating character:", newCharacter);
        response = await apiRequest("POST", "/api/characters", newCharacter);
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(`Failed to create character: ${JSON.stringify(errorData)}`);
        }
        
        characterData = await response.json();
        console.log("Character created:", characterData);
        
        // Invalidate queries to refresh the UI
        queryClient.invalidateQueries({ queryKey: ["/api/characters"] });
        queryClient.invalidateQueries({ queryKey: ["/api/lexicon/stats"] });
      } else {
        characterData = await response.json();
      }
      
      setSelectedCharacter(characterData);
    } catch (error) {
      console.error("Failed to load/create character:", error);
    }
  };

  const currentChapter = taoTeChingChapters.find(c => c.number === selectedChapter);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 h-16 flex items-center px-6">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-medium text-gray-900">
            <Languages className="inline text-primary mr-2" size={24} />
            Tao Te Ching Translation Studio
          </h1>
        </div>
        
        <div className="flex-1 max-w-md mx-8">
          <div className="relative">
            <Input
              type="text"
              placeholder="Search characters, pinyin, or meanings..."
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
              className="pl-10"
            />
            <Search className="absolute left-3 top-3 text-gray-400" size={16} />
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          <Button 
            onClick={() => setShowExportModal(true)}
            className="bg-success text-white hover:bg-green-700"
          >
            <Download className="mr-2" size={16} />
            Export
          </Button>
          <Button variant="ghost" size="icon">
            <Settings size={16} />
          </Button>
        </div>
      </header>

      <div className="flex h-screen pt-16">
        <ChapterSidebar
          chapters={chapters || []}
          selectedChapter={selectedChapter}
          onChapterSelect={setSelectedChapter}
          lexiconStats={lexiconStats}
        />

        <div className="flex-1 flex">
          <OriginalTextPanel
            chapter={currentChapter}
            showPinyin={showPinyin}
            onTogglePinyin={() => setShowPinyin(!showPinyin)}
            onCharacterSelect={handleCharacterSelect}
            selectedCharacter={selectedCharacter}
          />

          {/* Resizer */}
          <div className="w-1 bg-gray-200 cursor-col-resize hover:bg-gray-300" />

          <TranslationPanel
            chapter={currentChapter}
            characters={characters}
            selectedCharacter={selectedCharacter}
          />
        </div>

        <MappingPanel
          selectedCharacter={selectedCharacter}
          onCharacterUpdate={() => {
            queryClient.invalidateQueries({ queryKey: ["/api/characters"] });
            queryClient.invalidateQueries({ queryKey: ["/api/lexicon/stats"] });
          }}
          onClearSelection={() => setSelectedCharacter(null)}
        />
      </div>

      <ExportModal
        isOpen={showExportModal}
        onClose={() => setShowExportModal(false)}
      />
    </div>
  );
}
