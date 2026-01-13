import { PageHeader } from '../Common/PageHeader';

export function ConfigPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Configurações"
        description="Configure o sistema"
      />

      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <h3 className="text-white text-xl font-bold mb-4">Integrações</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
            <div>
              <p className="text-white font-medium">WhatsApp Gateway</p>
              <p className="text-gray-400 text-sm">Conectado via whatsapp-web.js</p>
            </div>
            <div className="w-2 h-2 rounded-full bg-green-400" />
          </div>
          <div className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
            <div>
              <p className="text-white font-medium">Gemini AI</p>
              <p className="text-gray-400 text-sm">API Key configurada</p>
            </div>
            <div className="w-2 h-2 rounded-full bg-green-400" />
          </div>
        </div>
      </div>
    </div>
  );
}
