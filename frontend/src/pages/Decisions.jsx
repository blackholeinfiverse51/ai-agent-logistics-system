import React from 'react';
import { Brain } from 'lucide-react';

export const Decisions = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <Brain className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-heading font-bold tracking-tight">AI Decision Engine</h1>
      </div>
      <p className="text-muted-foreground">Decision engine features coming soon...</p>
    </div>
  );
};

export default Decisions;
