module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  outputDir: '../jumpscale/packages/gettft/frontend',
  publicPath: process.env.NODE_ENV === 'production' ? '/gettft/shop/' : undefined
}
