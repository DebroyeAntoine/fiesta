module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      keyframes: {
        confettiFall: {
          '0%': { transform: 'translateY(0) rotate(0deg)' },
          '100%': { transform: 'translateY(300px) rotate(360deg)' },
        },
      },
      animation: {
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

