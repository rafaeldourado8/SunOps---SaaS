import { useState, useEffect } from 'react';
import { api } from '../lib/api';

export function useKits() {
  const [kits, setKits] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getKits()
      .then(setKits)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { kits, loading, error };
}

export function useOrcamentos() {
  const [orcamentos, setOrcamentos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getOrcamentos()
      .then(setOrcamentos)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { orcamentos, loading, error };
}

export function useHealthCheck() {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.healthCheck()
      .then(setStatus)
      .catch(() => setStatus({ status: 'error' }))
      .finally(() => setLoading(false));
  }, []);

  return { status, loading };
}
