import { useProjetosLei } from '../../hooks/useProjetosLei';
import NavBar from '../../components/NavBar';
import Footer from '../../components/Footer';
import FiltrosBar from '../../components/ProjetosLei/FiltrosBar';
import ListagemPL from '../../components/ProjetosLei/ListagemPL';
import Paginacao from '../../components/ProjetosLei/Paginacao';

export default function ProjetosLei() {
  const {
    projetos,
    total,
    totalPages,
    page,
    setPage,
    ordenar,
    setOrdenar,
    filtros,
    setFiltros,
    metaFiltros,
    loading,
    error,
    aplicarFiltros,
    limparFiltros,
    recarregar,
  } = useProjetosLei();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <NavBar />

      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-10">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-[#5B4FCF] mb-3">
            Projetos de Lei
          </h1>
          <p className="text-gray-500 max-w-2xl text-sm leading-relaxed">
            Explore a base de dados legislativa. Utilize os filtros avançados
            para encontrar proposições específicas por autoria, tema ou status
            atual.
          </p>
        </div>

        {/* Filtros */}
        <FiltrosBar
          filtros={filtros}
          setFiltros={setFiltros}
          metaFiltros={metaFiltros}
          onAplicar={aplicarFiltros}
          onLimpar={limparFiltros}
        />

        {/* Barra de resultados e ordenação */}
        <div className="flex items-center justify-between mb-5">
          <p className="text-sm font-semibold text-gray-700">
            {loading
              ? 'Carregando...'
              : `${total} Projeto${total !== 1 ? 's' : ''} Encontrado${total !== 1 ? 's' : ''}`}
          </p>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">Ordenar por:</span>
            <select
              value={ordenar}
              onChange={(e) => setOrdenar(e.target.value)}
              className="text-sm border border-gray-300 rounded-lg px-3 py-1.5 bg-white focus:outline-none focus:border-[#5B4FCF]"
            >
              <option value="recentes">Mais Recentes</option>
              <option value="antigos">Mais Antigos</option>
              <option value="numero_asc">Menor para Maior (Número do PL)</option>
            </select>
          </div>
        </div>

        {/* Grid de cards */}
        <ListagemPL
          projetos={projetos}
          loading={loading}
          error={error}
          onRecarregar={recarregar}
          onLimparFiltros={limparFiltros}
        />

        {/* Paginação */}
        {!loading && !error && (
          <Paginacao page={page} totalPages={totalPages} onPageChange={setPage} />
        )}
      </main>

      <Footer />
    </div>
  );
}
