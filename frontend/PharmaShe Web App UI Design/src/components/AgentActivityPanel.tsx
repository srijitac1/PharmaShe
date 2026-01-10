import { Activity, TrendingUp, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import leadAnalystImage from 'figma:asset/4c42766d625ba85af686c58a246edef9ed696d2e.png';

interface Agent {
  id: string;
  name: string;
  status: 'active' | 'completed' | 'pending';
  progress: number;
  findings: number;
  confidence: number;
}

const agents: Agent[] = [
  {
    id: 'literature',
    name: 'Literature Agent',
    status: 'completed',
    progress: 100,
    findings: 247,
    confidence: 94,
  },
  {
    id: 'clinical',
    name: 'Clinical Trials Agent',
    status: 'active',
    progress: 68,
    findings: 34,
    confidence: 87,
  },
  {
    id: 'ip',
    name: 'IP Agent',
    status: 'active',
    progress: 42,
    findings: 12,
    confidence: 79,
  },
  {
    id: 'scoring',
    name: 'Confidence Scoring',
    status: 'pending',
    progress: 0,
    findings: 0,
    confidence: 0,
  },
];

const evidenceItems = [
  {
    id: 1,
    title: 'Paclitaxel + Trastuzumab Synergistic Effects',
    source: 'PubMed',
    confidence: 94,
    date: '2024',
  },
  {
    id: 2,
    title: 'Phase III Trial: HER2+ Breast Cancer',
    source: 'ClinicalTrials.gov',
    confidence: 91,
    date: '2023',
  },
  {
    id: 3,
    title: 'Cardiotoxicity Risk Assessment',
    source: 'PubMed',
    confidence: 88,
    date: '2024',
  },
];

function StatusIcon({ status }: { status: Agent['status'] }) {
  if (status === 'completed') {
    return <CheckCircle2 className="w-4 h-4 text-[#10b981]" />;
  }
  if (status === 'active') {
    return <Loader2 className="w-4 h-4 text-[#8b5cf6] animate-spin" />;
  }
  return <AlertCircle className="w-4 h-4 text-muted-foreground" />;
}

export function AgentActivityPanel() {
  return (
    <aside className="w-96 h-screen border-l border-border bg-gradient-to-b from-[#fafbfd] to-[#f8f9ff] p-6 overflow-auto">
      {/* Lead Analyst Avatar */}
      <Card className="p-4 mb-6 bg-gradient-to-br from-white via-purple-50/50 to-pink-50/50 border-[#8b5cf6]/20">
        <div className="flex items-start gap-4">
          <div className="relative">
            <img
              src={leadAnalystImage}
              alt="Lead Analyst"
              className="w-16 h-16 rounded-full object-cover border-2 border-[#8b5cf6] shadow-lg shadow-purple-500/30"
            />
            <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-[#10b981] rounded-full border-2 border-white flex items-center justify-center shadow-md">
              <Activity className="w-3 h-3 text-white" />
            </div>
          </div>
          <div className="flex-1">
            <h3 className="text-foreground">Lead Analyst</h3>
            <p className="text-sm text-muted-foreground mb-2">Master Agent</p>
            <Badge variant="outline" className="bg-gradient-to-r from-emerald-50 to-green-50 text-[#10b981] border-[#10b981]/30 text-xs">
              Active
            </Badge>
          </div>
        </div>
      </Card>

      {/* Agent Status Cards */}
      <div className="mb-6">
        <h4 className="text-foreground mb-4">Agent Status</h4>
        <div className="space-y-3">
          {agents.map((agent) => (
            <Card key={agent.id} className="p-4 border-l-2 border-l-[#8b5cf6] hover:shadow-md transition-shadow bg-white/80 backdrop-blur-sm">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <StatusIcon status={agent.status} />
                  <div>
                    <p className="text-sm text-foreground">{agent.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {agent.findings} findings
                    </p>
                  </div>
                </div>
                {agent.confidence > 0 && (
                  <div className="text-right">
                    <p className="text-xs text-muted-foreground">Confidence</p>
                    <p className="text-sm text-[#8b5cf6]">{agent.confidence}%</p>
                  </div>
                )}
              </div>
              {agent.status !== 'pending' && (
                <Progress value={agent.progress} className="h-1.5" />
              )}
            </Card>
          ))}
        </div>
      </div>

      {/* Overall Confidence Score */}
      <Card className="p-4 mb-6 bg-gradient-to-br from-[#667eea] to-[#764ba2] text-white shadow-xl shadow-purple-500/40">
        <div className="flex items-center gap-3 mb-3">
          <TrendingUp className="w-5 h-5" />
          <h4>Overall Confidence</h4>
        </div>
        <div className="text-center">
          <p className="text-4xl mb-1">87%</p>
          <p className="text-sm text-white/80">RRF-based scoring</p>
        </div>
      </Card>

      {/* Top Evidence */}
      <div>
        <h4 className="text-foreground mb-4">Top Evidence</h4>
        <div className="space-y-3">
          {evidenceItems.map((item) => (
            <Card key={item.id} className="p-3 hover:shadow-md transition-shadow cursor-pointer bg-white/80 backdrop-blur-sm">
              <div className="flex items-start justify-between mb-2">
                <p className="text-sm text-foreground pr-2">{item.title}</p>
                <Badge variant="outline" className="text-xs bg-gradient-to-r from-purple-50 to-pink-50 text-[#8b5cf6] border-[#8b5cf6]/30 shrink-0">
                  {item.confidence}%
                </Badge>
              </div>
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>{item.source}</span>
                <span>{item.date}</span>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </aside>
  );
}