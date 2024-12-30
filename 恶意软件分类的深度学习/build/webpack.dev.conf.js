'use strict'
const utils = require('./utils')
const webpack = require('webpack')
const config = require('../config')
const merge = require('webpack-merge')
const path = require('path')
const baseWebpackConfig = require('./webpack.base.conf')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin')
const portfinder = require('portfinder')
// utils: 自定义工具函数模块。
// webpack: Webpack 核心库。
// config: 项目配置文件。
// merge: 用于合并多个配置对象的库。
// path: Node.js 内置路径处理模块。
// baseWebpackConfig: 基础 Webpack 配置。
// CopyWebpackPlugin: 用于复制静态文件的插件。
// HtmlWebpackPlugin: 用于生成 HTML 文件的插件。
// FriendlyErrorsPlugin: 用于友好的错误提示的插件。
// portfinder: 用于查找可用端口的库。

const HOST = process.env.HOST
// const HOST = process.env.HOST||'0.0.0.0'
const PORT = process.env.PORT && Number(process.env.PORT)
// HOST: 获取环境变量 HOST，如果未设置则默认为 '0.0.0.0'，表示监听所有网络接口。
// PORT: 获取环境变量 PORT，如果未设置则使用 config.dev.port。
const devWebpackConfig = merge(baseWebpackConfig, {
  module: {
    rules: utils.styleLoaders({ sourceMap: config.dev.cssSourceMap, usePostCSS: true })
  },
  // cheap-module-eval-source-map is faster for development
  devtool: config.dev.devtool,

  // these devServer options should be customized in /config/index.js
  devServer: {
    clientLogLevel: 'warning',
    historyApiFallback: {
      rewrites: [
        { from: /.*/, to: path.posix.join(config.dev.assetsPublicPath, 'index.html') },
      ],
    },
    hot: true,
    contentBase: false, // since we use CopyWebpackPlugin.
    compress: true,
    host: HOST || config.dev.host,
    port: PORT || config.dev.port,
    open: config.dev.autoOpenBrowser,
    overlay: config.dev.errorOverlay
      ? { warnings: false, errors: true }
      : false,
    publicPath: config.dev.assetsPublicPath,
    proxy: config.dev.proxyTable,
    quiet: true, // necessary for FriendlyErrorsPlugin
    watchOptions: {
      poll: config.dev.poll,
    },

  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': require('../config/dev.env')
    }),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NamedModulesPlugin(), // HMR shows correct file names in console on update.
    new webpack.NoEmitOnErrorsPlugin(),
    // https://github.com/ampedandwired/html-webpack-plugin
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: 'index.html',
      inject: true,
      favicon: path.resolve('./static/logo.ico')
    }),
    // copy custom static assets
    new CopyWebpackPlugin([
      {
        from: path.resolve(__dirname, '../static'),
        to: config.dev.assetsSubDirectory,
        ignore: ['.*']
      }
    ])
  ]
})
// module.rules: 使用 utils.styleLoaders 函数生成样式加载器规则。
// devtool: 设置开发工具，使用 cheap-module-eval-source-map 以加快开发速度。
// devServer: 配置开发服务器。
// clientLogLevel: 客户端日志级别。
// historyApiFallback: 用于单页应用的路由回退。
// hot: 开启热更新。
// contentBase: 不使用内容基础目录，因为使用了 CopyWebpackPlugin。
// compress: 开启压缩。
// host: 监听的主机地址，使用 HOST 或 config.dev.host。
// port: 监听的端口，使用 PORT 或 config.dev.port。
// open: 是否自动打开浏览器。
// overlay: 错误覆盖显示。
// publicPath: 资源公共路径。
// proxy: 代理表。
// quiet: 静默模式，配合 FriendlyErrorsPlugin 使用。
// watchOptions: 监视选项。
// plugins: 插件配置。
// DefinePlugin: 定义环境变量。
// HotModuleReplacementPlugin: 热模块替换插件。
// NamedModulesPlugin: 显示模块名称。
// NoEmitOnErrorsPlugin: 发生错误时不输出资源。
// HtmlWebpackPlugin: 生成 HTML 文件。
// CopyWebpackPlugin: 复制静态文件。
module.exports = new Promise((resolve, reject) => {
  portfinder.basePort = process.env.PORT || config.dev.port
  portfinder.getPort((err, port) => {
    if (err) {
      reject(err)
    } else {
      // publish the new Port, necessary for e2e tests
      process.env.PORT = port
      // add port to devServer config
      devWebpackConfig.devServer.port = port

      // Add FriendlyErrorsPlugin
      devWebpackConfig.plugins.push(new FriendlyErrorsPlugin({
        compilationSuccessInfo: {
          messages: [`Your application is running here: http://${devWebpackConfig.devServer.host}:${port}`],
        },
        onErrors: config.dev.notifyOnErrors
          ? utils.createNotifierCallback()
          : undefined
      }))

      resolve(devWebpackConfig)
    }
  })
})
// portfinder: 查找可用端口。
// basePort: 基础端口。
// getPort: 获取可用端口。
// resolve: 解析配置对象。
// reject: 拒绝配置对象。
// FriendlyErrorsPlugin: 添加友好的错误提示插件。
// compilationSuccessInfo: 编译成功信息。
// onErrors: 错误回调。
