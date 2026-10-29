import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

export function useClock() {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);
  return now;
}

export function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(() => window.matchMedia(query).matches);
  useEffect(() => {
    const media = window.matchMedia(query);
    const change = () => setMatches(media.matches);
    media.addEventListener('change', change);
    return () => media.removeEventListener('change', change);
  }, [query]);
  return matches;
}

export function useUrlState(key: string, fallback = ''): [string, (value: string) => void] {
  const [params, setParams] = useSearchParams();
  return [
    params.get(key) || fallback,
    (value) =>
      setParams(
        (previous) => {
          const next = new URLSearchParams(previous);
          if (value && value !== fallback) next.set(key, value);
          else next.delete(key);
          return next;
        },
        { replace: true },
      ),
  ];
}

export function useDebouncedValue<T>(value: T, delay = 250) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);
  }, [value, delay]);
  return debounced;
}
