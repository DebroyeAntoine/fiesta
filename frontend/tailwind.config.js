module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      keyframes: {
        confettiFall: {
          '0%': { transform: 'translateY(0) rotate(0deg)' },
          '100%': { transform: 'translateY(300px) rotate(360deg)' },
        },
        shine: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        spin: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      },
        animation: {
        shine: 'shine 2s ease-in-out infinite',
        spin: 'spin 3s linear infinite',
        'confetti-fall': 'confettiFall 4s infinite',
      },
      colors: {
        primary: '#ff6f61', // exemple couleur vive
        secondary: '#36d7b7',
      },
    },
  },
  plugins: [],
};

