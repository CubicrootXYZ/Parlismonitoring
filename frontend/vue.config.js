module.exports = {
    devServer: {
        disableHostCheck: true
    },
    build: {
        index: path.resolve(__dirname, '/app/index.html'),
        assetsPublicPath: "/",
        assetsSubDirectory: "src/assets"
    }
    publicPath: ''
}