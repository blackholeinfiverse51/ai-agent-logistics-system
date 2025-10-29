import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/layout/Layout';
import { ROUTES } from './utils/constants';

// Pages
import Dashboard from './pages/Dashboard';
import Logistics from './pages/Logistics';
import CRM from './pages/CRM';
import Infiverse from './pages/Infiverse';
import Inventory from './pages/Inventory';
import Suppliers from './pages/Suppliers';
import Products from './pages/Products';
import Agents from './pages/Agents';
import Workflows from './pages/Workflows';
import Decisions from './pages/Decisions';
import Learning from './pages/Learning';
import Notifications from './pages/Notifications';
import Emails from './pages/Emails';
import Reports from './pages/Reports';
import Settings from './pages/Settings';
import Users from './pages/Users';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path={ROUTES.LOGISTICS} element={<Logistics />} />
          <Route path={ROUTES.CRM} element={<CRM />} />
          <Route path={ROUTES.INFIVERSE} element={<Infiverse />} />
          <Route path={ROUTES.INVENTORY} element={<Inventory />} />
          <Route path={ROUTES.SUPPLIERS} element={<Suppliers />} />
          <Route path={ROUTES.PRODUCTS} element={<Products />} />
          <Route path={ROUTES.AGENTS} element={<Agents />} />
          <Route path={ROUTES.WORKFLOWS} element={<Workflows />} />
          <Route path={ROUTES.DECISIONS} element={<Decisions />} />
          <Route path={ROUTES.LEARNING} element={<Learning />} />
          <Route path={ROUTES.NOTIFICATIONS} element={<Notifications />} />
          <Route path={ROUTES.EMAILS} element={<Emails />} />
          <Route path={ROUTES.REPORTS} element={<Reports />} />
          <Route path={ROUTES.SETTINGS} element={<Settings />} />
          <Route path={ROUTES.USERS} element={<Users />} />
        </Route>
      </Routes>
      <Toaster position="top-right" />
    </Router>
  );
}

export default App;
