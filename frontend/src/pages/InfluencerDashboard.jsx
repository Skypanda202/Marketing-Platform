import { Bell, CheckCircle, DollarSign, Upload, Users } from "lucide-react";
import { useEffect, useState } from "react";

import { invitationService } from "../api/services";
import DataTable from "../components/DataTable";
import MetricCard from "../components/MetricCard";
import { EarningsChart } from "../components/ChartPanel";

export default function InfluencerDashboard() {
  const [invitations, setInvitations] = useState([]);
  const chartData = [];

  useEffect(() => {
    invitationService.list().then(({ data }) => setInvitations(data.results || data)).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div className="surface p-6">
        <p className="eyebrow">Creator studio</p>
        <div className="mt-2 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-4xl font-black">Your partnerships, content, and earnings.</h1>
            <p className="mt-3 max-w-2xl text-slate-500 dark:text-slate-400">Manage profile signals, campaign invitations, content submissions, portfolio links, and payout progress.</p>
          </div>
          <button className="btn-primary"><Upload size={16} /> Upload portfolio</button>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-4">
        <MetricCard icon={Users} label="Followers" value="95K" />
        <MetricCard icon={CheckCircle} label="Engagement" value="5.8%" tone="mint" />
        <MetricCard icon={DollarSign} label="Earnings" value="INR 62K" tone="coral" />
        <MetricCard icon={Bell} label="Pending Invites" value={invitations.filter((item) => item.status === "PENDING").length} />
      </div>
      <div className="grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="panel space-y-4">
          <p className="eyebrow">Profile</p>
          <h2 className="text-lg font-black">Creator snapshot</h2>
          <input className="input" placeholder="Display name" defaultValue="Asha Creates" />
          <input className="input" placeholder="Instagram URL" defaultValue="https://instagram.com/asha" />
          <textarea className="input min-h-28" placeholder="Bio" defaultValue="Beauty creator with a skincare-first audience." />
          <button className="btn-primary">Save profile</button>
        </div>
        <EarningsChart data={chartData} />
      </div>
      <DataTable
        columns={[
          { key: "campaign_detail", label: "Campaign", render: (row) => row.campaign_detail?.title || "Campaign" },
          { key: "status", label: "Status" },
          { key: "proposed_rate", label: "Rate", render: (row) => `INR ${row.proposed_rate || 0}` },
          { key: "actions", label: "Actions", render: (row) => <div className="flex gap-2"><button className="btn-secondary" onClick={() => invitationService.accept(row.id)}>Accept</button><button className="btn-secondary" onClick={() => invitationService.reject(row.id)}>Reject</button></div> },
        ]}
        rows={invitations}
        empty="No invitations yet."
      />
    </div>
  );
}
