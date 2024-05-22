import { useState } from 'react';
import CyclesUp from './components/CyclesUp';
import './App.css';
import CyclesDown from './components/CyclesDown';
import { Flex, Heading } from '@chakra-ui/react';

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <Heading>2 Cycles</Heading>
      <Flex>
        <CyclesUp />
        <CyclesDown />
      </Flex>
    </>
  );
}


