export default function CardIntegraPDF({ urlPdf }) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 flex flex-col items-center text-center gap-4">
      {/* Ícone */}
      <div className="w-14 h-14 rounded-full bg-[#5B4FCF] flex items-center justify-center">
        <span className="text-2xl">📄</span>
      </div>

      <div>
        <h3 className="text-base font-bold text-gray-800">Íntegra do Projeto</h3>
        <p className="text-sm text-gray-500 mt-1 leading-relaxed">
          Acesse o documento original com a redação completa proposta.
        </p>
      </div>

      {urlPdf ? (
        <a
          href={urlPdf}
          target="_blank"
          rel="noopener noreferrer"
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-[#5B4FCF] hover:bg-[#4338CA] text-white text-sm font-semibold rounded-lg transition-colors"
        >
          ⬇ DOWNLOAD PDF
        </a>
      ) : (
        <button
          disabled
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-gray-200 text-gray-400 text-sm font-semibold rounded-lg cursor-not-allowed"
        >
          PDF não disponível
        </button>
      )}
    </div>
  );
}