import { MousePointerClick, Receipt, TrendingUp, Users } from "lucide-react";
import { useEffect, useState } from "react";

import { analyticsService } from "../api/services";
import { PerformanceChart } from "../components/ChartPanel";
import MetricCard from "../components/MetricCard";

export default function AnalyticsPage() {
  const [overview, setOverview] = useState({});
  const chartData = [];

  useEffect(() => {
    analyticsService.overview().then(({ data }) => setOverview(data)).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div className="surface p-6">
        <p className="eyebrow">Analytics</p>
        <h1 className="mt-2 text-4xl font-black">Know what each collaboration returns.</h1>
        <p className="mt-3 max-w-2xl text-slate-500 dark:text-slate-400">Performance, conversion, revenue, sentiment, and ROI metrics in one executive view.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-4">
        <MetricCard icon={Users} label="Impressions" value={overview.impressions || 0} />
        <MetricCard icon={MousePointerClick} label="Clicks" value={overview.clicks || 0} tone="mint" />
        <MetricCard icon={Receipt} label="Conversions" value={overview.conversions || 0} tone="coral" />
        <MetricCard icon={TrendingUp} label="ROI" value={`${overview.roi || 0}%`} />
      </div>
      <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
        <PerformanceChart data={chartData} />
        <div className="panel">
          <p className="eyebrow">Insights</p>
          <h2 className="mt-1 text-lg font-black">What changed</h2>
          <div className="mt-5 space-y-4 text-sm">
            <p className="rounded-lg bg-mint/10 p-4 font-semibold text-mint">Beauty creators are converting 1.7x higher than the campaign average.</p>
            <p className="rounded-lg bg-saffron/15 p-4 font-semibold text-slate-700 dark:text-slate-200">Weekend posting windows delivered the strongest click-through rate.</p>
            <p className="rounded-lg bg-coral/10 p-4 font-semibold text-coral">Two creators need content revision before the next release window.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
