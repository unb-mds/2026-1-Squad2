import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { fetchPLDetalhado } from '../services/api';

export function usePLDetalhado(id) {
  const [pl, setPL] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { state } = useLocation();

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setError(null);
    fetchPLDetalhado(id, state)
      .then((data) => setPL(data))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id, state]);

  return { pl, loading, error };
}