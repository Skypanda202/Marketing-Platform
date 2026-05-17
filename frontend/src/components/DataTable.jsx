export default function DataTable({ columns, rows, empty = "No records yet." }) {
  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[680px] text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase text-slate-500 dark:bg-slate-950 dark:text-slate-400">
            <tr>{columns.map((column) => <th key={column.key} className="px-4 py-3">{column.label}</th>)}</tr>
          </thead>
          <tbody>
            {rows.length === 0 && (
              <tr><td className="px-4 py-6 text-center text-slate-500" colSpan={columns.length}>{empty}</td></tr>
            )}
            {rows.map((row) => (
              <tr key={row.id} className="border-t border-slate-100 dark:border-slate-800">
                {columns.map((column) => <td key={column.key} className="px-4 py-3">{column.render ? column.render(row) : row[column.key]}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
