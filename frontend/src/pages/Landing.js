import { Gamepad2, Users, Clock, Star, Sparkles, TrendingUp } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';

const Landing = () => {
  const handleLogin = () => {
    // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    const redirectUrl = window.location.origin + '/dashboard';
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden px-4">
        {/* Background gradient glow */}
        <div className="absolute inset-0 gradient-glow opacity-30"></div>
        
        <div className="relative z-10 max-w-6xl mx-auto text-center">
          {/* Logo/Brand */}
          <div className="mb-8 flex justify-center">
            <div className="relative">
              <Gamepad2 className="w-20 h-20 text-primary" strokeWidth={1.5} />
              <div className="absolute -inset-4 bg-primary/20 rounded-full blur-xl"></div>
            </div>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 tracking-tight">
            Chega de partidas <span className="text-primary">tóxicas</span>.
            <br />
            Encontre seu <span className="text-secondary">squad ideal</span>.
          </h1>

          {/* Subheadline */}
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-10">
            Jogue com pessoas compatíveis com seu estilo, não só com seu rank.
            Match por comportamento, mentalidade e horários.
          </p>

          {/* CTA Button */}
          <Button
            data-testid="login-button"
            onClick={handleLogin}
            size="lg"
            className="bg-primary text-white hover:bg-primary/90 shadow-[0_0_20px_-5px_rgba(124,77,255,0.5)] text-lg px-8 py-6 h-auto"
          >
            <Sparkles className="mr-2 h-5 w-5" />
            Começar Grátis com Google
          </Button>

          {/* Trust Badge */}
          <p className="mt-6 text-sm text-muted-foreground">
            ✨ Grátis para começar • 🎮 Match inteligente • 🔒 100% seguro
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-4 relative">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-16 text-white">
            Como funciona
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <Card className="bg-card border-border/50 p-8 hover:border-primary/50 transition-all group relative overflow-hidden">
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <Users className="w-7 h-7 text-primary" strokeWidth={1.5} />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Match por Estilo</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Encontre jogadores com o mesmo estilo: Casual, Competitivo, Tryhard ou Fun.
                  Compatibilidade real, não apenas rank.
                </p>
              </div>
            </Card>

            {/* Feature 2 */}
            <Card className="bg-card border-border/50 p-8 hover:border-primary/50 transition-all group relative overflow-hidden">
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-xl bg-secondary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <Clock className="w-7 h-7 text-secondary" strokeWidth={1.5} />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Horários Compatíveis</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Configure seus horários disponíveis. Match automático apenas com quem joga
                  no mesmo período que você.
                </p>
              </div>
            </Card>

            {/* Feature 3 */}
            <Card className="bg-card border-border/50 p-8 hover:border-primary/50 transition-all group relative overflow-hidden">
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <Star className="w-7 h-7 text-primary" strokeWidth={1.5} />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Score Comportamental</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Avalie seus parceiros após jogar. Sistema inteligente afasta jogadores
                  tóxicos e destaca os melhores.
                </p>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-24 px-4 bg-card/30">
        <div className="max-w-4xl mx-auto text-center">
          <div className="grid grid-cols-3 gap-8">
            <div className="space-y-2">
              <div className="text-4xl font-bold text-primary">95%</div>
              <p className="text-sm text-muted-foreground">Compatibilidade Média</p>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-secondary">80%</div>
              <p className="text-sm text-muted-foreground">Menos Toxicidade</p>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-primary">3x</div>
              <p className="text-sm text-muted-foreground">Mais Diversão</p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-24 px-4">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-white">
            Pronto para jogar com seu squad perfeito?
          </h2>
          <Button
            data-testid="cta-login-button"
            onClick={handleLogin}
            size="lg"
            className="bg-primary text-white hover:bg-primary/90 shadow-[0_0_20px_-5px_rgba(124,77,255,0.5)] text-lg px-8 py-6 h-auto"
          >
            <TrendingUp className="mr-2 h-5 w-5" />
            Criar Conta Grátis
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8 text-center text-sm text-muted-foreground">
        <p>PlayMatch © 2025 • Jogue melhor, jogue junto</p>
      </footer>
    </div>
  );
};

export default Landing;