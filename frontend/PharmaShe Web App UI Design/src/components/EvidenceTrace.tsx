import { Search, MoreVertical, CheckCircle2, FileText, Scale, FlaskConical } from 'lucide-react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';

interface EvidenceCard {
  id: string;
  source: string;
  sourceType: 'TCGA' | 'WIFO' | 'PubMed' | 'ClinicalTrials.gov';
  title: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
}

const evidenceCards: EvidenceCard[] = [
  {
    id: '1',
    source: 'TCGA',
    sourceType: 'TCGA',
    title: 'BRCA1 SOMATIC variant identified',
    description: '',
    icon: FlaskConical,
    color: '#1e3a8a',
  },
  {
    id: '2',
    source: 'WIFO',
    sourceType: 'WIFO',
    title: 'No blocking patents found',
    description: '',
    icon: Scale,
    color: '#8b5cf6',
  },
  {
    id: '3',
    source: 'WIFO',
    sourceType: 'WIFO',
    title: 'No limiting patents found',
    description: '',
    icon: Scale,
    color: '#8b5cf6',
  },
  {
    id: '4',
    source: 'PubMed',
    sourceType: 'PubMed',
    title: 'High-confidence mutation in breast cancer',
    description: '',
    icon: FileText,
    color: '#10b981',
  },
  {
    id: '5',
    source: 'ClinicalTrials.gov',
    sourceType: 'ClinicalTrials.gov',
    title: 'No linked trials',
    description: '',
    icon: CheckCircle2,
    color: '#f59e0b',
  },
];

export function EvidenceTrace() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h3 className="text-foreground mb-1">Evidence Trace</h3>
        <p className="text-sm text-muted-foreground">
          Cross-referenced sources for target validation
        </p>
      </div>

      {/* Evidence Cards Grid */}
      <div className="grid grid-cols-2 gap-4">
        {evidenceCards.map((card) => {
          const Icon = card.icon;
          return (
            <Card
              key={card.id}
              className="p-4 hover:shadow-md transition-all cursor-pointer border-l-4"
              style={{ borderLeftColor: card.color }}
            >
              <div className="flex items-start justify-between mb-3">
                <div
                  className="p-2 rounded-lg"
                  style={{ backgroundColor: `${card.color}15` }}
                >
                  <Icon className="w-4 h-4" style={{ color: card.color }} />
                </div>
                <button className="text-muted-foreground hover:text-foreground">
                  <MoreVertical className="w-4 h-4" />
                </button>
              </div>
              <div>
                <p className="text-xs text-muted-foreground mb-1">
                  {card.source}
                </p>
                <p className="text-sm text-foreground">{card.title}</p>
              </div>
            </Card>
          );
        })}
      </div>

      {/* RRF Scores */}
      <div className="grid grid-cols-2 gap-4">
        {/* RR Fusion Score */}
        <Card className="p-4 bg-gradient-to-br from-emerald-50 via-green-50 to-white border-l-4 border-l-[#10b981] hover:shadow-lg transition-shadow">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#10b981] to-[#059669] flex items-center justify-center shadow-md">
              <CheckCircle2 className="w-4 h-4 text-white" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">RR Fusion Score</p>
            </div>
          </div>
          <p className="text-3xl text-foreground mb-2">0.82</p>
          <p className="text-xs text-muted-foreground leading-relaxed">
            Evidence data ranked using Reciprocal Rank Fusion to reduce redundant scientific claims
          </p>
        </Card>

        {/* RR Power Score */}
        <Card className="p-4 bg-gradient-to-br from-purple-50 via-pink-50 to-white border-l-4 border-l-[#8b5cf6] hover:shadow-lg transition-shadow">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#8b5cf6] to-[#ec4899] flex items-center justify-center shadow-md">
              <CheckCircle2 className="w-4 h-4 text-white" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">RR Power Score</p>
            </div>
          </div>
          <p className="text-3xl text-foreground mb-2">High</p>
          <p className="text-xs text-muted-foreground leading-relaxed">
            Evidence aggregation using Reciprocal Rank Fusion
          </p>
        </Card>
      </div>
    </div>
  );
}