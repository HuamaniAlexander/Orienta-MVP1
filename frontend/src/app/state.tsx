import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { api, mutate, ApiError } from "../shared/api";
import type {
  Recommendation,
  RecommendationInput,
  User,
} from "../shared/types";
interface State {
  selection: number[];
  toggle: (id: number) => void;
  clear: () => void;
  user: User | null;
  authLoading: boolean;
  refreshUser: () => Promise<void>;
  logout: () => Promise<void>;
  result: Recommendation | null;
  setResult: (r: Recommendation | null) => void;
  input: RecommendationInput | null;
  setInput: (v: RecommendationInput | null) => void;
  notice: string;
  setNotice: (v: string) => void;
}
const Context = createContext<State | null>(null);
function initialSelection() {
  try {
    const value = JSON.parse(localStorage.getItem("orienta-selection") ?? "[]");
    return Array.isArray(value)
      ? ([
          ...new Set(
            value.filter((v: unknown) => Number.isInteger(v) && Number(v) >= 0),
          ),
        ].slice(0, 2) as number[])
      : [];
  } catch {
    return [];
  }
}
export function AppProvider({ children }: { children: ReactNode }) {
  const [selection, setSelection] = useState<number[]>(initialSelection),
    [user, setUser] = useState<User | null>(null),
    [authLoading, setAuthLoading] = useState(true),
    [result, setResult] = useState<Recommendation | null>(null),
    [input, setInput] = useState<RecommendationInput | null>(null),
    [notice, setNotice] = useState("");
  const refreshUser = async () => {
    try {
      setUser(await api<User>("/auth/me"));
    } catch (e) {
      setUser(null);
      if (!(e instanceof ApiError && e.status === 401))
        setNotice(
          "El acceso a tu cuenta no está disponible. Puedes seguir explorando.",
        );
    } finally {
      setAuthLoading(false);
    }
  };
  useEffect(() => {
    void refreshUser();
  }, []);
  useEffect(() => {
    localStorage.setItem("orienta-selection", JSON.stringify(selection));
  }, [selection]);
  const toggle = (id: number) =>
    setSelection((old) => {
      if (old.includes(id)) return old.filter((v) => v !== id);
      if (old.length === 2) {
        setNotice("Ya elegiste dos carreras. Quita una para seleccionar otra.");
        return old;
      }
      return [...old, id];
    });
  const logout = async () => {
    await mutate("/auth/logout");
    setUser(null);
    setResult(null);
    setInput(null);
    setNotice("Sesión cerrada y respuestas de esta sesión borradas.");
  };
  return (
    <Context.Provider
      value={{
        selection,
        toggle,
        clear: () => setSelection([]),
        user,
        authLoading,
        refreshUser,
        logout,
        result,
        setResult,
        input,
        setInput,
        notice,
        setNotice,
      }}
    >
      {children}
    </Context.Provider>
  );
}
export function useApp() {
  const value = useContext(Context);
  if (!value) throw new Error("AppProvider requerido");
  return value;
}
