import { useState, useEffect } from 'react';
import CyclesUp from './components/CyclesUp';
import './App.css';
import CyclesDown from './components/CyclesDown';
import {
  Flex,
  Box,
  Heading,
  useFocusEffect

} from '@chakra-ui/react';
import CandlestickChart from './components/CandlestickChart';
import { initializeApp } from "firebase/app";
import { getFunctions, httpsCallable } from 'firebase/functions';
import BtcMoversLongs from './components/BtcMoversLongs';
import BtcMoversShorts from './components/BtcMoversShorts';
import UsdMoversLongs from './components/UsdMoversLongs';
import UsdMoversShorts from './components/UsdMoversShorts';




export default function App() {

  const [data, setData] = useState([]);
  const [symbol, setSymbol] = useState('BTCUSDT');
  const [precision, setPrecision] = useState(2);
  const [Entry, setEntry] = useState(-1);
  const [SL, setSL] = useState(-1);
  const [TP, setTP] = useState(-1);


  return (
    <>
      <Heading>2 Cycles</Heading>
      <Flex justify="center" align="center">
        <CyclesUp />
        <CyclesDown />
      </Flex>
      <Heading>Top Movers</Heading>
      <Flex justify="center" align="center">
        <BtcMoversLongs />
        <UsdMoversLongs />
        <BtcMoversShorts />
        <UsdMoversShorts />
      </Flex>
    </>
  );
}


