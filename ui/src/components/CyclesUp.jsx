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

export default function CyclesUp() {
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
        fetchCollection('cycles_up');
    }, []);



    function handleCellClick(value) {
        console.log("Copied to clipboard: ", value);

        // Copy to clipboard
        navigator.clipboard.writeText(value);

        // Show toast
        toast({
            title: "Copied to clipboard",
            description: value,
            status: "success",
            duration: 1500,
            position: 'top',
        });
    }

    const columns = [
        {
            field: "ticker",
            headerName: "Ticker",
            flex: 1,
            renderCell: (params) => (
                <Typography
                    color="blue"
                    onClick={() => handleCellClick(params.value)}
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
                Uptrending
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