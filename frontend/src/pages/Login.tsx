import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {Sun, Mail, Lock, AlertCircle} from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import api from '../services/api';
import toast from 'react-hot-toast';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  // Puxa as ações separadas da store
  const setToken = useAuthStore((state) => state.setToken);
  const setUser = useAuthStore((state) => state.setUser);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // OAuth2PasswordRequestForm - enviar como form data
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      // 1. Fazer o login
      const loginResponse = await api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { access_token } = loginResponse.data;

      // 2. Salvar o token na store IMEDIATAMENTE
      setToken(access_token);

      // 3. Buscar dados do usuário (o interceptador do api.ts vai funcionar agora)
      // Não precisamos mais de headers manuais aqui
      const userResponse = await api.get('/users/me');

      const userData = userResponse.data;
      
      // 4. Salvar os dados do usuário na store
      setUser(userData);
      
      toast.success(`Bem-vindo, ${userData.name}!`);
      navigate('/app');
      
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Email ou senha incorretos';
      setError(errorMessage);
      toast.error(errorMessage);
      setToken(null); // Limpa o token em caso de falha ao buscar o usuário
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-yellow-50 flex items-center justify-center px-6">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 text-3xl font-bold text-gray-900">
            <Sun className="w-8 h-8 text-orange-500" />
            SunOps
          </Link>
          <p className="text-gray-600 mt-2">Entre na sua conta</p>
        </div>

        {/* Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="flex items-center gap-2 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                <AlertCircle className="w-5 h-5" />
                <span className="text-sm">{error}</span>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  placeholder="seu@email.com"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Senha
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {loading ? 'Entrando...' : 'Entrar'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <Link to="/" className="text-sm text-orange-500 hover:text-orange-600">
              ← Voltar para o início
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}