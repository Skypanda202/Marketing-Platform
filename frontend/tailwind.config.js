export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#101114",
        cloud: "#f5f3ef",
        brand: "#315c52",
        mint: "#1f9d77",
        coral: "#c85f4a",
        saffron: "#d79b39",
        plum: "#4c3f66",
      },
      boxShadow: {
        soft: "0 18px 55px rgba(16, 17, 20, 0.12)",
        lift: "0 28px 80px rgba(16, 17, 20, 0.16)",
      },
    },
  },
  plugins: [],
};
