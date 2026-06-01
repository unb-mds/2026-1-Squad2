import { Link } from 'react-router-dom';

export default function Breadcrumb({ numero, ano }) {
  return (
    <nav className="flex items-center gap-2 text-sm mb-6">
      <Link to="/" className="text-[#5B4FCF] hover:underline">Início</Link>
      <span className="text-gray-400">›</span>
      <Link to="/projetos" className="text-[#5B4FCF] hover:underline">Pesquisa PL</Link>
      <span className="text-gray-400">›</span>
      <span className="text-gray-600 font-medium">PL {numero}/{ano}</span>
    </nav>
  );
}