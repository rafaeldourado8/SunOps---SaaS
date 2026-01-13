import { FileText, MessageSquare, Package } from 'lucide-react';
import { StatCard } from '../Common/StatCard';
import { ServiceStatus } from '../Common/ServiceStatus';

export function DashboardPage() {
  const services = [
    { name: 'API FastAPI', status: 'online' as const },
    { name: 'PostgreSQL', status: 'online' as const },
    { name: 'Redis Cache', status: 'online' as const },
    { name: 'RabbitMQ', status: 'online' as const },
    { name: 'WhatsApp Gateway', status: 'online' as const },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-white">Dashboard</h2>
        <p className="text-gray-400 mt-2">Visão geral do sistema</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard label="Orçamentos Hoje" value="12" icon={FileText} iconColor="#eab308" />
        <StatCard label="Mensagens WhatsApp" value="47" icon={MessageSquare} iconColor="#22c55e" />
        <StatCard label="Kits Cadastrados" value="8" icon={Package} iconColor="#3b82f6" />
      </div>

      <ServiceStatus services={services} />
    </div>
  );
}
