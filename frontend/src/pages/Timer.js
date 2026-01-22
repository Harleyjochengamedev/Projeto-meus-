import { useState, useEffect } from 'react';
import { axiosInstance } from '../App';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Play, Pause, RotateCcw, Coffee } from 'lucide-react';
import { toast } from 'sonner';

const Timer = () => {
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [isBreak, setIsBreak] = useState(false);
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [initialTime, setInitialTime] = useState(25 * 60);
  const [pomodoroCount, setPomodoroCount] = useState(0);
  const [todayTime, setTodayTime] = useState(0);

  useEffect(() => {
    loadTasks();
    loadTodayTime();
  }, []);

  useEffect(() => {
    let interval = null;
    if (isRunning && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft(time => time - 1);
      }, 1000);
    } else if (timeLeft === 0 && isRunning) {
      handleTimerComplete();
    }
    return () => clearInterval(interval);
  }, [isRunning, timeLeft]);

  const loadTasks = async () => {
    try {
      const response = await axiosInstance.get('/tasks?status=todo&status=in_progress');
      setTasks(response.data);
      if (response.data.length > 0 && !selectedTask) {
        setSelectedTask(response.data[0].task_id);
      }
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  };

  const loadTodayTime = async () => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const response = await axiosInstance.get(`/time-entries?date=${today}`);
      const total = response.data.reduce((sum, entry) => sum + entry.duration, 0);
      setTodayTime(total);
    } catch (error) {
      console.error('Error loading today time:', error);
    }
  };

  const handleTimerComplete = async () => {
    setIsRunning(false);
    
    if (!isBreak && selectedTask) {
      const duration = Math.floor(initialTime / 60);
      try {
        await axiosInstance.post('/time-entries', {
          task_id: selectedTask,
          duration: duration,
          entry_type: 'pomodoro'
        });
        toast.success(`Pomodoro concluído! ${duration} minutos registrados.`);
        setPomodoroCount(prev => prev + 1);
        loadTodayTime();
      } catch (error) {
        console.error('Error saving time entry:', error);
        toast.error('Erro ao registrar tempo');
      }
    }

    if (isBreak) {
      toast.success('Pausa concluída! Hora de voltar ao trabalho.');
      startPomodoro();
    } else {
      const newCount = pomodoroCount + 1;
      if (newCount % 4 === 0) {
        startLongBreak();
      } else {
        startShortBreak();
      }
    }
  };

  const startPomodoro = () => {
    if (!selectedTask && tasks.length > 0) {
      toast.error('Selecione uma task primeiro');
      return;
    }
    setIsBreak(false);
    setTimeLeft(25 * 60);
    setInitialTime(25 * 60);
    setIsRunning(true);
  };

  const startShortBreak = () => {
    setIsBreak(true);
    setTimeLeft(5 * 60);
    setInitialTime(5 * 60);
    setIsRunning(true);
    toast.success('Hora da pausa curta! (5 min)');
  };

  const startLongBreak = () => {
    setIsBreak(true);
    setTimeLeft(15 * 60);
    setInitialTime(15 * 60);
    setIsRunning(true);
    toast.success('Pausa longa! Você merece! (15 min)');
  };

  const toggleTimer = () => {
    if (!isRunning && !selectedTask && !isBreak && tasks.length > 0) {
      toast.error('Selecione uma task primeiro');
      return;
    }
    setIsRunning(!isRunning);
  };

  const resetTimer = () => {
    setIsRunning(false);
    setTimeLeft(initialTime);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const progress = ((initialTime - timeLeft) / initialTime) * 100;

  return (
    <div className="min-h-screen bg-background pb-24 md:pb-8">
      <main className="max-w-2xl mx-auto px-4 py-6 space-y-8">
        {/* Header */}
        <div className="text-center">
          <h2 className="text-2xl md:text-3xl font-bold text-white mb-2">Pomodoro Timer</h2>
          <p className="text-muted-foreground">Foco em 25 minutos</p>
        </div>

        {/* Task Selection */}
        {!isBreak && tasks.length > 0 && (
          <Card className="bg-card border-border p-6">
            <label className="text-sm text-muted-foreground mb-2 block">Task Atual</label>
            <Select
              value={selectedTask || ''}
              onValueChange={setSelectedTask}
              disabled={isRunning}
            >
              <SelectTrigger data-testid="select-task" className="bg-input border-border text-white">
                <SelectValue placeholder="Selecione uma task" />
              </SelectTrigger>
              <SelectContent>
                {tasks.map(task => (
                  <SelectItem key={task.task_id} value={task.task_id}>
                    {task.title}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </Card>
        )}

        {/* Timer Circle */}
        <Card className="bg-card border-border p-8 md:p-12">
          <div className="relative w-full max-w-xs mx-auto aspect-square">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="50%"
                cy="50%"
                r="45%"
                fill="none"
                stroke="rgba(255,255,255,0.1)"
                strokeWidth="8"
              />
              <circle
                cx="50%"
                cy="50%"
                r="45%"
                fill="none"
                stroke={isBreak ? 'hsl(var(--accent))' : 'hsl(var(--primary))'}
                strokeWidth="8"
                strokeDasharray="283"
                strokeDashoffset={283 - (283 * progress) / 100}
                strokeLinecap="round"
                className="transition-all duration-1000"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              {isBreak && <Coffee className="w-8 h-8 text-accent mb-2" />}
              <div className="text-5xl md:text-6xl font-bold text-white font-mono">
                {formatTime(timeLeft)}
              </div>
              <p className="text-sm text-muted-foreground mt-2">
                {isBreak ? 'Pausa' : 'Foco'}
              </p>
            </div>
          </div>

          {/* Controls */}
          <div className="flex justify-center gap-4 mt-8">
            <Button
              data-testid="reset-timer-button"
              onClick={resetTimer}
              variant="outline"
              size="lg"
              className="border-border"
            >
              <RotateCcw className="w-5 h-5" />
            </Button>
            <Button
              data-testid="toggle-timer-button"
              onClick={toggleTimer}
              size="lg"
              className="bg-primary text-white hover:bg-primary/90 px-12"
            >
              {isRunning ? (
                <><Pause className="w-5 h-5 mr-2" /> Pausar</>
              ) : (
                <><Play className="w-5 h-5 mr-2" /> Iniciar</>
              )}
            </Button>
          </div>
        </Card>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-4">
          <Card className="bg-card border-border p-6 text-center">
            <p className="text-3xl font-bold text-primary font-mono">{pomodoroCount}</p>
            <p className="text-sm text-muted-foreground mt-1">Pomodoros Hoje</p>
          </Card>
          <Card className="bg-card border-border p-6 text-center">
            <p className="text-3xl font-bold text-accent font-mono">{todayTime}m</p>
            <p className="text-sm text-muted-foreground mt-1">Tempo Total</p>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-3 gap-3">
          <Button
            onClick={startPomodoro}
            variant="outline"
            className="border-primary/30 text-primary hover:bg-primary/10"
            disabled={isRunning}
          >
            25m
          </Button>
          <Button
            onClick={startShortBreak}
            variant="outline"
            className="border-accent/30 text-accent hover:bg-accent/10"
            disabled={isRunning}
          >
            5m
          </Button>
          <Button
            onClick={startLongBreak}
            variant="outline"
            className="border-accent/30 text-accent hover:bg-accent/10"
            disabled={isRunning}
          >
            15m
          </Button>
        </div>
      </main>
    </div>
  );
};

export default Timer;