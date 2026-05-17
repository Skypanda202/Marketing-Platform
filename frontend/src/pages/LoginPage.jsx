import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { LockKeyhole, Search, Sparkles, Users } from "lucide-react";

import { useAuth } from "../context/AuthContext";
import { integrationService } from "../api/services";

export default function LoginPage({ mode }) {
  const isRegister = mode === "register";
  const navigate = useNavigate();
  const { login, register } = useAuth();
  const [form, setForm] = useState({ role: "BRAND", email: "", password: "", username: "", company_name: "", display_name: "", niche: "Lifestyle" });
  const [error, setError] = useState("");

  const update = (event) => setForm((state) => ({ ...state, [event.target.name]: event.target.value }));

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const user = isRegister ? await register(form) : await login({ email: form.email, password: form.password });
      navigate(user.role === "BRAND" ? "/brand" : user.role === "INFLUENCER" ? "/influencer" : "/admin-dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || "Authentication failed.");
    }
  };

  const startSocialLogin = async (provider) => {
    const { data } = provider === "META" ? await integrationService.metaAuthUrl() : await integrationService.googleAuthUrl();
    window.location.href = data.authorization_url;
  };

  return (
    <section className="mx-auto grid max-w-5xl gap-6 py-10 lg:grid-cols-[0.9fr_1.1fr]">
      <div className="surface flex min-h-[460px] flex-col justify-between overflow-hidden p-6">
        <div>
          <p className="eyebrow inline-flex items-center gap-2"><Sparkles size={15} /> InfluenceOS</p>
          <h1 className="mt-4 text-4xl font-black leading-tight">{isRegister ? "Build your campaign workspace." : "Step back into your campaign room."}</h1>
          <p className="mt-4 text-slate-500 dark:text-slate-400">Role-aware access for brands, creators, and platform operators.</p>
        </div>
        <div className="rounded-lg bg-ink p-5 text-white dark:bg-white dark:text-ink">
          <div className="flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded-md bg-white/12 dark:bg-black/10"><LockKeyhole size={18} /></span>
            <div>
              <p className="font-black">Secure by default</p>
              <p className="text-sm opacity-70">JWT sessions, protected routes, and role-based API access.</p>
            </div>
          </div>
        </div>
      </div>
      <form className="panel space-y-4 p-6" onSubmit={submit}>
        <div>
          <h2 className="text-2xl font-black">{isRegister ? "Create account" : "Login"}</h2>
          <p className="mt-1 text-sm text-slate-500">{isRegister ? "Choose a role and start with the essentials." : "Use your email and password to continue."}</p>
        </div>
        {isRegister && (
          <div className="grid gap-3 sm:grid-cols-2">
            <select className="input" name="role" value={form.role} onChange={update}>
              <option value="BRAND">Brand</option>
              <option value="INFLUENCER">Influencer</option>
            </select>
            <input className="input" name="username" placeholder="Username" value={form.username} onChange={update} required />
          </div>
        )}
        <input className="input" name="email" type="email" placeholder="Email" value={form.email} onChange={update} required />
        <input className="input" name="password" type="password" placeholder="Password" value={form.password} onChange={update} required />
        {isRegister && form.role === "BRAND" && <input className="input" name="company_name" placeholder="Company name" value={form.company_name} onChange={update} required />}
        {isRegister && form.role === "INFLUENCER" && (
          <div className="grid gap-3 sm:grid-cols-2">
            <input className="input" name="display_name" placeholder="Creator name" value={form.display_name} onChange={update} required />
            <input className="input" name="niche" placeholder="Niche" value={form.niche} onChange={update} />
          </div>
        )}
        {error && <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950 dark:text-red-200">{error}</p>}
        <button className="btn-primary w-full" type="submit">{isRegister ? "Create workspace" : "Enter workspace"}</button>
        <div className="grid gap-2 sm:grid-cols-2">
          <button className="btn-secondary" type="button" onClick={() => startSocialLogin("META")}><Users size={16} /> Facebook / Instagram</button>
          <button className="btn-secondary" type="button" onClick={() => startSocialLogin("GOOGLE")}><Search size={16} /> Google</button>
        </div>
        <p className="text-center text-sm text-slate-500">
          {isRegister ? "Already have an account? " : "New here? "}
          <Link className="font-semibold text-brand" to={isRegister ? "/login" : "/register"}>{isRegister ? "Login" : "Register"}</Link>
        </p>
      </form>
    </section>
  );
}
