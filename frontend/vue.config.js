module.exports = {
    devServer: {
        disableHostCheck: true
    },
    build: {
        index: path.resolve(__dirname, '/app/index.html')
        assetssPublicPath: "/",
        assetsSubDirectory: "src/assets"
    }
    publicPath: ''
}