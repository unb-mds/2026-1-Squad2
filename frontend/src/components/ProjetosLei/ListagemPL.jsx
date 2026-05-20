import CardPL from './CardPL';
import CardPLSkeleton from './CardPLSkeleton';

export default function ListagemPL({ projetos, loading, error, onRecarregar, onLimparFiltros }) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {Array.from({ length: 6 }).map((_, i) => (
          <CardPLSkeleton key={i} />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <p className="text-gray-500 text-center text-sm">
          Não foi possível carregar os projetos. Tente novamente.
        </p>
        <button
          onClick={onRecarregar}
          className="px-5 py-2 text-sm font-semibold bg-[#5B4FCF] text-white rounded-lg hover:bg-[#4338CA] transition-colors"
        >
          Tentar novamente
        </button>
      </div>
    );
  }

  if (projetos.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <p className="text-gray-500 text-center text-sm">
          Nenhum projeto encontrado com os filtros selecionados.
        </p>
        <button
          onClick={onLimparFiltros}
          className="px-5 py-2 text-sm font-semibold border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
        >
          Limpar filtros
        </button>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      {projetos.map((projeto) => (
        <CardPL key={projeto.id} projeto={projeto} />
      ))}
    </div>
  );
}