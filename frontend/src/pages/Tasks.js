import { useState, useEffect } from 'react';
import { axiosInstance } from '../App';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Badge } from '../components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Plus, Clock, CheckCircle2, Filter } from 'lucide-react';
import { toast } from 'sonner';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    category: 'task',
    priority: 'medium',
    estimated_time: ''
  });

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await axiosInstance.get('/tasks');
      setTasks(response.data);
    } catch (error) {
      console.error('Error loading tasks:', error);
      toast.error('Erro ao carregar tasks');
    } finally {
      setLoading(false);
    }
  };

  const createTask = async () => {
    if (!newTask.title.trim()) {
      toast.error('Título é obrigatório');
      return;
    }

    try {
      const taskData = {
        ...newTask,
        estimated_time: newTask.estimated_time ? parseInt(newTask.estimated_time) : null
      };
      await axiosInstance.post('/tasks', taskData);
      toast.success('Task criada!');
      setDialogOpen(false);
      setNewTask({ title: '', description: '', category: 'task', priority: 'medium', estimated_time: '' });
      loadTasks();
    } catch (error) {
      console.error('Error creating task:', error);
      toast.error('Erro ao criar task');
    }
  };

  const toggleTaskStatus = async (task) => {
    try {
      const newStatus = task.status === 'done' ? 'todo' : 'done';
      await axiosInstance.put(`/tasks/${task.task_id}`, { status: newStatus });
      loadTasks();
      toast.success(newStatus === 'done' ? 'Task concluída!' : 'Task reaberta');
    } catch (error) {
      console.error('Error updating task:', error);
      toast.error('Erro ao atualizar task');
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

  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true;
    if (filter === 'active') return task.status !== 'done';
    if (filter === 'completed') return task.status === 'done';
    return true;
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pb-24 md:pb-8">
      <main className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl md:text-3xl font-bold text-white">Minhas Tasks</h2>
            <p className="text-sm text-muted-foreground mt-1">
              {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} total
            </p>
          </div>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button data-testid="create-task-button" className="bg-primary text-white">
                <Plus className="w-5 h-5 mr-2" />
                Nova Task
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-card border-border">
              <DialogHeader>
                <DialogTitle className="text-white">Criar Nova Task</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 mt-4">
                <div className="space-y-2">
                  <Label className="text-white">Título *</Label>
                  <Input
                    data-testid="task-title-input"
                    value={newTask.title}
                    onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                    placeholder="Ex: Implementar autenticação"
                    className="bg-input border-border text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-white">Descrição</Label>
                  <Textarea
                    data-testid="task-description-input"
                    value={newTask.description}
                    onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                    placeholder="Detalhes da task..."
                    className="bg-input border-border text-white"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label className="text-white">Categoria</Label>
                    <Select
                      value={newTask.category}
                      onValueChange={(value) => setNewTask({ ...newTask, category: value })}
                    >
                      <SelectTrigger data-testid="task-category-select" className="bg-input border-border text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="task">Task</SelectItem>
                        <SelectItem value="study">Estudo</SelectItem>
                        <SelectItem value="pr">PR</SelectItem>
                        <SelectItem value="bug">Bug</SelectItem>
                        <SelectItem value="project">Projeto</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label className="text-white">Prioridade</Label>
                    <Select
                      value={newTask.priority}
                      onValueChange={(value) => setNewTask({ ...newTask, priority: value })}
                    >
                      <SelectTrigger data-testid="task-priority-select" className="bg-input border-border text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="low">Baixa</SelectItem>
                        <SelectItem value="medium">Média</SelectItem>
                        <SelectItem value="high">Alta</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <div className="space-y-2">
                  <Label className="text-white">Tempo Estimado (min)</Label>
                  <Input
                    data-testid="task-estimated-time-input"
                    type="number"
                    value={newTask.estimated_time}
                    onChange={(e) => setNewTask({ ...newTask, estimated_time: e.target.value })}
                    placeholder="Ex: 60"
                    className="bg-input border-border text-white"
                  />
                </div>
                <Button
                  data-testid="save-task-button"
                  onClick={createTask}
                  className="w-full bg-primary text-white"
                >
                  Criar Task
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        {/* Filters */}
        <div className="flex gap-2">
          <Button
            data-testid="filter-all"
            variant={filter === 'all' ? 'default' : 'outline'}
            onClick={() => setFilter('all')}
            className={filter === 'all' ? 'bg-primary text-white' : 'border-border'}
            size="sm"
          >
            Todas
          </Button>
          <Button
            data-testid="filter-active"
            variant={filter === 'active' ? 'default' : 'outline'}
            onClick={() => setFilter('active')}
            className={filter === 'active' ? 'bg-primary text-white' : 'border-border'}
            size="sm"
          >
            Ativas
          </Button>
          <Button
            data-testid="filter-completed"
            variant={filter === 'completed' ? 'default' : 'outline'}
            onClick={() => setFilter('completed')}
            className={filter === 'completed' ? 'bg-primary text-white' : 'border-border'}
            size="sm"
          >
            Concluídas
          </Button>
        </div>

        {/* Tasks List */}
        {filteredTasks.length === 0 ? (
          <Card className="bg-card border-border p-12 text-center" data-testid="no-tasks">
            <Filter className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">Nenhuma task encontrada</p>
          </Card>
        ) : (
          <div className="space-y-3">
            {filteredTasks.map((task, index) => (
              <Card
                key={task.task_id}
                data-testid={`task-item-${index}`}
                className="bg-card border-border p-4 grid-border hover:border-primary/50 transition-all"
              >
                <div className="flex items-start gap-3">
                  <button
                    data-testid={`toggle-task-${index}`}
                    onClick={() => toggleTaskStatus(task)}
                    className="mt-1 flex-shrink-0"
                  >
                    {task.status === 'done' ? (
                      <CheckCircle2 className="w-6 h-6 text-emerald-500" />
                    ) : (
                      <div className="w-6 h-6 rounded-full border-2 border-muted-foreground hover:border-primary transition-colors" />
                    )}
                  </button>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-2 flex-wrap">
                      <Badge className={`${getCategoryColor(task.category)} text-xs font-mono`}>
                        {task.category}
                      </Badge>
                      {task.priority === 'high' && (
                        <Badge variant="destructive" className="text-xs">Alta</Badge>
                      )}
                      {task.actual_time > 0 && (
                        <Badge variant="outline" className="text-xs font-mono text-accent border-accent/30">
                          <Clock className="w-3 h-3 mr-1" />
                          {task.actual_time}m
                        </Badge>
                      )}
                    </div>
                    <h4 className={`font-medium text-white mb-1 ${task.status === 'done' ? 'line-through opacity-60' : ''}`}>
                      {task.title}
                    </h4>
                    {task.description && (
                      <p className="text-sm text-muted-foreground line-clamp-2">{task.description}</p>
                    )}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default Tasks;