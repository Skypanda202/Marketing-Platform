import { BadgeCheck, Facebook, Megaphone, Plus, Search } from "lucide-react";
import { useEffect, useState } from "react";

import { integrationService } from "../api/services";

export default function IntegrationsPage() {
  const [connections, setConnections] = useState([]);
  const [form, setForm] = useState({ provider: "META", account_id: "", account_name: "" });
  const [launch, setLaunch] = useState({ campaign: "", connection: "", daily_budget: "", destination_url: "", dry_run: true });

  const load = () => integrationService.connections().then(({ data }) => setConnections(data.results || data)).catch(() => setConnections([]));
  useEffect(() => { load(); }, []);

  const connectOAuth = async (provider) => {
    const { data } = provider === "META" ? await integrationService.metaAuthUrl() : await integrationService.googleAuthUrl();
    window.location.href = data.authorization_url;
  };

  const saveConnection = async (event) => {
    event.preventDefault();
    await integrationService.createConnection(form);
    setForm({ provider: "META", account_id: "", account_name: "" });
    load();
  };

  const createLaunch = async (event) => {
    event.preventDefault();
    await integrationService.createLaunch({ ...launch, dry_run: true, objective: "OUTCOME_TRAFFIC", audience: {}, creative: {} });
    setLaunch({ campaign: "", connection: "", daily_budget: "", destination_url: "", dry_run: true });
  };

  return (
    <div className="space-y-6">
      <div className="surface p-6">
        <p className="eyebrow">Paid media control room</p>
        <h1 className="mt-2 text-4xl font-black">Launch Meta and Google campaigns from the same workspace.</h1>
        <p className="mt-3 max-w-3xl text-slate-500 dark:text-slate-400">Connect Facebook, Instagram, and Google Ads accounts, prepare campaigns in dry-run mode, then submit paused campaigns after credentials and approvals are complete.</p>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="panel space-y-4">
          <h2 className="text-xl font-black">OAuth connections</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            <button className="btn-primary" onClick={() => connectOAuth("META")}><Facebook size={17} /> Facebook / Instagram</button>
            <button className="btn-secondary" onClick={() => connectOAuth("GOOGLE")}><Search size={17} /> Google Ads</button>
          </div>
          <form className="grid gap-3" onSubmit={saveConnection}>
            <select className="input" value={form.provider} onChange={(event) => setForm((state) => ({ ...state, provider: event.target.value }))}>
              <option value="META">Meta / Facebook / Instagram</option>
              <option value="GOOGLE">Google Ads</option>
            </select>
            <input className="input" placeholder="Ad account ID, e.g. act_123 or Google customer ID" value={form.account_id} onChange={(event) => setForm((state) => ({ ...state, account_id: event.target.value }))} required />
            <input className="input" placeholder="Account name" value={form.account_name} onChange={(event) => setForm((state) => ({ ...state, account_name: event.target.value }))} />
            <button className="btn-secondary" type="submit"><Plus size={16} /> Save manual connection</button>
          </form>
        </div>
        <form className="panel space-y-4" onSubmit={createLaunch}>
          <h2 className="text-xl font-black">Prepare ad launch</h2>
          <select className="input" value={launch.connection} onChange={(event) => setLaunch((state) => ({ ...state, connection: event.target.value }))} required>
            <option value="">Select ad account</option>
            {connections.map((connection) => <option key={connection.id} value={connection.id}>{connection.provider} / {connection.account_name || connection.account_id}</option>)}
          </select>
          <input className="input" placeholder="Campaign ID from backend" value={launch.campaign} onChange={(event) => setLaunch((state) => ({ ...state, campaign: event.target.value }))} required />
          <input className="input" placeholder="Daily budget" value={launch.daily_budget} onChange={(event) => setLaunch((state) => ({ ...state, daily_budget: event.target.value }))} required />
          <input className="input" placeholder="Destination URL" value={launch.destination_url} onChange={(event) => setLaunch((state) => ({ ...state, destination_url: event.target.value }))} required />
          <button className="btn-primary" type="submit"><Megaphone size={16} /> Validate launch</button>
        </form>
      </div>
      <div className="grid gap-3">
        {connections.map((connection) => (
          <div key={connection.id} className="panel flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="font-black">{connection.account_name || connection.account_id}</p>
              <p className="text-sm text-slate-500">{connection.provider} / {connection.account_id}</p>
            </div>
            <span className="inline-flex items-center gap-2 rounded-md bg-mint/10 px-3 py-2 text-sm font-bold text-mint"><BadgeCheck size={16} /> Connected</span>
          </div>
        ))}
      </div>
    </div>
  );
}
