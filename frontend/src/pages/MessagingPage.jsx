import { Send } from "lucide-react";
import { useEffect, useState } from "react";

import { communicationService } from "../api/services";

export default function MessagingPage() {
  const [messages, setMessages] = useState([]);
  const [body, setBody] = useState("");

  useEffect(() => {
    communicationService.messages().then(({ data }) => setMessages(data.results || data)).catch(() => {});
  }, []);

  return (
    <div className="grid gap-4 lg:grid-cols-[320px_1fr]">
      <aside className="panel">
        <p className="eyebrow">Inbox</p>
        <h1 className="mt-1 text-xl font-black">Campaign conversations</h1>
        <div className="mt-4 space-y-2">
          {["Nova Cosmetics", "Asha Creates", "Campaign Ops"].map((name) => (
            <button key={name} className="w-full rounded-md px-3 py-3 text-left text-sm font-semibold hover:bg-black/[0.035] dark:hover:bg-white/7">{name}</button>
          ))}
        </div>
      </aside>
      <section className="panel flex min-h-[560px] flex-col">
        <div className="flex-1 space-y-3 overflow-y-auto">
          {(messages.length ? messages : [{ id: 1, body: "Can you share content drafts by Friday?", sender_detail: { email: "brand@example.com" } }]).map((message) => (
            <div key={message.id} className="max-w-xl rounded-lg bg-black/[0.035] p-3 text-sm dark:bg-white/7">
              <p className="font-semibold">{message.sender_detail?.email || "Team"}</p>
              <p className="mt-1 text-slate-600 dark:text-slate-300">{message.body}</p>
            </div>
          ))}
        </div>
        <form className="mt-4 flex gap-2" onSubmit={(event) => event.preventDefault()}>
          <input className="input" value={body} onChange={(event) => setBody(event.target.value)} placeholder="Write a message" />
          <button className="btn-primary" type="submit"><Send size={16} /></button>
        </form>
      </section>
    </div>
  );
}
