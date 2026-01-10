import { Sidebar } from './components/Sidebar';
import { TopBar } from './components/TopBar';
import { ResearchQueryPanel } from './components/ResearchQueryPanel';
import { AgentActivityPanel } from './components/AgentActivityPanel';

export default function App() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      
      <div className="flex-1 flex flex-col">
        <TopBar />
        
        <div className="flex flex-1 overflow-hidden">
          <ResearchQueryPanel />
          <AgentActivityPanel />
        </div>
      </div>
    </div>
  );
}
