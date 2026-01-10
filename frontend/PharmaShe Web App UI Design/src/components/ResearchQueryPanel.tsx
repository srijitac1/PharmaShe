import { Search, Sparkles, Download } from 'lucide-react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Card } from './ui/card';
import { Input } from './ui/input';
import { EvidenceTrace } from './EvidenceTrace';

const timelineEvents = [
  {
    id: 1,
    agent: 'Lead Analyst',
    action: 'Initialized multi-agent research pipeline',
    time: '2 min ago',
    status: 'completed',
  },
  {
    id: 2,
    agent: 'Literature Agent',
    action: 'Scanning PubMed for relevant publications (1,247 found)',
    time: '1.5 min ago',
    status: 'completed',
  },
  {
    id: 3,
    agent: 'Clinical Trials Agent',
    action: 'Analyzing ClinicalTrials.gov database',
    time: '1 min ago',
    status: 'active',
  },
  {
    id: 4,
    agent: 'IP Agent',
    action: 'Patent landscape analysis in progress',
    time: 'Just now',
    status: 'active',
  },
];

export function ResearchQueryPanel() {
  return (
    <div className="flex-1 p-6 overflow-auto">
      {/* Research Header */}
      <div className="mb-6">
        <div className="flex items-center gap-2 text-sm text-muted-foreground mb-4">
          <span>Research</span>
          <span>/</span>
          <span>Workspaces</span>
        </div>
        <h2 className="text-foreground mb-2">Rapid Target Validation</h2>
        <p className="text-sm text-muted-foreground">
          Agent-enabled for rapid target validation
        </p>
      </div>

      {/* Query Input with Search */}
      <Card className="p-4 mb-6 border-2 border-[#8b5cf6]/20 bg-gradient-to-r from-purple-50/50 to-pink-50/50">
        <div className="flex items-center gap-3">
          <Search className="w-5 h-5 text-muted-foreground" />
          <Input
            placeholder="Describe biological focus"
            className="flex-1 border-0 focus-visible:ring-0 focus-visible:ring-offset-0 bg-transparent"
            defaultValue=""
          />
          <Button className="bg-gradient-to-r from-[#667eea] to-[#764ba2] hover:from-[#5568d3] to-[#6a3f8f] shadow-lg shadow-purple-500/30">
            <Sparkles className="w-4 h-4 mr-2" />
            Run Validation Pipeline
          </Button>
        </div>
      </Card>

      {/* Detailed Research Query */}
      <Card className="p-6 mb-6 border-2 border-[#8b5cf6]/20 bg-gradient-to-br from-white via-purple-50/30 to-pink-50/30">
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-xl bg-gradient-to-br from-[#667eea] to-[#764ba2] shadow-lg shadow-purple-500/30">
            <Search className="w-5 h-5 text-white" />
          </div>
          <div className="flex-1">
            <label className="block text-foreground mb-2">Current Research Query</label>
            <Textarea
              placeholder="e.g., Analyze drug interactions for paclitaxel in combination with HER2-targeted therapies for breast cancer treatment..."
              className="min-h-[100px] mb-4 border-[#8b5cf6]/30 focus:border-[#8b5cf6] bg-white"
              defaultValue="Analyze drug interactions for paclitaxel in combination with HER2-targeted therapies for breast cancer treatment in postmenopausal women."
            />
            <div className="flex items-center gap-3">
              <Button className="bg-gradient-to-r from-[#667eea] to-[#764ba2] hover:from-[#5568d3] to-[#6a3f8f] shadow-lg shadow-purple-500/30">
                <Sparkles className="w-4 h-4 mr-2" />
                Start Analysis
              </Button>
              <Button variant="outline" className="border-[#8b5cf6]/30 hover:bg-purple-50">
                <Download className="w-4 h-4 mr-2" />
                Export PDF Brief
              </Button>
            </div>
          </div>
        </div>
      </Card>

      {/* Evidence Trace Section */}
      <EvidenceTrace />

      {/* Analysis Timeline */}
      <div className="space-y-4 mt-8">
        <h3 className="text-foreground">Analysis Timeline</h3>
        
        {timelineEvents.map((event, index) => (
          <div key={event.id} className="flex gap-4">
            {/* Timeline line */}
            <div className="flex flex-col items-center">
              <div
                className={`w-3 h-3 rounded-full ${
                  event.status === 'completed'
                    ? 'bg-[#10b981]'
                    : event.status === 'active'
                    ? 'bg-[#8b5cf6] animate-pulse'
                    : 'bg-muted'
                }`}
              />
              {index < timelineEvents.length - 1 && (
                <div className="w-0.5 h-16 bg-muted mt-1" />
              )}
            </div>

            {/* Event card */}
            <Card className="flex-1 p-4 border-l-4 border-l-[#8b5cf6]">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <p className="text-sm text-[#8b5cf6]">{event.agent}</p>
                  <p className="text-foreground">{event.action}</p>
                </div>
                <span className="text-xs text-muted-foreground whitespace-nowrap ml-4">
                  {event.time}
                </span>
              </div>
              
              {event.status === 'active' && (
                <div className="mt-3">
                  <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-[#8b5cf6] to-[#f9a8d4] w-2/3 rounded-full animate-pulse" />
                  </div>
                </div>
              )}
            </Card>
          </div>
        ))}
      </div>
    </div>
  );
}