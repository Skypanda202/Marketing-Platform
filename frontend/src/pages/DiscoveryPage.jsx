import { BadgeCheck, Filter, MapPin, Send, SlidersHorizontal, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";

import { influencerService } from "../api/services";

export default function DiscoveryPage() {
  const [filters, setFilters] = useState({ niche: "", location: "", followers_min: "", engagement_min: "" });
  const [influencers, setInfluencers] = useState([]);

  const load = () => influencerService.list(filters).then(({ data }) => setInfluencers(data.results || data)).catch(() => {});
  useEffect(() => { load(); }, []);

  const update = (event) => setFilters((state) => ({ ...state, [event.target.name]: event.target.value }));

  return (
    <div className="space-y-6">
      <div className="surface p-6">
        <p className="eyebrow">Creator discovery</p>
        <div className="mt-2 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-4xl font-black">Find creators with evidence, not vibes.</h1>
            <p className="mt-3 max-w-2xl text-slate-500 dark:text-slate-400">Score creators by fit, reach, engagement, location, trust signals, and predicted collaboration value.</p>
          </div>
          <span className="inline-flex items-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-bold text-white dark:bg-white dark:text-ink">
            <Sparkles size={16} /> AI-ranked shortlist
          </span>
        </div>
      </div>
      <div className="panel grid gap-3 md:grid-cols-5">
        <input className="input" name="niche" placeholder="Niche" value={filters.niche} onChange={update} />
        <input className="input" name="location" placeholder="Location" value={filters.location} onChange={update} />
        <input className="input" name="followers_min" placeholder="Min followers" value={filters.followers_min} onChange={update} />
        <input className="input" name="engagement_min" placeholder="Min engagement" value={filters.engagement_min} onChange={update} />
        <button className="btn-primary" onClick={load}><SlidersHorizontal size={16} /> Apply</button>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {influencers.length === 0 && (
          <div className="panel md:col-span-3">
            <h2 className="text-xl font-black">No influencers found</h2>
            <p className="mt-2 text-sm text-slate-500">Real creator profiles will appear here after influencer accounts complete their profiles.</p>
          </div>
        )}
        {influencers.map((item) => (
          <article key={item.id} className="panel overflow-hidden">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 className="text-lg font-bold">{item.display_name}</h2>
                <p className="mt-1 inline-flex items-center gap-1 text-sm text-slate-500"><MapPin size={14} /> {item.niche} / {item.location}</p>
              </div>
              <span className="rounded-md bg-saffron/20 px-2 py-1 text-xs font-black text-ink dark:text-white">{item.recommendation_score || 76}</span>
            </div>
            <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
              <span className="rounded-md bg-black/[0.035] p-3 dark:bg-white/7">Followers<br /><b>{item.followers}</b></span>
              <span className="rounded-md bg-black/[0.035] p-3 dark:bg-white/7">Engagement<br /><b>{item.engagement_rate}%</b></span>
            </div>
            <div className="mt-5 flex items-center justify-between border-t border-black/10 pt-4 dark:border-white/10">
              <span className="inline-flex items-center gap-1 text-xs font-bold text-mint"><BadgeCheck size={14} /> Verified fit</span>
              <button className="btn-secondary"><Send size={16} /> Invite</button>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
