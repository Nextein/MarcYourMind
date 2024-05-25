import {
    Box,
    Typography,
    useTheme,
    IconButton,
} from "@mui/material";
import { useState, useEffect } from "react";

import { doc, collection, getDocs, setDoc, updateDoc, serverTimestamp } from 'firebase/firestore';
import { db } from '../firebase';

import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Flex, Text, useToast } from "@chakra-ui/react";

export default function CyclesDown() {
    const toast = useToast();
    const [data, setData] = useState(initialData);

    useEffect(() => {
        async function fetchCollection(collectionName) {
            const querySnapshot = await getDocs(collection(db, collectionName));
            const docs = [];
            querySnapshot.forEach((doc) => {
                docs.push({
                    id: doc.id,
                    ...doc.data(),
                });
            });
            setData(docs);
        }
        fetchCollection('cycles_down');
    }, []);

    
    
    function openLink(value) {
        const url = "https://swap.bingx.com/es-es/ETH-USDT";
        window.open(url, '_blank');
    }

    const columns = [
        {
            field: "ticker",
            headerName: "Ticker",
            flex: 1,
            renderCell: (params) => (
                <Typography
                    color="blue"
                    onClick={() => openLink(params.value)}
                    sx={{
                        cursor: "pointer",
                        color: "white",
                    }}
                >
                    {params.row.ticker}
                </Typography>
            ),
        },
        {
            field: "price",
            headerName: "Price",
            flex: 1,
            renderCell: (params) => (
                <Typography
                    // color="blue"
                >
                    {params.row.price}
                </Typography>
            ),
        },
    ];




    return (
        <Box
            m={2}
        >
            <Text
                fontSize={22}
                fontWeight="bold"
                mb={5}
            >
                Downtrending
            </Text>
            <Box
                height="400px"
                width="40%vw"
                
                sx={{
                    '& .MuiDataGrid-root': {
                        color: 'white',
                    },
                    '& .MuiDataGrid-cell': {
                        color: 'white',
                    },
                    '& .MuiDataGrid-columnHeaderTitle': {
                        color: 'black',
                    },
                    '& .MuiDataGrid-toolbarContainer': {
                        color: 'white',
                    },
                    "& .MuiDataGrid-footerContainer": {
                        color: 'white',
                    },
                }}
            >
                <DataGrid
                    checkboxSelection={false}
                    rows={data}
                    columns={columns}
                    density="compact"
                    components={{
                        Toolbar: GridToolbar,
                    }}
                    initialState={{
                        columns: {
                            columnVisibilityModel: {
                                // Hide the following columns by default
                                id: false,
                                phone: false,
                            },
                        },
                    }}
                />
            </Box>
        </Box>
    );
}

// Sample data
const initialData = [
    {
        id: 1,
        ticker: "AAPL",
        date: "2021-10-01",
        price: 145.0,
    },
    {
        id: 2,
        ticker: "GOOGL",
        date: "2021-10-01",
        price: 2800.0,
    },
    {
        id: 3,
        ticker: "AMZN",
        date: "2021-10-01",
        price: 3500.0,
    },
];