var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var node_env = process.env.NODE_ENV;


if (node_env == 'development') {
  var apiUrl = JSON.stringify("http://localhost:5000");
} else {
  var apiUrl = JSON.stringify("http://www.liftorum.com");
}

module.exports = {
  devtool: 'eval',
  entry: ['./src/index'],
  output: {
    path: path.join(__dirname, 'liftorum/static/'),
    filename: 'bundle.js',
    publicPath: '/'
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.DefinePlugin({
      __APIURL__: apiUrl
    }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    }),
    new ExtractTextPlugin("styles.css")
  ],
  module: {
    loaders: [{
      test: /\.jsx?$/,
      loaders: ['react-hot', 'babel'],
      include: path.join(__dirname, 'src')
    },{
      test: /\.css?$/,
      loader: ExtractTextPlugin.extract("style-loader", "css-loader"), 
    },{
      test: /\.woff($|\?)|\.woff2($|\?)|\.ttf($|\?)|\.eot($|\?)|\.svg($|\?)/,
      loader: 'url-loader'
    }]
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  }
};

