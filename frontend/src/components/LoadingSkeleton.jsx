export default function LoadingSkeleton() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {[1, 2, 3].map((item) => (
        <div key={item} className="panel animate-pulse">
          <div className="h-4 w-24 rounded bg-slate-200 dark:bg-slate-800" />
          <div className="mt-4 h-8 w-32 rounded bg-slate-200 dark:bg-slate-800" />
          <div className="mt-6 h-24 rounded bg-slate-200 dark:bg-slate-800" />
        </div>
      ))}
    </div>
  );
}
