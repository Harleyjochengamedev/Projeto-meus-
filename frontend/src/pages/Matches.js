import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { axiosInstance } from '../App';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Avatar, AvatarImage, AvatarFallback } from '../components/ui/avatar';
import { Badge } from '../components/ui/badge';
import { ArrowLeft, Heart, X, MessageCircle, Gamepad2 } from 'lucide-react';
import { toast } from 'sonner';

const Matches = () => {
  const navigate = useNavigate();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);

  useEffect(() => {
    loadMatches();
  }, []);

  const loadMatches = async () => {
    try {
      const response = await axiosInstance.get('/matches?limit=50');
      setMatches(response.data);
    } catch (error) {
      console.error('Error loading matches:', error);
      toast.error('Erro ao carregar matches');
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (match, action) => {
    try {
      setActionLoading(match.user.user_id);
      
      // First create match if it doesn't exist
      let matchId = match.match_id;
      if (!matchId) {
        const createResponse = await axiosInstance.post('/matches/create', null, {
          params: { other_user_id: match.user.user_id }
        });
        matchId = createResponse.data.match_id;
      }

      const response = await axiosInstance.post('/matches/action', {
        match_id: matchId,
        action: action
      });

      if (action === 'like') {
        toast.success('Match aceito! Você pode conversar agora.');
        if (response.data.chat_id) {
          navigate(`/chat/${matchId}`);
        }
      } else {
        toast.success('Match rejeitado');
      }

      // Remove from list
      setMatches(matches.filter(m => m.user.user_id !== match.user.user_id));
    } catch (error) {
      console.error('Error handling action:', error);
      toast.error('Erro ao processar ação');
    } finally {
      setActionLoading(null);
    }
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
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <Button
            data-testid="back-to-dashboard-button"
            variant="ghost"
            onClick={() => navigate('/dashboard')}
            className="text-muted-foreground hover:text-white"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Voltar
          </Button>
          <div className="flex items-center gap-3">
            <Gamepad2 className="w-6 h-6 text-primary" />
            <h1 className="text-xl font-bold text-white">Matches</h1>
          </div>
          <div className="w-24"></div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">Jogadores Compatíveis</h2>
          <p className="text-muted-foreground">
            {matches.length} {matches.length === 1 ? 'match encontrado' : 'matches encontrados'}
          </p>
        </div>

        {matches.length === 0 ? (
          <Card className="bg-card border-border/50 p-12 text-center" data-testid="no-matches-available">
            <MessageCircle className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">Nenhum match disponível</h3>
            <p className="text-muted-foreground mb-6">
              Não há jogadores compatíveis no momento. Volte mais tarde!
            </p>
            <Button
              onClick={() => navigate('/dashboard')}
              className="bg-primary text-white"
            >
              Voltar ao Dashboard
            </Button>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {matches.map((match, index) => (
              <Card
                key={match.user.user_id}
                data-testid={`match-card-${index}`}
                className="bg-card border-border/50 hover:border-primary/50 transition-all overflow-hidden match-card"
              >
                <div className="p-6 space-y-4">
                  {/* User Info */}
                  <div className="flex items-start gap-4">
                    <Avatar className="w-16 h-16 border-2 border-primary/30">
                      <AvatarImage src={match.user.picture} alt={match.user.name} />
                      <AvatarFallback>{match.user.name[0]}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-bold text-white text-lg truncate">
                        {match.user.name}
                      </h3>
                      <p className="text-sm text-muted-foreground">
                        {match.user.gaming_profile?.platform}
                      </p>
                    </div>
                  </div>

                  {/* Compatibility Score */}
                  <div className="bg-secondary/10 border border-secondary/20 rounded-lg p-4 text-center">
                    <div className="text-4xl font-bold text-secondary">
                      {match.compatibility_score}%
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">Compatibilidade</p>
                  </div>

                  {/* Gaming Profile */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Estilo:</span>
                      <Badge variant="secondary" className="bg-primary/20 text-primary border-0">
                        {match.user.gaming_profile?.style}
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Comunicação:</span>
                      <span className="text-white">{match.user.gaming_profile?.communication}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Objetivo:</span>
                      <span className="text-white">{match.user.gaming_profile?.goal}</span>
                    </div>
                  </div>

                  {/* Reasons */}
                  {match.reasons && match.reasons.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-xs text-muted-foreground font-medium">Por que compatíveis:</p>
                      {match.reasons.map((reason, idx) => (
                        <div key={idx} className="text-xs text-white bg-white/5 rounded px-3 py-2">
                          • {reason}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Games */}
                  {match.user.gaming_profile?.games && match.user.gaming_profile.games.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-xs text-muted-foreground font-medium">Jogos:</p>
                      <div className="flex flex-wrap gap-1">
                        {match.user.gaming_profile.games.slice(0, 3).map((game, idx) => (
                          <span
                            key={idx}
                            className="text-xs bg-white/5 rounded-full px-2 py-1 text-white"
                          >
                            {game}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex gap-3 pt-4">
                    <Button
                      data-testid={`reject-button-${index}`}
                      variant="outline"
                      className="flex-1 border-destructive/30 text-destructive hover:bg-destructive/10"
                      onClick={() => handleAction(match, 'skip')}
                      disabled={actionLoading === match.user.user_id}
                    >
                      <X className="w-4 h-4 mr-2" />
                      Pular
                    </Button>
                    <Button
                      data-testid={`accept-button-${index}`}
                      className="flex-1 bg-secondary text-secondary-foreground hover:bg-secondary/90"
                      onClick={() => handleAction(match, 'like')}
                      disabled={actionLoading === match.user.user_id}
                    >
                      <Heart className="w-4 h-4 mr-2" />
                      Aceitar
                    </Button>
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

export default Matches;