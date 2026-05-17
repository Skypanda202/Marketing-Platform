import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function PerformanceChart({ data }) {
  return (
    <div className="panel h-80">
      <div className="mb-3 flex items-center justify-between">
        <div>
          <p className="eyebrow">Performance</p>
          <h2 className="text-lg font-black">Campaign pulse</h2>
        </div>
        <span className="rounded-md bg-mint/12 px-3 py-1 text-xs font-bold text-mint">+18.4%</span>
      </div>
      <ResponsiveContainer width="100%" height="85%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#d7d5cc" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="impressions" stroke="#315c52" strokeWidth={3} dot={false} />
          <Line type="monotone" dataKey="conversions" stroke="#d79b39" strokeWidth={3} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function EarningsChart({ data }) {
  return (
    <div className="panel h-80">
      <p className="eyebrow">Revenue</p>
      <h2 className="text-lg font-black">Earnings trend</h2>
      <ResponsiveContainer width="100%" height="85%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#d7d5cc" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="earnings" fill="#c85f4a" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
