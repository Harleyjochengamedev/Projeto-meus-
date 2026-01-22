import { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { axiosInstance } from '../App';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Avatar, AvatarImage, AvatarFallback } from '../components/ui/avatar';
import { ArrowLeft, Send, Gamepad2 } from 'lucide-react';
import { toast } from 'sonner';

const Chat = () => {
  const { matchId } = useParams();
  const navigate = useNavigate();
  const [chat, setChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [currentUserId, setCurrentUserId] = useState(null);
  const [otherUser, setOtherUser] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadChat();
    const interval = setInterval(loadChat, 3000); // Poll every 3 seconds
    return () => clearInterval(interval);
  }, [matchId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChat = async () => {
    try {
      const [chatRes, meRes] = await Promise.all([
        axiosInstance.get(`/chats/${matchId}`),
        axiosInstance.get('/auth/me')
      ]);
      
      setChat(chatRes.data);
      setMessages(chatRes.data.messages || []);
      setCurrentUserId(meRes.data.user_id);

      // Get match details to find other user
      const matchRes = await axiosInstance.get('/matches?limit=100');
      // This is a workaround - in production you'd want a dedicated endpoint
      // For now we just set a placeholder
      setOtherUser({ name: 'Parceiro' });
    } catch (error) {
      console.error('Error loading chat:', error);
      if (error.response?.status === 404) {
        toast.error('Chat não encontrado');
        navigate('/dashboard');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || sending) return;

    setSending(true);
    const messageText = newMessage;
    setNewMessage('');

    try {
      await axiosInstance.post(`/chats/${matchId}/message`, {
        text: messageText
      });
      
      // Reload chat to get the new message
      await loadChat();
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Erro ao enviar mensagem');
      setNewMessage(messageText);
    } finally {
      setSending(false);
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
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <Button
            data-testid="back-to-matches-button"
            variant="ghost"
            onClick={() => navigate('/matches')}
            className="text-muted-foreground hover:text-white"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Voltar
          </Button>
          <div className="flex items-center gap-3">
            <Avatar className="w-8 h-8 border-2 border-primary/30">
              <AvatarFallback>{otherUser?.name?.[0] || 'P'}</AvatarFallback>
            </Avatar>
            <h1 className="text-lg font-bold text-white">{otherUser?.name || 'Chat'}</h1>
          </div>
          <div className="w-24"></div>
        </div>
      </header>

      {/* Messages */}
      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-6 overflow-y-auto" data-testid="chat-messages-container">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <Card className="bg-card border-border/50 p-8 text-center" data-testid="no-messages-card">
              <Gamepad2 className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-bold text-white mb-2">Nenhuma mensagem ainda</h3>
              <p className="text-muted-foreground">
                Seja o primeiro a enviar uma mensagem!
              </p>
            </Card>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message, index) => {
              const isOwn = message.sender_id === currentUserId;
              return (
                <div
                  key={message.message_id || index}
                  data-testid={`message-${index}`}
                  className={`flex ${isOwn ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[70%] rounded-2xl px-4 py-3 ${
                      isOwn
                        ? 'bg-primary text-white'
                        : 'bg-card border border-border text-white'
                    }`}
                  >
                    <p className="text-sm break-words">{message.text}</p>
                    <p className={`text-xs mt-1 ${
                      isOwn ? 'text-white/70' : 'text-muted-foreground'
                    }`}>
                      {new Date(message.timestamp).toLocaleTimeString('pt-BR', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </p>
                  </div>
                </div>
              );
            })}
            <div ref={messagesEndRef} />
          </div>
        )}
      </main>

      {/* Input */}
      <footer className="border-t border-border bg-card/50 backdrop-blur-xl sticky bottom-0">
        <form
          onSubmit={handleSendMessage}
          className="max-w-4xl mx-auto px-4 py-4 flex gap-3"
        >
          <Input
            data-testid="message-input"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Digite sua mensagem..."
            className="bg-white/5 border-white/10 text-white flex-1"
            disabled={sending}
          />
          <Button
            data-testid="send-message-button"
            type="submit"
            disabled={!newMessage.trim() || sending}
            className="bg-primary text-white hover:bg-primary/90"
          >
            <Send className="w-5 h-5" />
          </Button>
        </form>
      </footer>
    </div>
  );
};

export default Chat;