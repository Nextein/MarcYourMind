import { Box, Typography } from "@mui/material";
import { useState, useEffect } from "react";
import { getDocs, collection } from 'firebase/firestore';
import { db } from '../firebase';
import { DataGrid, GridToolbar } from "@mui/x-data-grid";

export default function BtcMoversLongs() {
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
                        percentChange: docData.percent_changes_longs[index]
                    });
                });
            });
            setData(docs);
        }
        fetchCollection('btc_movers'); // Update collection name
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
            <Typography variant="h5">BTC Movers Longs</Typography>
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
                            color: 'green',
                        },
                    }}
                />
            </Box>
        </Box>
    );
}
