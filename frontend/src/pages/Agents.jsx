import React from 'react';
import { Bot } from 'lucide-react';

export const Agents = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <Bot className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-heading font-bold tracking-tight">AI Agents Control</h1>
      </div>
      <p className="text-muted-foreground">AI agents features coming soon...</p>
    </div>
  );
};

export default Agents;
