import { motion } from "framer-motion";

export default function MetricCard({ icon: Icon, label, value, tone = "brand" }) {
  const color = tone === "mint" ? "bg-mint" : tone === "coral" ? "bg-coral" : tone === "plum" ? "bg-plum" : "bg-brand";
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} whileHover={{ y: -3 }} className="panel overflow-hidden">
      <div className="relative flex items-center justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-slate-500 dark:text-slate-400">{label}</p>
          <p className="mt-2 text-3xl font-black">{value}</p>
          <span className="mt-4 block h-1 w-16 rounded-full bg-black/10 dark:bg-white/15">
            <span className={`block h-full w-2/3 rounded-full ${color}`} />
          </span>
        </div>
        {Icon && <span className={`grid h-12 w-12 place-items-center rounded-lg ${color} text-white shadow-soft`}><Icon size={20} /></span>}
      </div>
    </motion.div>
  );
}
