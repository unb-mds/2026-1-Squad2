import { useState, useEffect } from 'react';
import { fetchPLDetalhado } from '../services/api';

export function usePLDetalhado(id) {
  const [pl, setPL] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setError(null);
    fetchPLDetalhado(id)
      .then((data) => setPL(data))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  return { pl, loading, error };
}