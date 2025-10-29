import React, { useState, useEffect } from 'react';
import { Users, TrendingUp, DollarSign, Target, Plus, Search, Filter } from 'lucide-react';
import Card, { CardHeader, CardTitle, CardContent } from '../components/common/ui/Card';
import MetricCard from '../components/common/charts/MetricCard';
import Button from '../components/common/ui/Button';
import Input from '../components/common/forms/Input';
import Badge from '../components/common/ui/Badge';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../components/common/ui/Table';
import { LoadingSpinner } from '../components/common/ui/Spinner';
import { formatDate, formatRelativeTime } from '@/utils/dateUtils';

export const CRM = () => {
  const [loading, setLoading] = useState(true);
  const [accounts, setAccounts] = useState([]);

  const metrics = {
    totalAccounts: 532,
    activeLeads: 148,
    opportunities: 67,
    conversionRate: 24.8,
  };

  const mockAccounts = [
    { id: 'ACC-001', name: 'Acme Corporation', industry: 'Technology', value: 125000, stage: 'negotiation', contact: 'John Doe', lastActivity: new Date(Date.now() - 86400000) },
    { id: 'ACC-002', name: 'Global Solutions', industry: 'Manufacturing', value: 89000, stage: 'proposal', contact: 'Jane Smith', lastActivity: new Date(Date.now() - 172800000) },
    { id: 'ACC-003', name: 'Tech Innovators', industry: 'Software', value: 210000, stage: 'closed_won', contact: 'Bob Johnson', lastActivity: new Date(Date.now() - 259200000) },
    { id: 'ACC-004', name: 'Enterprise LLC', industry: 'Retail', value: 45000, stage: 'qualification', contact: 'Alice Williams', lastActivity: new Date(Date.now() - 345600000) },
    { id: 'ACC-005', name: 'StartUp Ventures', industry: 'Technology', value: 67000, stage: 'discovery', contact: 'Charlie Brown', lastActivity: new Date(Date.now() - 432000000) },
  ];

  useEffect(() => {
    setTimeout(() => {
      setAccounts(mockAccounts);
      setLoading(false);
    }, 800);
  }, []);

  const getStageVariant = (stage) => {
    const variants = {
      discovery: 'info',
      qualification: 'info',
      proposal: 'warning',
      negotiation: 'warning',
      closed_won: 'success',
      closed_lost: 'destructive',
    };
    return variants[stage] || 'default';
  };

  if (loading) {
    return <LoadingSpinner text="Loading CRM data..." />;
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-heading font-bold tracking-tight">CRM Management</h1>
          <p className="text-muted-foreground mt-1">
            Manage customers, leads, and opportunities
          </p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          New Account
        </Button>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Total Accounts"
          value={metrics.totalAccounts.toLocaleString()}
          trend="up"
          trendValue="+8.2%"
          icon={Users}
          variant="primary"
        />
        <MetricCard
          title="Active Leads"
          value={metrics.activeLeads.toLocaleString()}
          trend="up"
          trendValue="+12.5%"
          icon={TrendingUp}
          variant="secondary"
        />
        <MetricCard
          title="Opportunities"
          value={metrics.opportunities.toLocaleString()}
          icon={Target}
          variant="accent"
        />
        <MetricCard
          title="Conversion Rate"
          value={`${metrics.conversionRate}%`}
          trend="up"
          trendValue="+3.1%"
          icon={DollarSign}
          variant="success"
        />
      </div>

      {/* Accounts Table */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Accounts & Opportunities</CardTitle>
            <div className="flex items-center gap-3">
              <Input
                placeholder="Search accounts..."
                icon={Search}
                className="w-64"
              />
              <Button variant="outline">
                <Filter className="h-4 w-4 mr-2" />
                Filter
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Account ID</TableHead>
                <TableHead>Company Name</TableHead>
                <TableHead>Industry</TableHead>
                <TableHead>Contact</TableHead>
                <TableHead>Value</TableHead>
                <TableHead>Stage</TableHead>
                <TableHead>Last Activity</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {accounts.map((account) => (
                <TableRow key={account.id}>
                  <TableCell className="font-medium">{account.id}</TableCell>
                  <TableCell>{account.name}</TableCell>
                  <TableCell>{account.industry}</TableCell>
                  <TableCell>{account.contact}</TableCell>
                  <TableCell>${account.value.toLocaleString()}</TableCell>
                  <TableCell>
                    <Badge variant={getStageVariant(account.stage)}>
                      {account.stage.replace('_', ' ')}
                    </Badge>
                  </TableCell>
                  <TableCell>{formatRelativeTime(account.lastActivity)}</TableCell>
                  <TableCell>
                    <Button variant="ghost" size="sm">
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default CRM;
