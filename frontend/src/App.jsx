import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Inicio from './pages/Inicio';
import ProjetosLei from './pages/ProjetosLei';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Inicio />} />
        <Route path="/projetos" element={<ProjetosLei />} />
      </Routes>
    </BrowserRouter>
  );
}