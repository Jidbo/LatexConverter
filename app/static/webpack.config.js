const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require('path');

module.exports = {
	entry: {
		'main': './src/app.js',
		'pdf.worker': 'pdfjs-dist/build/pdf.worker.entry'
	},
	output: {
		filename: '[name].bundle.js',
		path: path.resolve(__dirname, 'dist'),
		publicPath: "./dist"
	},
	module: {
		rules: [
			{
			test: /\.css$/,
			use: [
				{loader: MiniCssExtractPlugin.loader },
				{loader: 'css-loader' },
				{
					loader: 'postcss-loader',
					options: {
						indent: 'postcss',
						plugins: [
							require('tailwindcss'),
							require('autoprefixer')
						]
					},
				},
				]
			},
			{
			  test: /\.(ttf|eot|svg|png|jpg|gif|ico)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
			  loader: 'file-loader'
			},
			{
				test: /\.(woff|woff2|eot|ttf|otf)$/,
				use: [
					'file-loader'
				]
			}
		]
	},
	plugins: [
		new MiniCssExtractPlugin({
			filename: "[name].css",
			chunkFilename: "[id].css"
		}),
		new webpack.ProvidePlugin({
			$: "jquery",
			jQuery: "jquery"
		}),
	]
};
