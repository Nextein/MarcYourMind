
import { Box } from '@chakra-ui/react';
import { createChart, ColorType, CrosshairMode, LineStyle } from 'lightweight-charts';
import React, { useEffect, useRef, useState } from 'react';

export default function CandlestickChart(props) {
  const {
    data,
    symbol,
    interval,
    precision,
    Entry,
    SL,
    TP,
    colors: {
      backgroundColor = '#00000000',
      textColor = '#BBB',
    } = {},
    ...rest
  } = props;


  const [classname, setClassname] = useState("");
  const [signal, setSignal] = useState({});
  const [markers, setMarkers] = useState(initialMarkers);

  function defineClassName() {
    if (props.class_name) {
      setClassname(props.class_name);
    } else {
      setClassname("card chart");
    }

  }

  function defineMarkers() {
    if (props.signal) {
      setSignal(props.signal);
      updateMarkers();
    }
  }

  function updateMarkers() {
    var markers = [
      {
        time: signal['entry time'],
        position: 'belowBar',
        color: '#f68410',
        shape: 'arrowUp',
        text: 'Buy',
      },
      {
        time: signal['exit time'],
        position: 'aboveBar',
        color: '#f68410',
        shape: 'arrowDown',
        text: 'Sell',
      },
    ];
    setMarkers(markers);
  }


  useEffect(() => {
    defineClassName();
    // updateMarkers()
    defineMarkers();
  }, [props]);
  useEffect(() => {
    defineClassName();
    defineMarkers();
  }, []);



  const chartContainerRef = useRef();

  useEffect(
    () => {
      function handleResize() {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,

        });
        chart.timeScale().fitContent();

      };

      const chart = createChart(chartContainerRef.current, {
        layout: {
          background: { type: ColorType.Solid, color: backgroundColor },
          textColor,
        },
        width: chartContainerRef.current.clientWidth,
        height: 300,
        grid: {
          vertLines: {
            visible: false,
          },
          horzLines: {
            visible: false,
          },
        },
        crosshair: {
          // Change mode from default 'magnet' to 'normal'.
          // Allows the crosshair to move freely without snapping to datapoints
          mode: CrosshairMode.Normal,

          // Vertical crosshair line (showing Date in Label)
          vertLine: {
            width: 8,
            color: '#4444',
            style: LineStyle.Solid,
            labelBackgroundColor: '#444',
          },

          // Horizontal crosshair line (showing Price in Label)
          horzLine: {
            color: '#DDD',
            labelBackgroundColor: '#444',
          },
        },
      });
      // chart.timeScale().fitContent();

      chart.applyOptions({
        watermark: {
          visible: true,
          fontSize: 24,
          horzAlign: 'center',
          vertAlign: 'top',
          color: 'rgba(180, 180, 180, 0.5)',
          text: symbol + ' ' + interval,
        },
      });

      const candlestickSeries = chart.addCandlestickSeries({
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderVisible: true,
        wickUpColor: '#26a69a',
        wickDownColor: '#ef5350',
        priceFormat: {
          type: 'price',
          minMove: precision,
        },
      });

      candlestickSeries.setData(data);
      // candlestickSeries.setMarkers(markers);

      if (Entry > 0.0) {
        const entryLine = {
          price: parseFloat (Entry),
          // color: (Entry > SL)? 'green' : 'red',
          color: 'rgb(54, 116, 217)',
          lineWidth: 2,
          lineStyle: 1, // Dotted. 2 is for dashed
          axisLabelVisible: true,
          // title: (Entry > SL)? 'buy' : 'sell'
        };
        candlestickSeries.createPriceLine(entryLine);
      }

      if (SL > 0.0) {
        const SLLine = {
          price: parseFloat(SL),
          color: 'rgb(225, 50, 85)',
          lineWidth: 2,
          lineStyle: 1, // Dotted. 2 is for dashed
          axisLabelVisible: true,
          // title: 'SL'
        };
        candlestickSeries.createPriceLine(SLLine);
      }

      if (TP > 0.0) {
        const TPLine = {
          price: parseFloat(TP),
          color: 'rgb(40, 174, 40)',
          lineWidth: 2,
          lineStyle: 1, // Dotted. 2 is for dashed
          axisLabelVisible: true,
          // title: 'TP'
        };
        candlestickSeries.createPriceLine(TPLine);
      }



      window.addEventListener('resize', handleResize);
      return () => {
        window.removeEventListener('resize', handleResize);
        chart.remove();
      };
    },
    [data, backgroundColor, textColor, Entry, SL, TP]
    // [data, backgroundColor, textColor, props]
  );

  return (
    <Box w="100%" h="50vh">

      <div
        ref={chartContainerRef}
        />
        </Box>
  );
}


const initialSignal = {
  'SL': 7.381052494049072,
  'TP': -1.0,
  'Unnamed: 0': 0,
  'asset': 'GE',
  'entry': 6.9119181632995605,
  'entry balance': 100000.0,
  'entry time': '1981-11-02',
  'exit': 7.068295955657959,
  'exit time': '1981-11-09',
  'fees': 0.0,
  'pnl': 23.981260740088445,
  'side': 'buy',
  'size': 10000.0,
  'uid': 0
}

const initialMarkers = [
  {
    time: "2020-10-10",
    position: 'belowBar',
    color: '#f68410',
    shape: 'arrowUp',
    text: 'Buy',
  },
  {
    time: "2021-10-10",
    position: 'aboveBar',
    color: '#f68410',
    shape: 'arrowDown',
    text: 'Sell',
  },
];