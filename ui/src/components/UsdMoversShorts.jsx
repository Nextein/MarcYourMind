import { Box, Typography } from "@mui/material";
import { useState, useEffect } from "react";
import { getDocs, collection } from 'firebase/firestore';
import { db } from '../firebase';
import { DataGrid, GridToolbar } from "@mui/x-data-grid";

export default function UsdMoversShorts() {
    const [data, setData] = useState([]);

    useEffect(() => {
        async function fetchCollection(collectionName) {
            const querySnapshot = await getDocs(collection(db, collectionName));
            const docs = [];
            querySnapshot.forEach((doc) => {
                const docData = doc.data();
                docData.top_longs.forEach((ticker, index) => {
                    docs.push({
                        id: `${doc.id}-${ticker}`,
                        ticker: ticker,
                        percentChange: docData.percent_changes_shorts[index]
                    });
                });
            });
            setData(docs);
        }
        fetchCollection('usd_movers'); // Update collection name
    }, []);

    const columns = [
        {
            field: "ticker",
            headerName: "Ticker",
            flex: 1,
        },
        {
            field: "percentChange",
            headerName: "Percent Change",
            flex: 1,
            cellClassName: 'percentChange-cell',
        },
    ];

    return (
        <Box m={2}>
            <Typography variant="h5">USD Movers Shorts</Typography>
            <Box height="400px" width="100%">
                <DataGrid
                    rows={data}
                    columns={columns}
                    components={{ Toolbar: GridToolbar }}
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
                        '& .percentChange-cell': {
                            color: 'red',
                        },
                    }}
                />
            </Box>
        </Box>
    );
}
