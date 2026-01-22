import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { axiosInstance } from '../App';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Slider } from '../components/ui/slider';
import { ArrowLeft, Save, Gamepad2 } from 'lucide-react';
import { toast } from 'sonner';
import ScheduleGrid from '../components/ScheduleGrid';

const Profile = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [profile, setProfile] = useState({
    games: [],
    platform: 'PC',
    style: 'Casual',
    communication: 'Texto',
    tolerance: 3,
    goal: 'Diversão'
  });
  const [schedule, setSchedule] = useState({});
  const [gameInput, setGameInput] = useState('');

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await axiosInstance.get('/profile');
      const user = response.data;
      if (user.gaming_profile) {
        setProfile(user.gaming_profile);
      }
      if (user.availability_schedule) {
        setSchedule(user.availability_schedule);
      }
    } catch (error) {
      console.error('Error loading profile:', error);
      toast.error('Erro ao carregar perfil');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (profile.games.length === 0) {
      toast.error('Adicione pelo menos um jogo');
      return;
    }

    setSaving(true);
    try {
      await axiosInstance.put('/profile', {
        gaming_profile: profile,
        availability_schedule: schedule
      });
      toast.success('Perfil atualizado com sucesso!');
      navigate('/dashboard');
    } catch (error) {
      console.error('Error saving profile:', error);
      toast.error('Erro ao salvar perfil');
    } finally {
      setSaving(false);
    }
  };

  const addGame = () => {
    if (gameInput.trim() && !profile.games.includes(gameInput.trim())) {
      setProfile({ ...profile, games: [...profile.games, gameInput.trim()] });
      setGameInput('');
    }
  };

  const removeGame = (game) => {
    setProfile({ ...profile, games: profile.games.filter(g => g !== game) });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <Button
            data-testid="back-button"
            variant="ghost"
            onClick={() => navigate('/dashboard')}
            className="text-muted-foreground hover:text-white"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Voltar
          </Button>
          <div className="flex items-center gap-3">
            <Gamepad2 className="w-6 h-6 text-primary" />
            <h1 className="text-xl font-bold text-white">Meu Perfil</h1>
          </div>
          <div className="w-24"></div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-8 space-y-8">
        {/* Gaming Profile */}
        <Card className="bg-card border-border/50 p-8" data-testid="gaming-profile-card">
          <h2 className="text-2xl font-bold text-white mb-6">Perfil de Jogador</h2>
          
          <div className="space-y-6">
            {/* Games */}
            <div className="space-y-3">
              <Label className="text-white">Jogos Favoritos *</Label>
              <div className="flex gap-2">
                <Input
                  data-testid="game-input"
                  value={gameInput}
                  onChange={(e) => setGameInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addGame()}
                  placeholder="Ex: League of Legends, Valorant..."
                  className="bg-white/5 border-white/10 text-white"
                />
                <Button
                  data-testid="add-game-button"
                  onClick={addGame}
                  className="bg-primary text-white"
                >
                  Adicionar
                </Button>
              </div>
              <div className="flex flex-wrap gap-2">
                {profile.games.map((game, index) => (
                  <div
                    key={index}
                    data-testid={`game-tag-${index}`}
                    className="bg-primary/20 border border-primary/30 rounded-full px-4 py-2 flex items-center gap-2"
                  >
                    <span className="text-white text-sm">{game}</span>
                    <button
                      onClick={() => removeGame(game)}
                      className="text-white/60 hover:text-white"
                      data-testid={`remove-game-${index}`}
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Platform */}
            <div className="space-y-3">
              <Label className="text-white">Plataforma</Label>
              <Select
                value={profile.platform}
                onValueChange={(value) => setProfile({ ...profile, platform: value })}
              >
                <SelectTrigger data-testid="platform-select" className="bg-white/5 border-white/10 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="PC">PC</SelectItem>
                  <SelectItem value="Console">Console</SelectItem>
                  <SelectItem value="Mobile">Mobile</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Style */}
            <div className="space-y-3">
              <Label className="text-white">Estilo de Jogo</Label>
              <Select
                value={profile.style}
                onValueChange={(value) => setProfile({ ...profile, style: value })}
              >
                <SelectTrigger data-testid="style-select" className="bg-white/5 border-white/10 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Casual">🎈 Casual</SelectItem>
                  <SelectItem value="Competitivo">🔥 Competitivo</SelectItem>
                  <SelectItem value="Tryhard">⚔️ Tryhard</SelectItem>
                  <SelectItem value="Fun">😄 Fun / Meme</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Communication */}
            <div className="space-y-3">
              <Label className="text-white">Comunicação</Label>
              <Select
                value={profile.communication}
                onValueChange={(value) => setProfile({ ...profile, communication: value })}
              >
                <SelectTrigger data-testid="communication-select" className="bg-white/5 border-white/10 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Silencioso">🔇 Silencioso</SelectItem>
                  <SelectItem value="Voz ativa">🎧 Voz ativa</SelectItem>
                  <SelectItem value="Texto">💬 Texto</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Tolerance */}
            <div className="space-y-3">
              <Label className="text-white">Tolerância a Erros: {profile.tolerance}</Label>
              <Slider
                data-testid="tolerance-slider"
                value={[profile.tolerance]}
                onValueChange={([value]) => setProfile({ ...profile, tolerance: value })}
                min={1}
                max={5}
                step={1}
                className="py-4"
              />
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>Baixa</span>
                <span>Alta</span>
              </div>
            </div>

            {/* Goal */}
            <div className="space-y-3">
              <Label className="text-white">Objetivo Principal</Label>
              <Select
                value={profile.goal}
                onValueChange={(value) => setProfile({ ...profile, goal: value })}
              >
                <SelectTrigger data-testid="goal-select" className="bg-white/5 border-white/10 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Rank">Rank</SelectItem>
                  <SelectItem value="Diversão">Diversão</SelectItem>
                  <SelectItem value="Treino">Treino</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </Card>

        {/* Schedule */}
        <Card className="bg-card border-border/50 p-8" data-testid="schedule-card">
          <h2 className="text-2xl font-bold text-white mb-6">Horários Disponíveis</h2>
          <p className="text-muted-foreground mb-6">
            Selecione os horários em que você geralmente está disponível para jogar
          </p>
          <ScheduleGrid schedule={schedule} onChange={setSchedule} />
        </Card>

        {/* Save Button */}
        <div className="flex justify-end gap-4">
          <Button
            data-testid="cancel-button"
            variant="outline"
            onClick={() => navigate('/dashboard')}
            className="border-border text-white"
          >
            Cancelar
          </Button>
          <Button
            data-testid="save-profile-button"
            onClick={handleSave}
            disabled={saving || profile.games.length === 0}
            className="bg-primary text-white hover:bg-primary/90"
          >
            <Save className="w-5 h-5 mr-2" />
            {saving ? 'Salvando...' : 'Salvar Perfil'}
          </Button>
        </div>
      </main>
    </div>
  );
};

export default Profile;