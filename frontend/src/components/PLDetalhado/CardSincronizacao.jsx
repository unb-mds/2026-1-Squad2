export default function CardSincronizacao() {
  return (
    <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 flex gap-3">
      <span className="text-gray-400 text-lg flex-shrink-0">ℹ</span>
      <p className="text-xs text-gray-500 leading-relaxed">
        As informações desta página são sincronizadas diariamente com as bases
        de dados oficiais do Senado Federal e da Câmara dos Deputados. Última
        atualização: Hoje, 08:30.
      </p>
    </div>
  );
}