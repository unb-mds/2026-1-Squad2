import { Link } from 'react-router-dom';
import NavBar from '../../components/NavBar';
import Footer from '../../components/Footer';

const STATS = [
  {
    label: 'Total de Projetos de Feminicídio',
    value: '452',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-[#5B4FCF]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    ),
  },
  {
    label: 'Em Tramitação',
    value: '128',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
    ),
  },
  {
    label: 'Aprovados',
    value: '45',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  {
    label: 'Arquivados',
    value: '279',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8l1 12a2 2 0 002 2h8a2 2 0 002-2L19 8m-9 4h4" />
      </svg>
    ),
  },
];

export default function Inicio() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <NavBar />

      {/* Hero */}
      <section className="bg-gradient-to-b from-[#f0eeff] to-gray-50 py-20 px-6 text-center">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-black text-gray-900 leading-tight mb-6 uppercase tracking-tight">
            Monitoramento Integral de Leis de Feminicídio
          </h1>
          <p className="text-gray-500 text-base md:text-lg leading-relaxed mb-10 max-w-xl mx-auto">
            Informação e transparência para o combate à violência contra a mulher.
            Monitoramento diário de Projetos de Lei na Câmara e no Senado.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/projetos"
              className="flex items-center gap-2 bg-[#5B4FCF] text-white font-semibold px-6 py-3 rounded-lg hover:bg-[#4338CA] transition-colors text-sm"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              VER PROJETOS DE LEI
            </Link>
            <Link
              to="/graficos"
              className="flex items-center gap-2 border-2 border-[#5B4FCF] text-[#5B4FCF] font-semibold px-6 py-3 rounded-lg hover:bg-[#f0eeff] transition-colors text-sm"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              VER GRÁFICOS
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="max-w-7xl mx-auto w-full px-6 -mt-6 mb-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {STATS.map((stat) => (
            <div
              key={stat.label}
              className="bg-white border border-gray-200 rounded-xl p-5 flex items-start justify-between shadow-sm hover:shadow-md transition-shadow"
            >
              <div>
                <p className="text-xs text-gray-500 leading-snug mb-2">{stat.label}</p>
                <p className="text-3xl font-black text-gray-900">{stat.value}</p>
              </div>
              <div className="mt-1">{stat.icon}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Sobre */}
      <section className="max-w-7xl mx-auto w-full px-6 mb-16">
        <div className="bg-white border border-gray-200 rounded-2xl p-10 text-center shadow-sm">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Sobre o L.I.L.A.S.</h2>
          <p className="text-gray-500 text-sm leading-relaxed max-w-2xl mx-auto">
            Uma plataforma independente dedicada ao monitoramento e análise de proposições
            legislativas relacionadas aos direitos da mulher e combate ao feminicídio.
            Transformamos dados complexos em informações claras para fortalecer a
            transparência e o engajamento cívico.
          </p>
        </div>
      </section>

      <Footer />
    </div>
  );
}