import { Route, Routes } from 'react-router-dom';
import Home from '../pages/home/Home';
import Login from '../pages/login/Login';
import Register from '../pages/register/Register';
import Orders from '../pages/orders/Orders';
import Profile from '../pages/profile/Profile';
import Admin from '../admin/Admin';

function AppRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/orders" element={<Orders />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/admin" element={<Admin />} />
        </Routes>
    );
}

export default AppRoutes;