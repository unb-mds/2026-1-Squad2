const UFS = [
  'AC','AL','AM','AP','BA','CE','DF','ES','GO','MA',
  'MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN',
  'RO','RR','RS','SC','SE','SP','TO',
];

function SelectField({ label, value, onChange, children }) {
  return (
    <div>
      <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm bg-white focus:outline-none focus:border-[#5B4FCF] focus:ring-1 focus:ring-[#5B4FCF]"
      >
        {children}
      </select>
    </div>
  );
}

export default function FiltrosBar({ filtros, setFiltros, metaFiltros, onAplicar, onLimpar }) {
  const set = (campo, valor) =>
    setFiltros((prev) => ({ ...prev, [campo]: valor }));

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 mb-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-5">
        {/* Palavra-chave */}
        <div className="xl:col-span-2">
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
            Palavra-chave ou Número
          </label>
          <div className="relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">
              🔍
            </span>
            <input
              type="text"
              value={filtros.keyword}
              onChange={(e) => set('keyword', e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && onAplicar()}
              className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-[#5B4FCF] focus:ring-1 focus:ring-[#5B4FCF]"
            />
          </div>
        </div>

        {/* Partido */}
        <SelectField label="Partido" value={filtros.partido} onChange={(v) => set('partido', v)}>
          <option value="">Todos</option>
          {metaFiltros.partidos.map((p) => (
            <option key={p} value={p}>{p}</option>
          ))}
        </SelectField>

        {/* UF */}
        <SelectField label="UF" value={filtros.uf} onChange={(v) => set('uf', v)}>
          <option value="">Todos</option>
          {UFS.map((uf) => (
            <option key={uf} value={uf}>{uf}</option>
          ))}
        </SelectField>

        {/* Status */}
        <SelectField label="Status" value={filtros.status} onChange={(v) => set('status', v)}>
          <option value="">Todos</option>
          <option value="em_tramitacao">Em Tramitação</option>
          <option value="aprovado">Aprovado</option>
          <option value="arquivado">Arquivado</option>
        </SelectField>

        {/* Ano */}
        <SelectField label="Ano" value={filtros.ano} onChange={(v) => set('ano', v)}>
          <option value="">Todos</option>
          {metaFiltros.anos.map((a) => (
            <option key={a} value={a}>{a}</option>
          ))}
        </SelectField>
      </div>

      <div className="flex justify-end gap-3">
        <button
          onClick={onLimpar}
          className="px-5 py-2 text-sm font-semibold border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
        >
          LIMPAR
        </button>
        <button
          onClick={onAplicar}
          className="px-5 py-2 text-sm font-semibold bg-[#5B4FCF] text-white rounded-lg hover:bg-[#4338CA] transition-colors flex items-center gap-2"
        >
          ☰ APLICAR FILTROS
        </button>
      </div>
    </div>
  );
}