import React, { useEffect, useState } from 'react';
import { Package, Users, ShoppingCart, TrendingUp, Activity, AlertCircle } from 'lucide-react';
import MetricCard from '../components/common/charts/MetricCard';
import LineChart from '../components/common/charts/LineChart';
import BarChart from '../components/common/charts/BarChart';
import Card, { CardHeader, CardTitle, CardContent } from '../components/common/ui/Card';
import Badge from '../components/common/ui/Badge';
import { LoadingSpinner } from '../components/common/ui/Spinner';
import { formatRelativeTime } from '@/utils/dateUtils';

export const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState({
    totalOrders: 1248,
    activeCustomers: 532,
    inventoryItems: 3842,
    revenue: 128540,
  });

  const salesData = [
    { name: 'Jan', sales: 4000, orders: 240 },
    { name: 'Feb', sales: 3000, orders: 198 },
    { name: 'Mar', sales: 5000, orders: 320 },
    { name: 'Apr', sales: 4500, orders: 278 },
    { name: 'May', sales: 6000, orders: 389 },
    { name: 'Jun', sales: 5500, orders: 349 },
  ];

  const categoryData = [
    { name: 'Mon', logistics: 45, crm: 32, inventory: 28 },
    { name: 'Tue', logistics: 52, crm: 38, inventory: 35 },
    { name: 'Wed', logistics: 48, crm: 41, inventory: 30 },
    { name: 'Thu', logistics: 61, crm: 45, inventory: 38 },
    { name: 'Fri', logistics: 55, crm: 39, inventory: 33 },
  ];

  const recentActivity = [
    { id: 1, type: 'order', message: 'New order #1245 created', time: new Date(Date.now() - 300000), status: 'success' },
    { id: 2, type: 'inventory', message: 'Low stock alert for Product XYZ', time: new Date(Date.now() - 600000), status: 'warning' },
    { id: 3, type: 'delivery', message: 'Shipment #8821 delivered', time: new Date(Date.now() - 900000), status: 'success' },
    { id: 4, type: 'agent', message: 'AI Agent processed 15 orders', time: new Date(Date.now() - 1200000), status: 'info' },
    { id: 5, type: 'crm', message: 'New lead converted to customer', time: new Date(Date.now() - 1800000), status: 'success' },
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return <LoadingSpinner text="Loading dashboard..." />;
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-heading font-bold tracking-tight">Dashboard Overview</h1>
        <p className="text-muted-foreground mt-1">
          Welcome back! Here's what's happening with your business today.
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Total Orders"
          value={metrics.totalOrders.toLocaleString()}
          trend="up"
          trendValue="+12.5%"
          icon={Package}
          variant="primary"
        />
        <MetricCard
          title="Active Customers"
          value={metrics.activeCustomers.toLocaleString()}
          trend="up"
          trendValue="+8.2%"
          icon={Users}
          variant="secondary"
        />
        <MetricCard
          title="Inventory Items"
          value={metrics.inventoryItems.toLocaleString()}
          trend="down"
          trendValue="-3.1%"
          icon={ShoppingCart}
          variant="accent"
        />
        <MetricCard
          title="Revenue"
          value={`$${(metrics.revenue / 1000).toFixed(1)}K`}
          trend="up"
          trendValue="+15.3%"
          icon={TrendingUp}
          variant="success"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LineChart
          title="Sales & Orders Trend"
          data={salesData}
          lines={[
            { dataKey: 'sales', name: 'Sales ($)', color: 'hsl(var(--primary))' },
            { dataKey: 'orders', name: 'Orders', color: 'hsl(var(--secondary))' },
          ]}
          height={300}
        />
        
        <BarChart
          title="Activity by Category"
          data={categoryData}
          bars={[
            { dataKey: 'logistics', name: 'Logistics', color: 'hsl(var(--primary))' },
            { dataKey: 'crm', name: 'CRM', color: 'hsl(var(--secondary))' },
            { dataKey: 'inventory', name: 'Inventory', color: 'hsl(var(--accent))' },
          ]}
          height={300}
        />
      </div>

      {/* Recent Activity & System Health */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5" />
              Recent Activity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div 
                  key={activity.id}
                  className="flex items-start gap-4 p-3 rounded-lg hover:bg-muted/50 transition-colors"
                >
                  <div className={`w-2 h-2 rounded-full mt-2 bg-${activity.status}`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium">{activity.message}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {formatRelativeTime(activity.time)}
                    </p>
                  </div>
                  <Badge variant={activity.status}>{activity.type}</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* System Health */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="h-5 w-5" />
              System Health
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <HealthMetric label="API Status" value="Operational" status="success" />
            <HealthMetric label="Database" value="99.9% uptime" status="success" />
            <HealthMetric label="AI Agents" value="5 Active" status="success" />
            <HealthMetric label="Workflows" value="12 Running" status="info" />
            <HealthMetric label="Pending Tasks" value="3 Items" status="warning" />
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

const HealthMetric = ({ label, value, status }) => (
  <div className="flex items-center justify-between">
    <span className="text-sm text-muted-foreground">{label}</span>
    <Badge variant={status}>{value}</Badge>
  </div>
);

export default Dashboard;
