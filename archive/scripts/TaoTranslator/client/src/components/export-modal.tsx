import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Download, X } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ExportModal({ isOpen, onClose }: ExportModalProps) {
  const [format, setFormat] = useState("pdf");
  const [includeOriginal, setIncludeOriginal] = useState(true);
  const [includePinyin, setIncludePinyin] = useState(true);
  const [includeMappings, setIncludeMappings] = useState(true);
  const [includeLexicon, setIncludeLexicon] = useState(false);
  const { toast } = useToast();

  const handleExport = () => {
    // In a real implementation, this would generate and download the export
    toast({
      title: "Export started",
      description: `Generating ${format.toUpperCase()} export with selected options...`
    });
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Export Translation</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Export Format
            </label>
            <Select value={format} onValueChange={setFormat}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="pdf">PDF Document</SelectItem>
                <SelectItem value="html">HTML File</SelectItem>
                <SelectItem value="txt">Plain Text</SelectItem>
                <SelectItem value="json">JSON (with mappings)</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Include
            </label>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="original"
                  checked={includeOriginal}
                  onCheckedChange={setIncludeOriginal}
                />
                <label htmlFor="original" className="text-sm">
                  Original Chinese text
                </label>
              </div>
              
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="pinyin"
                  checked={includePinyin}
                  onCheckedChange={setIncludePinyin}
                />
                <label htmlFor="pinyin" className="text-sm">
                  Pinyin romanization
                </label>
              </div>
              
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="mappings"
                  checked={includeMappings}
                  onCheckedChange={setIncludeMappings}
                />
                <label htmlFor="mappings" className="text-sm">
                  Translation mappings
                </label>
              </div>
              
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="lexicon"
                  checked={includeLexicon}
                  onCheckedChange={setIncludeLexicon}
                />
                <label htmlFor="lexicon" className="text-sm">
                  Full lexicon
                </label>
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex space-x-3 mt-6">
          <Button onClick={handleExport} className="flex-1">
            <Download className="mr-2" size={16} />
            Export
          </Button>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
