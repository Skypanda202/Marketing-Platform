import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { authService } from "../api/services";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(localStorage.getItem("accessToken")));

  useEffect(() => {
    if (!localStorage.getItem("accessToken")) return;
    authService
      .me()
      .then(({ data }) => setUser(data))
      .catch(() => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (payload) => {
    const { data } = await authService.login(payload);
    localStorage.setItem("accessToken", data.tokens.access);
    localStorage.setItem("refreshToken", data.tokens.refresh);
    setUser(data.user);
    return data.user;
  };

  const register = async (payload) => {
    const { data } = await authService.register(payload);
    localStorage.setItem("accessToken", data.tokens.access);
    localStorage.setItem("refreshToken", data.tokens.refresh);
    setUser(data.user);
    return data.user;
  };

  const logout = async () => {
    const refresh = localStorage.getItem("refreshToken");
    if (refresh) await authService.logout(refresh).catch(() => {});
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setUser(null);
  };

  const value = useMemo(() => ({ user, loading, login, register, logout, isAuthenticated: Boolean(user) }), [user, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
