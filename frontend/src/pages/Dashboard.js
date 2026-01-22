import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { axiosInstance } from '../App';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Avatar, AvatarImage, AvatarFallback } from '../components/ui/avatar';
import { Gamepad2, Users, Clock, Settings, LogOut, Sparkles } from 'lucide-react';
import { toast } from 'sonner';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [userRes, matchesRes] = await Promise.all([
        axiosInstance.get('/auth/me'),
        axiosInstance.get('/matches?limit=5')
      ]);
      setUser(userRes.data);
      setMatches(matchesRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
      toast.error('Erro ao carregar dados');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await axiosInstance.post('/auth/logout');
      toast.success('Logout realizado');
      navigate('/', { replace: true });
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  const needsProfile = !user?.gaming_profile;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Gamepad2 className="w-8 h-8 text-primary" />
            <h1 className="text-2xl font-bold text-white">PlayMatch</h1>
          </div>
          
          <div className="flex items-center gap-4">
            <Button
              data-testid="profile-nav-button"
              variant="ghost"
              onClick={() => navigate('/profile')}
              className="text-muted-foreground hover:text-white"
            >
              <Settings className="w-5 h-5 mr-2" />
              Perfil
            </Button>
            <Button
              data-testid="logout-button"
              variant="ghost"
              onClick={handleLogout}
              className="text-muted-foreground hover:text-destructive"
            >
              <LogOut className="w-5 h-5" />
            </Button>
            <Avatar className="w-10 h-10 border-2 border-primary">
              <AvatarImage src={user?.picture} alt={user?.name} />
              <AvatarFallback>{user?.name?.[0]}</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {/* Welcome Section */}
        <div className="space-y-4">
          <h2 className="text-3xl font-bold text-white">Bem-vindo, {user?.name}!</h2>
          <p className="text-muted-foreground">Encontre jogadores compatíveis com seu estilo</p>
        </div>

        {/* Profile Setup CTA */}
        {needsProfile && (
          <Card className="bg-gradient-to-r from-primary/20 to-secondary/20 border-primary/30 p-8" data-testid="setup-profile-card">
            <div className="flex items-start gap-6">
              <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-6 h-6 text-primary" />
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold text-white mb-2">Complete seu perfil!</h3>
                <p className="text-muted-foreground mb-4">
                  Para começar a fazer match, precisamos saber mais sobre seu estilo de jogo,
                  horários e preferências.
                </p>
                <Button
                  data-testid="complete-profile-button"
                  onClick={() => navigate('/profile')}
                  className="bg-primary text-white hover:bg-primary/90"
                >
                  Configurar Perfil
                </Button>
              </div>
            </div>
          </Card>
        )}

        {/* Quick Stats */}
        <div className="grid md:grid-cols-3 gap-6">
          <Card className="bg-card border-border/50 p-6" data-testid="matches-stat-card">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                <Users className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Matches Disponíveis</p>
                <p className="text-2xl font-bold text-white">{matches.length}</p>
              </div>
            </div>
          </Card>

          <Card className="bg-card border-border/50 p-6" data-testid="schedule-stat-card">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center">
                <Clock className="w-6 h-6 text-secondary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Horários Configurados</p>
                <p className="text-2xl font-bold text-white">
                  {Object.keys(user?.availability_schedule || {}).length}
                </p>
              </div>
            </div>
          </Card>

          <Card className="bg-card border-border/50 p-6" data-testid="style-stat-card">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                <Gamepad2 className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Estilo de Jogo</p>
                <p className="text-2xl font-bold text-white">
                  {user?.gaming_profile?.style || 'Não definido'}
                </p>
              </div>
            </div>
          </Card>
        </div>

        {/* Top Matches Preview */}
        {!needsProfile && matches.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-2xl font-bold text-white">Top Matches para Você</h3>
              <Button
                data-testid="view-all-matches-button"
                variant="ghost"
                onClick={() => navigate('/matches')}
                className="text-primary hover:text-primary/90"
              >
                Ver Todos
              </Button>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {matches.slice(0, 3).map((match, index) => (
                <Card
                  key={index}
                  className="bg-card border-border/50 hover:border-primary/50 transition-all p-6 match-card cursor-pointer"
                  onClick={() => navigate('/matches')}
                  data-testid={`match-preview-card-${index}`}
                >
                  <div className="flex items-start gap-4">
                    <Avatar className="w-14 h-14 border-2 border-primary/30">
                      <AvatarImage src={match.user.picture} alt={match.user.name} />
                      <AvatarFallback>{match.user.name[0]}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-bold text-white truncate">{match.user.name}</h4>
                      <p className="text-sm text-muted-foreground">
                        {match.user.gaming_profile?.style}
                      </p>
                      <div className="mt-2">
                        <div className="text-2xl font-bold text-secondary">
                          {match.compatibility_score}%
                        </div>
                        <p className="text-xs text-muted-foreground">compatibilidade</p>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!needsProfile && matches.length === 0 && (
          <Card className="bg-card border-border/50 p-12 text-center" data-testid="no-matches-card">
            <Users className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">Nenhum match encontrado</h3>
            <p className="text-muted-foreground">
              Aguarde enquanto procuramos jogadores compatíveis com seu perfil
            </p>
          </Card>
        )}
      </main>
    </div>
  );
};

export default Dashboard;