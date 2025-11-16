import React from 'react';
import { Mail } from 'lucide-react';

export const Emails = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <Mail className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-heading font-bold tracking-tight">Email Automation</h1>
      </div>
      <p className="text-muted-foreground">Email automation features coming soon...</p>
    </div>
  );
};

export default Emails;
