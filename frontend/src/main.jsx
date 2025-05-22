import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/home'
import Notice from './pages/notice'
import Product from './pages/product' // ✅ 추가
import './index.css'


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/notice" element={<Notice />} />
        <Route path="/product" element={<Product />} /> {/* ✅ 추가 */}
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
