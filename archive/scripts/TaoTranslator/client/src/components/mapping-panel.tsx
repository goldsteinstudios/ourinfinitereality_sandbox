import { useState, useEffect } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Check, X, Search, Edit } from "lucide-react";
import { apiRequest } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";
import type { CharacterWithMapping } from "@shared/schema";

interface MappingPanelProps {
  selectedCharacter: CharacterWithMapping | null;
  onCharacterUpdate: () => void;
  onClearSelection: () => void;
}

export default function MappingPanel({
  selectedCharacter,
  onCharacterUpdate,
  onClearSelection
}: MappingPanelProps) {
  const [literal, setLiteral] = useState("");
  const [philosophical, setPhilosophical] = useState("");
  const [contextual, setContextual] = useState("");
  const [notes, setNotes] = useState("");
  const { toast } = useToast();
  const queryClient = useQueryClient();

  // Load recent mappings
  const { data: recentMappings = [] } = useQuery({
    queryKey: ["/api/mappings/recent"],
    select: (data) => data || []
  });

  // Update form when character changes
  useEffect(() => {
    if (selectedCharacter?.mapping) {
      setLiteral(selectedCharacter.mapping.literal || "");
      setPhilosophical(selectedCharacter.mapping.philosophical || "");
      setContextual(selectedCharacter.mapping.contextual || "");
      setNotes(selectedCharacter.mapping.notes || "");
    } else {
      setLiteral("");
      setPhilosophical("");
      setContextual("");
      setNotes("");
    }
  }, [selectedCharacter]);

  const mappingMutation = useMutation({
    mutationFn: async (mappingData: any) => {
      if (!selectedCharacter) throw new Error("No character selected");
      
      const response = await apiRequest(
        "PUT",
        `/api/mappings/${selectedCharacter.id}`,
        mappingData
      );
      return response.json();
    },
    onSuccess: () => {
      toast({
        title: "Mapping saved",
        description: "Character mapping has been updated successfully."
      });
      onCharacterUpdate();
      queryClient.invalidateQueries({ queryKey: ["/api/mappings/recent"] });
    },
    onError: (error: any) => {
      toast({
        variant: "destructive",
        title: "Failed to save mapping",
        description: error.message || "An error occurred while saving the mapping."
      });
    }
  });

  const handleConfirmMapping = () => {
    if (!selectedCharacter) return;

    mappingMutation.mutate({
      literal,
      philosophical,
      contextual,
      notes
    });
  };

  const handleEditRecentMapping = (mapping: any) => {
    // Find the character and set it as selected
    // This would require additional API call in a real implementation
    console.log("Edit recent mapping:", mapping);
  };

  if (!selectedCharacter) {
    return (
      <div className="w-80 bg-white border-l border-gray-200 overflow-y-auto">
        <div className="p-4 border-b border-gray-100">
          <h3 className="font-medium text-gray-900">Character Mapping</h3>
        </div>
        
        <div className="p-4 text-center text-gray-500">
          <p className="mb-4">Select a character from the original text to begin mapping.</p>
          <div className="text-6xl mb-4 opacity-20">字</div>
          <p className="text-sm">Click on any Chinese character to see its details and create translations.</p>
        </div>

        {/* Recent Mappings */}
        <div className="p-4 border-t border-gray-100">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Recent Mappings</h4>
          <div className="space-y-2">
            {recentMappings.slice(0, 5).map((mapping: any) => (
              <div key={mapping.id} className="flex items-center justify-between p-2 rounded-lg bg-gray-50">
                <div className="flex items-center space-x-2">
                  <span className="chinese-text text-lg">{mapping.character}</span>
                  <div>
                    <div className="text-sm font-medium">{mapping.contextual || mapping.literal}</div>
                    <div className="text-xs text-gray-500 font-mono">{mapping.pinyin}</div>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleEditRecentMapping(mapping)}
                >
                  <Edit size={14} />
                </Button>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-80 bg-white border-l border-gray-200 overflow-y-auto">
      <div className="p-4 border-b border-gray-100">
        <h3 className="font-medium text-gray-900">Character Mapping</h3>
      </div>
      
      {/* Selected Character Details */}
      <div className="p-4 border-b border-gray-100">
        <div className="text-center mb-4">
          <div className="chinese-text text-4xl text-primary mb-2">
            {selectedCharacter.character}
          </div>
          <div className="text-lg font-mono text-gray-600">
            {selectedCharacter.pinyin}
          </div>
        </div>
        
        {/* Interpretation Layers */}
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Literal Translation
            </label>
            <Input
              value={literal}
              onChange={(e) => setLiteral(e.target.value)}
              placeholder="way, path, road"
              className="text-sm"
            />
          </div>
          
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Philosophical Meaning
            </label>
            <Textarea
              rows={3}
              value={philosophical}
              onChange={(e) => setPhilosophical(e.target.value)}
              placeholder="The Way - the fundamental principle underlying all existence..."
              className="text-sm resize-none"
            />
          </div>
          
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Contextual Translation
            </label>
            <Input
              value={contextual}
              onChange={(e) => setContextual(e.target.value)}
              placeholder="The Way"
              className="text-sm"
            />
          </div>
          
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Notes
            </label>
            <Textarea
              rows={2}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Add translation notes..."
              className="text-sm resize-none"
            />
          </div>
        </div>
        
        <div className="flex space-x-2 mt-4">
          <Button
            onClick={handleConfirmMapping}
            disabled={mappingMutation.isPending}
            className="flex-1 bg-success text-white hover:bg-green-700"
            size="sm"
          >
            <Check className="mr-1" size={14} />
            {mappingMutation.isPending ? "Saving..." : "Confirm"}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={onClearSelection}
          >
            <X size={14} />
          </Button>
        </div>
      </div>
      
      {/* Character Usage Stats */}
      <div className="p-4 border-b border-gray-100">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Usage Statistics</h4>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Frequency</span>
            <Badge variant="secondary" className="font-mono">
              {selectedCharacter.frequency} times
            </Badge>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">First appears</span>
            <Badge variant="secondary" className="font-mono">
              Ch. {selectedCharacter.firstChapter || 1}
            </Badge>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Contexts</span>
            <Badge variant="secondary" className="font-mono">
              {selectedCharacter.contexts} different
            </Badge>
          </div>
        </div>
        
        <Button className="w-full mt-3" variant="outline" size="sm">
          <Search className="mr-1" size={14} />
          Show All Occurrences
        </Button>
      </div>
      
      {/* Recent Mappings */}
      <div className="p-4">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Recent Mappings</h4>
        <div className="space-y-2">
          {recentMappings.slice(0, 3).map((mapping: any) => (
            <div key={mapping.id} className="flex items-center justify-between p-2 rounded-lg bg-gray-50">
              <div className="flex items-center space-x-2">
                <span className="chinese-text text-lg">{mapping.character}</span>
                <div>
                  <div className="text-sm font-medium">{mapping.contextual || mapping.literal}</div>
                  <div className="text-xs text-gray-500 font-mono">{mapping.pinyin}</div>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleEditRecentMapping(mapping)}
              >
                <Edit size={14} />
              </Button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
