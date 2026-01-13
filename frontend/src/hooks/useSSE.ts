import { useEffect, useState } from 'react';

interface SSEEvent {
  type: string;
  timestamp: number;
  [key: string]: any;
}

export function useSSE(url: string) {
  const [data, setData] = useState<SSEEvent | null>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setData(parsed);
      } catch (err) {
        setError(err as Error);
      }
    };

    eventSource.onerror = () => {
      setError(new Error('SSE connection error'));
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [url]);

  return { data, error };
}
