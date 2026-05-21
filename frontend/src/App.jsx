import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProjetosLei from './pages/ProjetosLei';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProjetosLei />} />
        <Route path="/projetos" element={<ProjetosLei />} />
      </Routes>
    </BrowserRouter>
  );
}
