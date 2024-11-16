import { createTheme } from "@mui/material";

// Domyslne kolory w palecie (do nadpisania):
// https://mui.com/material-ui/customization/palette/ 

export const theme = createTheme({
  colorSchemes: {
    dark: {
      palette: {
        primary: {
          main: '#00FFFF',
        },
        background: {
          light: '#91a6be',
          default: '#003448',
          dark: '#FF0000',
        },
        text: {
          default: "#FFFFF7",
        }
      },
    },
    // light: {
    //   palette: {
    //     primary: {
    //       main: '#000000',
    //     },
    //     ...
    //   },
    // },
  },
});

