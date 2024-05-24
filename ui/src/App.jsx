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

import dotenv from 'dotenv';
// Load environment variables from .env
dotenv.config();

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: "cripto-tech.firebaseapp.com",
  projectId: "cripto-tech",
  storageBucket: "cripto-tech.appspot.com",
  messagingSenderId: "383277567591",
  appId: "1:383277567591:web:ba304c62e1564238e08ec2",
  measurementId: "G-JYXEHYJ8QH"
};
export const firebaseApp = initializeApp(firebaseConfig, 'technex');
const functions = getFunctions(firebaseApp);

export const getDataFunction = httpsCallable(functions, 'data');
export const getPrecisionFunction = httpsCallable(functions, 'precision');

export default function App() {

  const [data, setData] = useState([]);
  const [symbol, setSymbol] = useState('BTCUSDT');
  const [precision, setPrecision] = useState(2);
  const [Entry, setEntry] = useState(-1);
  const [SL, setSL] = useState(-1);
  const [TP, setTP] = useState(-1);

  async function fetchPrecision(symbol) {
    try {
      const response = getPrecisionFunction({ symbol });
      console.log(response.data);
      setPrecision(response.data);
    } catch (err) {
      console.log(err);
    }
  }
  async function fetchData(symbol, interval, chart_type = "OHLC") {
    console.log("Fetching ", symbol, interval, chart_type);

    try {

      const response = await getDataFunction({ symbol, interval, chart_type });
      // Set the retrieved data to state
      console.log(response.data);
      setData(response.data);
    } catch (err) {
      console.log(err);
    }
  }

  useEffect(() => {
    fetchData(symbol, '4h');
    fetchPrecision(symbol);
  }, []);

  useEffect(() => {
    fetchData(symbol, '4h');
    fetchPrecision(symbol);
  }, [symbol]);

  return (
    <>
      <Heading>2 Cycles</Heading>
      <Box w="70vw">
        <CandlestickChart
          data={data}
          symbol={symbol}
          interval='4h'
          precision={precision}
          Entry={Entry}
          SL={SL}
          TP={TP}
        />
      </Box>
      <Flex>
        <CyclesUp />
        <CyclesDown />
      </Flex>
    </>
  );
}


