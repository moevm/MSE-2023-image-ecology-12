const path = require("path");

module.exports = {
  webpackConfig: {
    resolve: {
      extensions: [".js", ".vue", ".json"],
      alias: {
        "@": path.resolve("src"),
      },
    },
  },
  title: "Default Style Guide",
  exampleMode: "expand",
};
