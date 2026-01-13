interface AgentCardProps {
  name: string;
  model: string;
  messages: number;
  status: 'online' | 'offline';
}

export function AgentCard({ name, model, messages, status }: AgentCardProps) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
      <h3 className="text-white text-xl font-bold mb-4">{name}</h3>
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-gray-400">Status</span>
          <span className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${status === 'online' ? 'bg-green-400' : 'bg-red-400'}`} />
            <span className={status === 'online' ? 'text-green-400' : 'text-red-400'}>
              {status === 'online' ? 'Ativo' : 'Inativo'}
            </span>
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-gray-400">Modelo</span>
          <span className="text-white">{model}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-gray-400">Mensagens Hoje</span>
          <span className="text-white">{messages}</span>
        </div>
      </div>
    </div>
  );
}
