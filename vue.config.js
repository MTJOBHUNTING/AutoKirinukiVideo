const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  configureWebpack: {
    optimization: {
      splitChunks: false
    }
  },
  transpileDependencies: true,
  outputDir: 'gui',
  assetsDir: './',
  publicPath: './'
})
