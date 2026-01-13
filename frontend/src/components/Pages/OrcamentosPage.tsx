import { PageHeader } from '../Common/PageHeader';

export function OrcamentosPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Orçamentos"
        description="Gerencie seus orçamentos"
        action={
          <button className="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold px-6 py-3 rounded-lg transition">
            + Novo Orçamento
          </button>
        }
      />

      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <p className="text-gray-400 text-center py-8">Nenhum orçamento cadastrado ainda</p>
      </div>
    </div>
  );
}
