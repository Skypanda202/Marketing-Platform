import { ArrowRight, BarChart3, CheckCircle2, MessageSquare, Radar, ShieldCheck, Sparkles, Users } from "lucide-react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function HomePage() {
  return (
    <div className="space-y-8">
      <section className="grid min-h-[72vh] items-center gap-8 py-8 lg:grid-cols-[0.92fr_1.08fr]">
        <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          <p className="eyebrow inline-flex items-center gap-2">
            <Sparkles size={15} /> Creator partnerships, cleaned up
          </p>
          <h1 className="max-w-4xl text-5xl font-black leading-[0.98] tracking-normal md:text-7xl">
            Run influencer campaigns without the spreadsheet chaos.
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-slate-600 dark:text-slate-300">
            Nexfluency brings discovery, outreach, content approvals, messaging, payments, verification, and campaign analytics into one sharp operating system.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link className="btn-primary" to="/register">Create workspace <ArrowRight size={17} /></Link>
            <Link className="btn-secondary" to="/login">Open demo login</Link>
          </div>
          <div className="grid max-w-xl grid-cols-3 gap-3 pt-3 text-sm">
            {[["12.4M", "tracked reach"], ["38%", "avg ROI lift"], ["4.8/5", "creator rating"]].map(([value, label]) => (
              <div key={label} className="surface px-4 py-3">
                <p className="text-xl font-black">{value}</p>
                <p className="text-xs font-semibold uppercase tracking-[0.12em] text-slate-500">{label}</p>
              </div>
            ))}
          </div>
        </motion.div>
        <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} className="relative">
          <div className="surface overflow-hidden p-4 shadow-lift">
            <div className="rounded-lg bg-ink p-5 text-white dark:bg-white dark:text-ink">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.18em] text-saffron">Live campaign room</p>
                  <h2 className="mt-2 text-2xl font-black">Glow Launch 2026</h2>
                </div>
                <span className="rounded-md bg-mint px-3 py-1 text-xs font-bold text-white">Active</span>
              </div>
              <div className="mt-6 grid gap-3 sm:grid-cols-3">
                {[["82K", "impressions"], ["5.9%", "engagement"], ["41", "content pieces"]].map(([value, label]) => (
                  <div key={label} className="rounded-lg bg-white/10 p-4 dark:bg-black/8">
                    <p className="text-2xl font-black">{value}</p>
                    <p className="text-xs font-semibold uppercase tracking-[0.12em] opacity-70">{label}</p>
                  </div>
                ))}
              </div>
              <div className="mt-6 space-y-3">
                {[
                  ["Asha Creates", "Reel draft submitted", "91"],
                  ["Meera Eats", "Contract ready", "84"],
                  ["Ravi Reels", "Audience check passed", "78"],
                ].map(([name, status, score]) => (
                  <div key={name} className="flex items-center justify-between rounded-lg bg-white px-4 py-3 text-ink dark:bg-black/10 dark:text-ink">
                    <div className="flex items-center gap-3">
                      <span className="grid h-10 w-10 place-items-center rounded-full bg-cloud font-black text-brand">{name[0]}</span>
                      <div>
                        <p className="font-bold">{name}</p>
                        <p className="text-sm text-slate-500">{status}</p>
                      </div>
                    </div>
                    <span className="rounded-md bg-saffron/20 px-2 py-1 text-xs font-black text-ink">{score}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      </section>
      <section className="grid gap-4 md:grid-cols-4">
        {[
          ["Discovery", "Find creators by niche, location, engagement, audience fit, and trust score.", Radar],
          ["Workflow", "Invites, content submissions, campaign rooms, and reviews stay connected.", MessageSquare],
          ["Analytics", "Charts connect reach, clicks, conversions, spend, revenue, and ROI.", BarChart3],
          ["Governance", "Admins can verify influencers and remove fake or spam accounts.", ShieldCheck],
        ].map(([title, body, Icon]) => (
          <motion.div key={title} whileHover={{ y: -4 }} className="panel flex min-h-44 flex-col justify-between">
            <span className="grid h-11 w-11 place-items-center rounded-lg bg-ink text-white dark:bg-white dark:text-ink"><Icon size={20} /></span>
            <div>
              <h2 className="font-black">{title}</h2>
              <p className="mt-2 text-sm leading-6 text-slate-500 dark:text-slate-400">{body}</p>
            </div>
          </motion.div>
        ))}
      </section>
      <section className="surface grid gap-4 p-5 md:grid-cols-3">
        {["Brand teams get creator discovery and ROI reporting.", "Creators manage invites, profiles, submissions, and earnings.", "Admins monitor trust, users, reports, and campaign health."].map((item) => (
          <div key={item} className="flex items-start gap-3">
            <CheckCircle2 className="mt-0.5 text-mint" size={18} />
            <p className="text-sm font-semibold leading-6 text-slate-700 dark:text-slate-300">{item}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
