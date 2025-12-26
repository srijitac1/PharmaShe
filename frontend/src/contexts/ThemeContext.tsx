import React, { createContext, useState, useMemo } from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';

export const ThemeContext = createContext({
  toggleTheme: () => {},
  mode: 'light',
});

export const CustomThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mode, setMode] = useState<'light' | 'dark'>('light');

  const theme = useMemo(() => {
    return createTheme({
      palette: {
        mode,
        ...(mode === 'light'
          ? {
              primary: {
                main: '#1976d2',
                light: '#42a5f5',
                dark: '#1565c0',
              },
              secondary: {
                main: '#dc004e',
                light: '#ff5983',
                dark: '#9a0036',
              },
              background: {
                default: '#f5f5f5',
                paper: '#ffffff',
              },
            }
          : {
              primary: {
                main: '#90caf9',
                light: '#e3f2fd',
                dark: '#42a5f5',
              },
              secondary: {
                main: '#f48fb1',
                light: '#f8bbd0',
                dark: '#c2185b',
              },
              background: {
                default: '#121212',
                paper: '#1e1e1e',
              },
            }),
      },
      typography: {
        fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
      },
      components: {
        MuiButton: {
          styleOverrides: {
            root: {
              textTransform: 'none',
              borderRadius: 8,
            },
          },
        },
        MuiCard: {
          styleOverrides: {
            root: {
              borderRadius: 12,
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            },
          },
        },
        MuiPaper: {
          styleOverrides: {
            root: {
              borderRadius: 12,
            },
          },
        },
      },
    });
  }, [mode]);

  const toggleTheme = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider value={{ toggleTheme, mode }}>
      <ThemeProvider theme={theme}>
        {children}
      </ThemeProvider>
    </ThemeContext.Provider>
  );
};
