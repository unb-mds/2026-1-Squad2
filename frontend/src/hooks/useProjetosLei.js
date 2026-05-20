import { useState, useEffect, useCallback } from 'react';
import { fetchProjetos, fetchFiltros } from '../services/api';

const FILTROS_INICIAL = {
  keyword: '',
  partido: '',
  uf: '',
  status: '',
  ano: '',
};

export function useProjetosLei() {
  const [projetos, setProjetos] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [page, setPage] = useState(1);
  const [ordenar, setOrdenar] = useState('recentes');
  const [filtros, setFiltros] = useState(FILTROS_INICIAL);
  const [filtrosAplicados, setFiltrosAplicados] = useState(FILTROS_INICIAL);
  const [metaFiltros, setMetaFiltros] = useState({ partidos: [], ufs: [], anos: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const carregarFiltros = useCallback(async () => {
    try {
      const data = await fetchFiltros();
      setMetaFiltros(data);
    } catch (e) {
      console.error('Erro ao carregar metadados dos filtros:', e);
    }
  }, []);

  const carregarProjetos = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchProjetos({
        ...filtrosAplicados,
        page,
        per_page: 6,
        ordenar,
      });
      setProjetos(data.projetos);
      setTotal(data.total);
      setTotalPages(data.total_pages);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [filtrosAplicados, page, ordenar]);

  useEffect(() => {
    carregarFiltros();
  }, [carregarFiltros]);

  useEffect(() => {
    carregarProjetos();
  }, [carregarProjetos]);

  const aplicarFiltros = () => {
    setFiltrosAplicados({ ...filtros });
    setPage(1);
  };

  const limparFiltros = () => {
    setFiltros(FILTROS_INICIAL);
    setFiltrosAplicados(FILTROS_INICIAL);
    setPage(1);
  };

  return {
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
    recarregar: carregarProjetos,
  };
}