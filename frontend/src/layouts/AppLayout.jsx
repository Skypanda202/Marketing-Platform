import { Bell, Compass, LogOut, Moon, Sun, Users } from "lucide-react";
import { Link, Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";

export default function AppLayout() {
  const { user, logout } = useAuth();
  const { dark, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const dashboardPath = user?.role === "BRAND" ? "/brand" : user?.role === "INFLUENCER" ? "/influencer" : "/admin-dashboard";
  const navClass = "rounded-md px-3 py-2 transition hover:bg-white hover:text-ink dark:hover:bg-white/10 dark:hover:text-white";

  return (
    <div className="min-h-screen text-ink dark:text-white">
      <header className="sticky top-0 z-30 border-b border-black/10 bg-cloud/75 backdrop-blur-xl dark:border-white/10 dark:bg-ink/75">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <Link to="/" className="flex items-center gap-3 text-base font-black">
            <span className="grid h-10 w-10 place-items-center rounded-lg bg-ink text-white shadow-soft dark:bg-white dark:text-ink"><Compass size={19} /></span>
            <span>
              Nexfluency
              <span className="block text-[10px] font-bold uppercase tracking-[0.18em] text-slate-500">Campaign studio</span>
            </span>
          </Link>
          <nav className="hidden items-center gap-2 rounded-lg border border-black/10 bg-white/55 p-1 text-sm font-semibold text-slate-600 shadow-sm backdrop-blur dark:border-white/10 dark:bg-white/7 dark:text-slate-300 md:flex">
            {user && <Link className={navClass} to={dashboardPath}>Dashboard</Link>}
            {user && <Link className={navClass} to="/feed">Feed</Link>}
            {user?.role === "BRAND" && <Link className={navClass} to="/discovery">Discovery</Link>}
            {user?.role === "BRAND" && <Link className={navClass} to="/integrations">Ads</Link>}
            {user && <Link className={navClass} to="/analytics">Analytics</Link>}
            {user && <Link className={navClass} to="/messages">Messages</Link>}
            {!user && <Link className={navClass} to="/register">Register</Link>}
          </nav>
          <div className="flex items-center gap-2">
            <button className="btn-secondary h-10 w-10 px-0" onClick={toggleTheme} aria-label="Toggle theme">
              {dark ? <Sun size={17} /> : <Moon size={17} />}
            </button>
            {user ? (
              <>
                <Link className="btn-secondary h-10 w-10 px-0" to="/messages" aria-label="Notifications"><Bell size={17} /></Link>
                <button
                  className="btn-secondary h-10 w-10 px-0"
                  onClick={async () => {
                    await logout();
                    navigate("/");
                  }}
                  aria-label="Logout"
                >
                  <LogOut size={17} />
                </button>
              </>
            ) : (
              <Link className="btn-primary" to="/login">Login</Link>
            )}
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-7">
        <Outlet />
      </main>
      <footer className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-8 text-sm text-slate-500">
        <span>Nexfluency connects credible creators with ambitious campaigns.</span>
        <span className="inline-flex items-center gap-2"><Users size={16} /> Brands, creators, and operators in one place</span>
      </footer>
    </div>
  );
}
