export default function CardTemas({ temas }) {
  if (!temas || temas.length === 0) return null;

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5">
      <h3 className="text-sm font-semibold text-gray-800 mb-3">Temas Relacionados</h3>
      <div className="flex flex-wrap gap-2">
        {temas.map((tema) => (
          <span
            key={tema}
            className="px-3 py-1 text-xs font-medium text-gray-700 border border-gray-300 rounded-full"
          >
            {tema}
          </span>
        ))}
      </div>
    </div>
  );
}