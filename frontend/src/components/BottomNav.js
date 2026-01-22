import { useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, ListTodo, Timer, Target } from 'lucide-react';

const BottomNav = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard', testId: 'nav-dashboard' },
    { icon: ListTodo, label: 'Tasks', path: '/tasks', testId: 'nav-tasks' },
    { icon: Timer, label: 'Timer', path: '/timer', testId: 'nav-timer' },
    { icon: Target, label: 'Sprints', path: '/sprints', testId: 'nav-sprints' }
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 glass-effect z-50">
      <div className="flex items-center justify-around h-16">
        {navItems.map(({ icon: Icon, label, path, testId }) => (
          <button
            key={path}
            data-testid={testId}
            onClick={() => navigate(path)}
            className={`flex flex-col items-center justify-center flex-1 h-full transition-colors ${
              isActive(path)
                ? 'text-primary'
                : 'text-muted-foreground hover:text-white'
            }`}
          >
            <Icon className="w-6 h-6 mb-1" strokeWidth={2} />
            <span className="text-xs font-medium">{label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
};

export default BottomNav;
