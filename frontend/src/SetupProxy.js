// setupProxy.js

const { createProxyMiddleware } = require('http-proxy-middleware');
import Router from './components/Routes';

module.exports = function (Router) {
  Router.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:5000',  // Replace with your Flask backend URL
      changeOrigin: true,
    })
  );
};
