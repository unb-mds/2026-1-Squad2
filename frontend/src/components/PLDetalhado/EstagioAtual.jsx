const ESTAGIOS = [
  { key: 'apresentacao', label: 'Apresentação' },
  { key: 'comissao', label: 'Comissão' },
  { key: 'votacao', label: 'Votação' },
  { key: 'sancao', label: 'Sanção' },
];

export default function EstagioAtual({ estagioAtual }) {
  const indiceAtual = ESTAGIOS.findIndex((e) => e.key === estagioAtual);

  return (
    <div className="mt-6">
      <h3 className="text-base font-semibold text-gray-800 mb-4">Estágio Atual</h3>
      <div className="flex items-center">
        {ESTAGIOS.map((estagio, index) => {
          const concluido = index < indiceAtual;
          const atual = index === indiceAtual;
          const pendente = index > indiceAtual;

          return (
            <div key={estagio.key} className="flex items-center flex-1 last:flex-none">
              {/* Círculo */}
              <div className="flex flex-col items-center">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all ${
                    concluido
                      ? 'bg-[#5B4FCF] text-white'
                      : atual
                      ? 'bg-[#5B4FCF] text-white ring-4 ring-purple-100'
                      : 'bg-gray-200 text-gray-400'
                  }`}
                >
                  {concluido ? '✓' : atual ? '👤' : ''}
                </div>
                <span
                  className={`text-xs mt-2 font-medium text-center whitespace-nowrap ${
                    pendente ? 'text-gray-400' : 'text-[#5B4FCF]'
                  }`}
                >
                  {estagio.label}
                </span>
              </div>

              {/* Linha conectora */}
              {index < ESTAGIOS.length - 1 && (
                <div
                  className={`flex-1 h-0.5 mx-1 mb-5 ${
                    index < indiceAtual ? 'bg-[#5B4FCF]' : 'bg-gray-200'
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}