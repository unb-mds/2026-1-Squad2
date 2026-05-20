const LINKS_FOOTER = [
  'Senado Federal',
  'Câmara dos Deputados',
  'Sobre Nós',
  'Privacidade',
  'Contato',
];

export default function Footer() {
  return (
    <footer className="bg-[#1F2937] text-gray-400 mt-16">
      <div className="max-w-7xl mx-auto px-6 py-10">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <span className="text-xl font-bold text-white tracking-widest">
            L.I.L.A.S.
          </span>
          <div className="flex flex-wrap gap-6 text-sm">
            {LINKS_FOOTER.map((link) => (
              <a
                key={link}
                href="#"
                className="hover:text-white transition-colors"
              >
                {link}
              </a>
            ))}
          </div>
          <p className="text-xs text-gray-500 md:text-right leading-relaxed">
            © 2026 L.I.L.A.S. - Monitoramento Legislativo.
            <br />
            Todos os direitos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}