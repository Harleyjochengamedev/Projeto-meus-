import { useState, useEffect } from 'react';
import { axiosInstance } from '../App';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Badge } from '../components/ui/badge';
import { Plus, Target, Calendar } from 'lucide-react';
import { toast } from 'sonner';

const Sprints = () => {
  const [sprints, setSprints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [newSprint, setNewSprint] = useState({
    name: '',
    goal: '',
    start_date: '',
    end_date: ''
  });

  useEffect(() => {
    loadSprints();
  }, []);

  const loadSprints = async () => {
    try {
      const response = await axiosInstance.get('/sprints');
      setSprints(response.data);
    } catch (error) {
      console.error('Error loading sprints:', error);
      toast.error('Erro ao carregar sprints');
    } finally {
      setLoading(false);
    }
  };

  const createSprint = async () => {
    if (!newSprint.name.trim() || !newSprint.start_date || !newSprint.end_date) {
      toast.error('Preencha todos os campos obrigatórios');
      return;
    }

    try {
      const sprintData = {
        ...newSprint,
        start_date: new Date(newSprint.start_date).toISOString(),
        end_date: new Date(newSprint.end_date).toISOString()
      };
      await axiosInstance.post('/sprints', sprintData);
      toast.success('Sprint criado!');
      setDialogOpen(false);
      setNewSprint({ name: '', goal: '', start_date: '', end_date: '' });
      loadSprints();
    } catch (error) {
      console.error('Error creating sprint:', error);
      toast.error('Erro ao criar sprint');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const getDaysLeft = (endDate) => {
    const end = new Date(endDate);
    const now = new Date();
    const diff = Math.ceil((end - now) / (1000 * 60 * 60 * 24));
    return diff;
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
      <main className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl md:text-3xl font-bold text-white">Sprints Pessoais</h2>
            <p className="text-sm text-muted-foreground mt-1">
              {sprints.length} {sprints.length === 1 ? 'sprint' : 'sprints'}
            </p>
          </div>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button data-testid="create-sprint-button" className="bg-primary text-white">
                <Plus className="w-5 h-5 mr-2" />
                Novo Sprint
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-card border-border">
              <DialogHeader>
                <DialogTitle className="text-white">Criar Novo Sprint</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 mt-4">
                <div className="space-y-2">
                  <Label className="text-white">Nome *</Label>
                  <Input
                    data-testid="sprint-name-input"
                    value={newSprint.name}
                    onChange={(e) => setNewSprint({ ...newSprint, name: e.target.value })}
                    placeholder="Ex: Sprint Semana 1"
                    className="bg-input border-border text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-white">Objetivo</Label>
                  <Textarea
                    data-testid="sprint-goal-input"
                    value={newSprint.goal}
                    onChange={(e) => setNewSprint({ ...newSprint, goal: e.target.value })}
                    placeholder="O que você quer alcançar?"
                    className="bg-input border-border text-white"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label className="text-white">Data Início *</Label>
                    <Input
                      data-testid="sprint-start-date-input"
                      type="date"
                      value={newSprint.start_date}
                      onChange={(e) => setNewSprint({ ...newSprint, start_date: e.target.value })}
                      className="bg-input border-border text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-white">Data Fim *</Label>
                    <Input
                      data-testid="sprint-end-date-input"
                      type="date"
                      value={newSprint.end_date}
                      onChange={(e) => setNewSprint({ ...newSprint, end_date: e.target.value })}
                      className="bg-input border-border text-white"
                    />
                  </div>
                </div>
                <Button
                  data-testid="save-sprint-button"
                  onClick={createSprint}
                  className="w-full bg-primary text-white"
                >
                  Criar Sprint
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        {/* Sprints List */}
        {sprints.length === 0 ? (
          <Card className="bg-card border-border p-12 text-center" data-testid="no-sprints">
            <Target className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground mb-4">Nenhum sprint criado ainda</p>
            <Button
              onClick={() => setDialogOpen(true)}
              className="bg-primary text-white"
            >
              Criar Primeiro Sprint
            </Button>
          </Card>
        ) : (
          <div className="space-y-4">
            {sprints.map((sprint, index) => {
              const daysLeft = getDaysLeft(sprint.end_date);
              const isActive = sprint.status === 'active';
              
              return (
                <Card
                  key={sprint.sprint_id}
                  data-testid={`sprint-card-${index}`}
                  className="bg-card border-border p-6 grid-border hover:border-primary/50 transition-all"
                >
                  <div className="space-y-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-xl font-bold text-white">{sprint.name}</h3>
                          <Badge
                            variant={isActive ? 'default' : 'secondary'}
                            className={isActive ? 'bg-primary text-white' : 'bg-secondary'}
                          >
                            {isActive ? 'Ativo' : 'Concluído'}
                          </Badge>
                        </div>
                        {sprint.goal && (
                          <p className="text-muted-foreground">{sprint.goal}</p>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center gap-6 text-sm">
                      <div className="flex items-center gap-2 text-muted-foreground">
                        <Calendar className="w-4 h-4" />
                        {formatDate(sprint.start_date)} - {formatDate(sprint.end_date)}
                      </div>
                      {isActive && daysLeft >= 0 && (
                        <Badge variant="outline" className="font-mono">
                          {daysLeft} {daysLeft === 1 ? 'dia restante' : 'dias restantes'}
                        </Badge>
                      )}
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
};

export default Sprints;