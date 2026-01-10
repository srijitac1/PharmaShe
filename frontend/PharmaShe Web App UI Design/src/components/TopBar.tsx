import { Clock, Activity } from 'lucide-react';
import { Badge } from './ui/badge';

export function TopBar() {
  return (
    <header className="h-16 border-b border-border bg-white/80 backdrop-blur-sm flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <div>
          <h2 className="text-foreground">Women's Oncology Research</h2>
          <p className="text-sm text-muted-foreground">Drug Interaction Analysis</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gradient-to-r from-emerald-50 to-green-50 border border-emerald-200">
          <Activity className="w-4 h-4 text-[#10b981] animate-pulse" />
          <span className="text-sm text-emerald-700">Analysis in Progress</span>
        </div>
        
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Clock className="w-4 h-4" />
          <span>Est. 2.5 min remaining</span>
        </div>

        <Badge variant="outline" className="bg-gradient-to-r from-purple-50 to-pink-50 text-[#8b5cf6] border-[#8b5cf6]/30">
          4 Agents Active
        </Badge>
      </div>
    </header>
  );
}