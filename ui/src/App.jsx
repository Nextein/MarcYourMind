import { useState } from 'react';
import CyclesUp from './components/CyclesUp';
import './App.css';

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <CyclesUp />
  );
}


