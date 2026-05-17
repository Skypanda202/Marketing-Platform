import { ArrowUpRight, DollarSign, Megaphone, Plus, TrendingUp, Users } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { analyticsService, campaignService } from "../api/services";
import DataTable from "../components/DataTable";
import MetricCard from "../components/MetricCard";
import { PerformanceChart } from "../components/ChartPanel";

export default function BrandDashboard() {
  const [campaigns, setCampaigns] = useState([]);
  const [overview, setOverview] = useState({});
  const chartData = [];

  useEffect(() => {
    campaignService.list().then(({ data }) => setCampaigns(data.results || data)).catch(() => {});
    analyticsService.overview().then(({ data }) => setOverview(data)).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div className="surface overflow-hidden p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="eyebrow">Brand command center</p>
            <h1 className="mt-2 text-4xl font-black">Campaigns that move with the market.</h1>
            <p className="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">Plan launches, discover the right creators, watch content flow, and keep spend tied to outcomes.</p>
          </div>
          <div className="flex gap-2">
            <Link className="btn-secondary" to="/campaigns/1"><ArrowUpRight size={16} /> View live room</Link>
            <Link className="btn-primary" to="/discovery"><Plus size={16} /> Find creators</Link>
          </div>
        </div>
      </div>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-black">Today&apos;s snapshot</h2>
          <p className="mt-1 text-slate-500 dark:text-slate-400">Performance, creator pipeline, and campaign spend.</p>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-4">
        <MetricCard icon={Megaphone} label="Campaigns" value={campaigns.length} />
        <MetricCard icon={Users} label="Invites" value={campaigns.reduce((sum, item) => sum + (item.invitation_count || 0), 0)} tone="mint" />
        <MetricCard icon={TrendingUp} label="ROI" value={`${overview.roi || 0}%`} tone="coral" />
        <MetricCard icon={DollarSign} label="Revenue" value={`INR ${overview.revenue || 0}`} tone="plum" />
      </div>
      <div className="grid gap-4 lg:grid-cols-[1.25fr_0.75fr]">
        <PerformanceChart data={chartData} />
        <div className="panel">
          <p className="eyebrow">Creator pipeline</p>
          <h2 className="mt-1 text-lg font-black">Priority actions</h2>
          <div className="mt-5 space-y-3">
            {["Review 3 submitted reels", "Approve 2 creator contracts", "Shortlist 8 beauty creators", "Release pending milestone payment"].map((item, index) => (
              <div key={item} className="flex items-center justify-between rounded-lg bg-black/[0.035] px-4 py-3 dark:bg-white/7">
                <span className="text-sm font-semibold">{item}</span>
                <span className="grid h-7 w-7 place-items-center rounded-full bg-white text-xs font-black text-brand shadow-sm dark:bg-white/10">{index + 1}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      <section className="space-y-3">
        <h2 className="text-xl font-black">Active campaigns</h2>
        <DataTable
          columns={[
            { key: "title", label: "Campaign", render: (row) => <Link className="font-semibold text-brand" to={`/campaigns/${row.id}`}>{row.title}</Link> },
            { key: "niche", label: "Niche" },
            { key: "budget", label: "Budget", render: (row) => `INR ${row.budget}` },
            { key: "status", label: "Status", render: (row) => <span className="rounded-md bg-mint/12 px-2 py-1 text-xs font-bold text-mint">{row.status}</span> },
            { key: "end_date", label: "Ends" },
          ]}
          rows={campaigns}
        />
      </section>
    </div>
  );
}
