// frontend/src/App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Clientes from './pages/Clientes';
import Propostas from './pages/Propostas';
import Projetos from './pages/Projetos';
import Usuarios from './pages/Usuarios';
import Financeiro from './pages/Financeiro';
// --- 1. Importar os novos componentes ---
import PropostaDimensionamento from './pages/PropostaDimensionamento'; 
import PropostaPreview from './pages/PropostaPreview'; // <-- LINHA ADICIONADA

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          {/* Rotas Públicas */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          
          {/* Rotas Privadas */}
          <Route path="/app" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            <Route index element={<Dashboard />} />
            <Route path="clientes" element={<Clientes />} />
            
            {/* --- 2. Atualizar Rotas de Propostas --- */}
            {/* A lista de propostas */}
            <Route path="propostas" element={<Propostas />} /> 
            {/* A nova rota para a página de edição/dimensionamento */}
            <Route 
              path="propostas/:propostaId/dimensionamento" 
              element={<PropostaDimensionamento />} 
            />
            {/* --- 3. ADICIONAR A NOVA ROTA DE PREVIEW --- */}
            <Route 
              path="propostas/:propostaId/preview" 
              element={<PropostaPreview />} 
            />

            <Route path="projetos" element={<Projetos />} />
            <Route path="usuarios" element={
              <ProtectedRoute requiredRole="gestor">
                <Usuarios />
              </ProtectedRoute>
            } />
            <Route path="financeiro" element={
              <ProtectedRoute requiredRole="gestor">
                <Financeiro />
              </ProtectedRoute>
            } />
          </Route>

          {/* Redirect para landing page */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;