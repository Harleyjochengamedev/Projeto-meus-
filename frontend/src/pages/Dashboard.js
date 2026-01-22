import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { axiosInstance } from '../App';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Avatar, AvatarImage, AvatarFallback } from '../components/ui/avatar';
import { Badge } from '../components/ui/badge';
import { Clock, CheckCircle2, Timer as TimerIcon, Target, Plus, TrendingUp, Code2 } from 'lucide-react';
import { toast } from 'sonner';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [overview, setOverview] = useState(null);
  const [recentTasks, setRecentTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [userRes, overviewRes, tasksRes] = await Promise.all([
        axiosInstance.get('/auth/me'),
        axiosInstance.get('/dashboard/overview'),
        axiosInstance.get('/tasks?status=todo&status=in_progress')
      ]);
      setUser(userRes.data);
      setOverview(overviewRes.data);
      setRecentTasks(tasksRes.data.slice(0, 5));
    } catch (error) {
      console.error('Error loading data:', error);
      toast.error('Erro ao carregar dados');
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      task: 'bg-primary/10 text-primary border-primary/30',
      study: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/30',
      pr: 'bg-purple-500/10 text-purple-500 border-purple-500/30',
      bug: 'bg-destructive/10 text-destructive border-destructive/30',
      project: 'bg-accent/10 text-accent border-accent/30'
    };
    return colors[category] || colors.task;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pb-24 md:pb-8">
      {/* Header */}
      <header className="glass-effect sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Code2 className="w-7 h-7 text-primary" strokeWidth={2} />
            <h1 className="text-xl font-bold text-white">DevFlow</h1>
          </div>
          
          <Avatar className="w-9 h-9 border-2 border-primary/30">
            <AvatarImage src={user?.picture} alt={user?.name} />
            <AvatarFallback>{user?.name?.[0]}</AvatarFallback>
          </Avatar>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        {/* Welcome */}
        <div className="space-y-2">
          <h2 className="text-2xl md:text-3xl font-bold text-white">Olá, {user?.name?.split(' ')[0]}!</h2>
          <p className="text-muted-foreground">Aqui está seu overview de hoje</p>
        </div>

        {/* Stats Grid - Bento Style */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="bg-card border-border p-6 grid-border" data-testid="tasks-today-card">
            <div className="space-y-2">
              <Target className="w-8 h-8 text-primary" strokeWidth={2} />
              <div>
                <p className="text-2xl md:text-3xl font-bold text-white font-mono">
                  {overview?.tasks_today || 0}
                </p>
                <p className="text-xs text-muted-foreground">Tasks Ativas</p>
              </div>
            </div>
          </Card>

          <Card className="bg-card border-border p-6 grid-border" data-testid="completed-today-card">
            <div className="space-y-2">
              <CheckCircle2 className="w-8 h-8 text-emerald-500" strokeWidth={2} />
              <div>
                <p className="text-2xl md:text-3xl font-bold text-white font-mono">
                  {overview?.tasks_completed_today || 0}
                </p>
                <p className="text-xs text-muted-foreground">Concluídas Hoje</p>
              </div>
            </div>
          </Card>

          <Card className="bg-card border-border p-6 grid-border" data-testid="time-today-card">
            <div className="space-y-2">
              <Clock className="w-8 h-8 text-accent" strokeWidth={2} />
              <div>
                <p className="text-2xl md:text-3xl font-bold text-white font-mono">
                  {overview?.total_time_today || 0}m
                </p>
                <p className="text-xs text-muted-foreground">Tempo Hoje</p>
              </div>
            </div>
          </Card>

          <Card className="bg-card border-border p-6 grid-border" data-testid="sprints-active-card">
            <div className="space-y-2">
              <TrendingUp className="w-8 h-8 text-primary" strokeWidth={2} />
              <div>
                <p className="text-2xl md:text-3xl font-bold text-white font-mono">
                  {overview?.active_sprints || 0}
                </p>
                <p className="text-xs text-muted-foreground">Sprints Ativos</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          <Button
            data-testid="new-task-button"
            onClick={() => navigate('/tasks')}
            className="bg-primary text-white hover:bg-primary/90 h-auto py-4"
          >
            <Plus className="w-5 h-5 mr-2" />
            Nova Task
          </Button>
          <Button
            data-testid="start-timer-button"
            onClick={() => navigate('/timer')}
            variant="outline"
            className="border-accent/30 text-accent hover:bg-accent/10 h-auto py-4"
          >
            <TimerIcon className="w-5 h-5 mr-2" />
            Iniciar Timer
          </Button>
          <Button
            data-testid="new-sprint-button"
            onClick={() => navigate('/sprints')}
            variant="outline"
            className="border-border hover:bg-card h-auto py-4 col-span-2 md:col-span-1"
          >
            <Target className="w-5 h-5 mr-2" />
            Novo Sprint
          </Button>
        </div>

        {/* Recent Tasks */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold text-white">Tasks Recentes</h3>
            <Button
              data-testid="view-all-tasks-button"
              variant="ghost"
              onClick={() => navigate('/tasks')}
              className="text-primary hover:text-primary/90"
            >
              Ver Todas
            </Button>
          </div>

          {recentTasks.length === 0 ? (
            <Card className="bg-card border-border p-8 text-center" data-testid="no-tasks-card">
              <Target className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
              <p className="text-muted-foreground">Nenhuma task ativa</p>
              <Button
                onClick={() => navigate('/tasks')}
                className="mt-4 bg-primary text-white"
              >
                Criar Primeira Task
              </Button>
            </Card>
          ) : (
            <div className="space-y-3">
              {recentTasks.map((task, index) => (
                <Card
                  key={task.task_id}
                  data-testid={`task-card-${index}`}
                  onClick={() => navigate('/tasks')}
                  className="bg-card border-border p-4 grid-border hover:border-primary/50 transition-all cursor-pointer"
                >
                  <div className="flex items-start gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge className={`${getCategoryColor(task.category)} text-xs font-mono`}>
                          {task.category}
                        </Badge>
                        {task.priority === 'high' && (
                          <Badge variant="destructive" className="text-xs">Alta</Badge>
                        )}
                      </div>
                      <h4 className="font-medium text-white truncate">{task.title}</h4>
                      {task.description && (
                        <p className="text-sm text-muted-foreground line-clamp-1 mt-1">
                          {task.description}
                        </p>
                      )}
                    </div>
                    {task.actual_time > 0 && (
                      <div className="text-right">
                        <p className="text-sm font-mono text-accent">{task.actual_time}m</p>
                      </div>
                    )}
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;