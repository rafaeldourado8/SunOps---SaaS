interface Service {
  name: string;
  status: 'online' | 'offline';
}

interface ServiceStatusProps {
  services: Service[];
}

export function ServiceStatus({ services }: ServiceStatusProps) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
      <h3 className="text-white text-xl font-bold mb-4">Status dos Serviços</h3>
      <div className="space-y-3">
        {services.map((service) => (
          <div key={service.name} className="flex items-center justify-between">
            <span className="text-gray-300">{service.name}</span>
            <span className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${service.status === 'online' ? 'bg-green-400' : 'bg-red-400'}`} />
              <span className={`text-sm ${service.status === 'online' ? 'text-green-400' : 'text-red-400'}`}>
                {service.status === 'online' ? 'Online' : 'Offline'}
              </span>
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
