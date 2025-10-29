import React from 'react';
import { BarChart3 } from 'lucide-react';

export const Reports = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <BarChart3 className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-heading font-bold tracking-tight">Reports & Analytics</h1>
      </div>
      <p className="text-muted-foreground">Reports and analytics features coming soon...</p>
    </div>
  );
};

export default Reports;
