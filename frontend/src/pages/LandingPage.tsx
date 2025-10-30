import { Link } from 'react-router-dom';
import {Sun, Zap, Users, BarChart3, ArrowRight} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-yellow-50">
      {/* Header */}
      <header className="px-6 py-4 bg-white/80 backdrop-blur-sm border-b border-orange-100">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Sun className="w-8 h-8 text-orange-500" />
            <span className="text-2xl font-bold text-gray-900">SunOps</span>
          </div>
          <Link 
            to="/login"
            className="px-6 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
          >
            Entrar
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="px-6 py-20">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Gerencie seus projetos de 
            <span className="text-orange-500"> energia solar</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Plataforma completa para gestão de clientes, propostas e projetos solares. 
            Otimize suas vendas e acompanhe o desempenho da sua equipe.
          </p>
          <Link 
            to="/login"
            className="inline-flex items-center gap-2 px-8 py-4 bg-orange-500 text-white text-lg rounded-lg hover:bg-orange-600 transition-colors"
          >
            Começar Agora <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="px-6 py-16 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Tudo que você precisa em um só lugar
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center p-6">
              <Users className="w-12 h-12 text-orange-500 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Gestão de Clientes</h3>
              <p className="text-gray-600">Organize e acompanhe todos os seus clientes em um só lugar</p>
            </div>
            <div className="text-center p-6">
              <BarChart3 className="w-12 h-12 text-orange-500 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Propostas Inteligentes</h3>
              <p className="text-gray-600">Crie e gerencie propostas com acompanhamento de status</p>
            </div>
            <div className="text-center p-6">
              <Zap className="w-12 h-12 text-orange-500 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Projetos Solares</h3>
              <p className="text-gray-600">Monitore o progresso dos seus projetos em tempo real</p>
            </div>
            <div className="text-center p-6">
              <Sun className="w-12 h-12 text-orange-500 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Dashboard Inteligente</h3>
              <p className="text-gray-600">Visualize KPIs e métricas importantes do seu negócio</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-16 bg-gradient-to-r from-orange-500 to-yellow-500">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h2 className="text-3xl font-bold mb-4">
            Pronto para revolucionar sua gestão solar?
          </h2>
          <p className="text-xl mb-8">
            Junte-se às empresas que já confiam no SunOps para gerenciar seus projetos
          </p>
          <Link 
            to="/login"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white text-orange-500 text-lg rounded-lg hover:bg-gray-100 transition-colors"
          >
            Acessar Plataforma <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
}