import React from 'react';
import { GraduationCap } from 'lucide-react';

export const Learning = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <GraduationCap className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-heading font-bold tracking-tight">RL Learning System</h1>
      </div>
      <p className="text-muted-foreground">Learning system features coming soon...</p>
    </div>
  );
};

export default Learning;
