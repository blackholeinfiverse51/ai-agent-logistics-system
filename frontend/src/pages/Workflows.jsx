import React from 'react';
import { Workflow } from 'lucide-react';

export const Workflows = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <Workflow className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-heading font-bold tracking-tight">Automated Workflows</h1>
      </div>
      <p className="text-muted-foreground">Workflow automation features coming soon...</p>
    </div>
  );
};

export default Workflows;
