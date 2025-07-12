import React from "react";
import ReactDOM from "react-dom/client";
import AppWithProvider from "./App";
import { ThemeProvider, CssBaseline, createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#1976d2" },
    background: { default: "#181c24", paper: "#232936" },
  },
});

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppWithProvider />
    </ThemeProvider>
  </React.StrictMode>
);
