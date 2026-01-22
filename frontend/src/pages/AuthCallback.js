import { useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { axiosInstance } from '../App';
import { toast } from 'sonner';

const AuthCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const hasProcessed = useRef(false);

  useEffect(() => {
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processAuth = async () => {
      try {
        const hash = location.hash.substring(1);
        const params = new URLSearchParams(hash);
        const sessionId = params.get('session_id');

        if (!sessionId) {
          toast.error('Sessão inválida');
          navigate('/', { replace: true });
          return;
        }

        const response = await axiosInstance.post('/auth/callback', null, {
          params: { session_id: sessionId }
        });

        const user = response.data;
        
        toast.success(`Bem-vindo, ${user.name}!`);
        navigate('/dashboard', { replace: true, state: { user } });
      } catch (error) {
        console.error('Auth error:', error);
        toast.error('Erro na autenticação. Tente novamente.');
        navigate('/', { replace: true });
      }
    };

    processAuth();
  }, [navigate, location]);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-center space-y-4">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary mx-auto"></div>
        <p className="text-muted-foreground">Autenticando...</p>
      </div>
    </div>
  );
};

export default AuthCallback;