import { LayoutDashboard, Sparkles, Users, FileText, FileBarChart } from 'lucide-react';
import logoImage from 'figma:asset/7abc8ae89b943403b345a522dd3753e3e241007b.png';

interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  active?: boolean;
}

const navItems: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, active: false },
  { id: 'new-analysis', label: 'New Analysis', icon: Sparkles, active: true },
  { id: 'agents', label: 'Agents', icon: Users },
  { id: 'evidence', label: 'Evidence', icon: FileText },
  { id: 'reports', label: 'Reports', icon: FileBarChart },
];

export function Sidebar() {
  return (
    <aside className="w-64 h-screen border-r border-sidebar-border bg-gradient-to-b from-[#f8f9ff] to-[#faf5ff] flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-sidebar-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl overflow-hidden bg-gradient-to-br from-[#ec4899] to-[#8b5cf6] flex items-center justify-center">
            <img src={logoImage} alt="PharmaShe" className="w-full h-full object-cover" />
          </div>
          <div>
            <h1 className="text-sidebar-foreground">PharmaShe</h1>
            <p className="text-xs text-muted-foreground">AI Research Platform</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <li key={item.id}>
                <button
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    item.active
                      ? 'bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white shadow-lg shadow-purple-500/30'
                      : 'text-sidebar-foreground hover:bg-[#f5f3ff]'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border">
        <div className="flex items-center gap-3 px-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-[#ec4899] to-[#8b5cf6] flex items-center justify-center shadow-md">
            <span className="text-white text-sm">DR</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm text-sidebar-foreground truncate">Dr. Research</p>
            <p className="text-xs text-muted-foreground">Admin</p>
          </div>
        </div>
      </div>
    </aside>
  );
}