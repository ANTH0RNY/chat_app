//Routes.js
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Home";
import NotFound from "./Notfound";
import Login from './Login';

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="*" element={<NotFound />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
};

export default Router;