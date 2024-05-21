import { useState } from 'react';
import Cycles from './components/Cycles';
import './App.css';

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <Cycles />
  );
}


