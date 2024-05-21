import {
    Box,
    Typography,
    useTheme,
    IconButton,
} from "@mui/material";
import { CheckCircle as CheckCircleIcon } from '@mui/icons-material';

// import { doc, collection, getDocs, setDoc, updateDoc, serverTimestamp } from 'firebase/firestore';
// import { db } from '../../../../firebase';

import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Flex, Text, useToast } from "@chakra-ui/react";

export default function Cycles() {
    const toast = useToast();

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
            field: "id",
            headerName: "ID",
            width: 200,
        },
        {
            field: "name",
            headerName: "Name",
            flex: 1, // Material UI allows to customize our column. We can set the width of the column by using the flex property to size of 1.
        },
        {
            field: "quote",
            headerName: "Payment",
            width: 120,
            renderCell: (params) => (
                <Typography
                    color="green"
                >
                    {params.row.quote}
                </Typography>
            ),
        },
        {
            field: "email",
            headerName: "Email",
            flex: 1,
            // render cell with onclick function
            renderCell: (params) => (
                <Typography
                    onClick={() => handleCellClick(params.value)}
                    sx={{
                        cursor: "pointer",
                    }}
                >
                    {params.value}
                </Typography>
            ),
        },
        {
            field: "phone",
            headerName: "Phone",
            flex: 1,
        },
        {
            field: "pickupDate",
            headerName: "Pickup Date",
            width: 100,
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
                height="75vh"
                sx={{
                    "& .MuiDataGrid-root": {
                        border: "none",
                    },
                    "& .MuiDataGrid-cell": {
                        // borderBottom: "none",
                    },
                    "& .name-column--cell": {
                        color: "green",
                        fontWeight: "bold",
                    },
                    "& .MuiDataGrid-columnHeaders": {
                        backgroundColor: "blue",
                        borderBottom: "none",
                    },
                    "& .MuiDataGrid-virtualScroller": {
                        backgroundColor: "lightblue",
                    },
                    "& .MuiDataGrid-footerContainer": {
                        borderTop: "none",
                        backgroundColor: "lightblue",
                    },
                    '& .MuiDataGrid-toolbarContainer .MuiButton-text': {
                        color: `gray !important`,
                    },
                    "& .MuiCheckbox-root": {
                        color: `lightgreen !important`,
                    }
                }}
            >
                <DataGrid
                    checkboxSelection={false}
                    rows={newOrders}
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
const newOrders = [
    {
        id: 1,
        name: "John Doe",
        createdAt: new Date(),
        quote: 100,
        email: "mgtroja@fgmail.om",
        phone: "1234567890",
        origin: "New York",
        destination: "Los Angeles",
        pickupDate: "2022-12-31",
        createdAt: new Date(),
    },
    {
        id: 2,
        name: "Jane Doe",
        createdAt: new Date(),
        quote: 200,
        email: "test@exmpale.com",
        phone: "0987654321",
        origin: "Los Angeles",
        destination: "New York",
        pickupDate: "2022-12-31",
        createdAt: new Date(),
    },
    {
        id: 3,
        name: "John Smith",
        quote: 300,
        email: "Test@gmail.com",
        phone: "1234567890",
        pickupDate: "2022-12-31",
    },
];
