import { CalendarDays, DollarSign, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { campaignService } from "../api/services";
import MetricCard from "../components/MetricCard";

export default function CampaignDetails() {
  const { id } = useParams();
  const [campaign, setCampaign] = useState(null);

  useEffect(() => {
    campaignService.detail(id).then(({ data }) => setCampaign(data)).catch(() => {});
  }, [id]);

  return (
    <div className="space-y-6">
      <div className="panel">
        <p className="text-sm font-semibold uppercase text-brand">{campaign?.status || "Loading"}</p>
        <h1 className="mt-2 text-3xl font-black">{campaign?.title || "Campaign"}</h1>
        <p className="mt-3 max-w-3xl text-slate-500 dark:text-slate-400">{campaign?.description || "Campaign details will load from the API."}</p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard icon={DollarSign} label="Budget" value={`INR ${campaign?.budget || 0}`} />
        <MetricCard icon={CalendarDays} label="Timeline" value={campaign?.end_date || "Pending"} tone="mint" />
        <MetricCard icon={Sparkles} label="Predicted ROI" value={`${campaign?.expected_roi || 0}%`} tone="coral" />
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="panel">
          <h2 className="text-lg font-semibold">Deliverables</h2>
          <ul className="mt-4 space-y-2 text-sm text-slate-600 dark:text-slate-300">
            <li>Instagram reel and story set</li>
            <li>Creator review with product placement</li>
            <li>Performance report within 72 hours</li>
          </ul>
        </div>
        <div className="panel">
          <h2 className="text-lg font-semibold">Collaboration Status</h2>
          <p className="mt-4 text-sm text-slate-600 dark:text-slate-300">Accepted creators can submit campaign content, brands can review progress, and admins can monitor activity.</p>
        </div>
      </div>
    </div>
  );
}
