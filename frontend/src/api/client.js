import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem("refreshToken");
      if (refresh) {
        const { data } = await axios.post(`${api.defaults.baseURL}/auth/token/refresh/`, { refresh });
        localStorage.setItem("accessToken", data.access);
        original.headers.Authorization = `Bearer ${data.access}`;
        return api(original);
      }
    }
    return Promise.reject(error);
  },
);

export default api;
