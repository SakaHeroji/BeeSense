import { createContext, useContext } from 'react';
import type { Capabilities, FieldError, Session } from './types';

export const AppContext = createContext<{
  cap: Capabilities;
  session: Session;
  notify: (message: string) => void;
} | null>(null);
export const FieldErrorsContext = createContext<FieldError[]>([]);
export function useApp() {
  const context = useContext(AppContext);
  if (!context) throw new Error('App context unavailable');
  return context;
}
