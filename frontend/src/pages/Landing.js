import { Code2, Clock, Target, TrendingUp, CheckCircle2, Zap } from 'lucide-react';
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
        {/* Gradient glow */}
        <div className="absolute inset-0 bg-gradient-radial from-primary/10 via-transparent to-transparent"></div>
        
        <div className="relative z-10 max-w-5xl mx-auto text-center">
          {/* Logo */}
          <div className="mb-8 flex justify-center">
            <div className="relative">
              <Code2 className="w-16 h-16 text-primary" strokeWidth={2} />
            </div>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 tracking-tight">
            Pare de se perder entre
            <br />
            <span className="text-primary">tasks, bugs e PRs</span>
          </h1>

          {/* Subheadline */}
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            DevFlow organiza sua rotina de desenvolvedor: planejamento, sprints pessoais,
            tracking de tempo e lembretes de code review em um só lugar.
          </p>

          {/* CTA Button */}
          <Button
            data-testid="login-button"
            onClick={handleLogin}
            size="lg"
            className="bg-primary text-white hover:bg-primary/90 text-lg px-8 py-6 h-auto shadow-[0_0_20px_-5px_rgba(99,102,241,0.5)]"
          >
            <Zap className="mr-2 h-5 w-5" />
            Começar Grátis
          </Button>

          <p className="mt-6 text-sm text-muted-foreground">
            ✨ Grátis para começar • 🚀 Setup em 2 minutos • 💻 Mobile-first
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-4 relative">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-16 text-white">
            Tudo que você precisa para manter o foco
          </h2>

          <div className="grid md:grid-cols-3 gap-6">
            <Card className="bg-card border-border p-6 grid-border hover:border-primary/50 transition-all">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <CheckCircle2 className="w-6 h-6 text-primary" strokeWidth={2} />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Planejamento Inteligente</h3>
              <p className="text-muted-foreground leading-relaxed">
                Organize tasks por categoria: estudos, bugs, PRs, projetos pessoais.
                Priorize e planeje sprints semanais.
              </p>
            </Card>

            <Card className="bg-card border-border p-6 grid-border hover:border-primary/50 transition-all">
              <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-4">
                <Clock className="w-6 h-6 text-accent" strokeWidth={2} />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Timer Pomodoro</h3>
              <p className="text-muted-foreground leading-relaxed">
                Técnica Pomodoro integrada (25min + pausas). Tracking automático
                de tempo gasto por task.
              </p>
            </Card>

            <Card className="bg-card border-border p-6 grid-border hover:border-primary/50 transition-all">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <TrendingUp className="w-6 h-6 text-primary" strokeWidth={2} />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Relatórios</h3>
              <p className="text-muted-foreground leading-relaxed">
                Veja sua produtividade em gráficos. Análise por categoria,
                tempo total e taxa de conclusão.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-24 px-4 bg-card/30">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-4">
              Feito para devs que querem evoluir
            </h2>
            <p className="text-muted-foreground">
              Dev solo, freelancer ou estudante — organize sua rotina e foque no que importa
            </p>
          </div>

          <div className="grid grid-cols-3 gap-8">
            <div className="text-center space-y-2">
              <div className="text-4xl font-bold text-primary">5+</div>
              <p className="text-sm text-muted-foreground">Categorias de Tasks</p>
            </div>
            <div className="text-center space-y-2">
              <div className="text-4xl font-bold text-accent">25min</div>
              <p className="text-sm text-muted-foreground">Pomodoro Timer</p>
            </div>
            <div className="text-center space-y-2">
              <div className="text-4xl font-bold text-primary">∞</div>
              <p className="text-sm text-muted-foreground">Sprints Pessoais</p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-24 px-4">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-white">
            Comece a organizar sua rotina hoje
          </h2>
          <Button
            data-testid="cta-login-button"
            onClick={handleLogin}
            size="lg"
            className="bg-primary text-white hover:bg-primary/90 text-lg px-8 py-6 h-auto"
          >
            <Target className="mr-2 h-5 w-5" />
            Criar Conta Grátis
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8 text-center text-sm text-muted-foreground">
        <p>DevFlow © 2025 • Organize, Execute, Evolua</p>
      </footer>
    </div>
  );
};

export default Landing;