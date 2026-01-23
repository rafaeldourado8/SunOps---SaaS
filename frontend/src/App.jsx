import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import useAuthStore from './store/authStore';

// Pages
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import ClientesPage from './pages/ClientesPage';
import PropostasPage from './pages/PropostasPage';
import PremissasPage from './pages/PremissasPage';
import TemplatesPage from './pages/TemplatesPage';
import ConfiguracoesPage from './pages/ConfiguracoesPage';

// Components
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const initialize = useAuthStore((state) => state.initialize);

  useEffect(() => {
    initialize();
  }, [initialize]);

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          
          <Route path="/" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            <Route index element={<DashboardPage />} />
            <Route path="clientes" element={<ClientesPage />} />
            <Route path="propostas" element={<PropostasPage />} />
            <Route path="premissas" element={<PremissasPage />} />
            <Route path="templates" element={<TemplatesPage />} />
            <Route path="configuracoes" element={<ConfiguracoesPage />} />
          </Route>
          
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
      
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#1e293b',
            color: '#f1f5f9',
            border: '1px solid rgba(71, 85, 105, 0.5)',
            borderRadius: '12px',
          },
          success: {
            iconTheme: {
              primary: '#fbbf24',
              secondary: '#0f172a',
            },
          },
        }}
      />
    </>
  );
}

export default App;