import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: 'gestor' | 'vendedor';
}

export default function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && user?.role !== requiredRole) {
    // Se o usuário não tem a role necessária, redireciona para o dashboard principal
    // Evita que um vendedor acesse /app/usuarios
    return <Navigate to="/app" replace />;
  }

  return <>{children}</>;
}