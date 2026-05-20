import { Link, useLocation } from 'react-router-dom';

const LINKS = [
  { label: 'INÍCIO', to: '/' },
  { label: 'GRÁFICOS', to: '/graficos' },
  { label: 'PROJETOS DE LEI', to: '/projetos' },
];

export default function NavBar() {
  const { pathname } = useLocation();

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold text-[#5B4FCF] tracking-widest">
          L.I.L.A.S.
        </Link>
        <div className="flex items-center gap-8">
          {LINKS.map((link) => {
            const ativo =
              pathname === link.to ||
              (link.to !== '/' && pathname.startsWith(link.to));
            return (
              <Link
                key={link.to}
                to={link.to}
                className={`text-sm font-semibold tracking-wide transition-colors pb-0.5 ${
                  ativo
                    ? 'text-[#5B4FCF] border-b-2 border-[#5B4FCF]'
                    : 'text-gray-600 hover:text-[#5B4FCF]'
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}