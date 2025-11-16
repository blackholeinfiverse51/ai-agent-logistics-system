import React from 'react';
import { Bell } from 'lucide-react';

export const Notifications = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <Bell className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-heading font-bold tracking-tight">Alert Management</h1>
      </div>
      <p className="text-muted-foreground">Notification features coming soon...</p>
    </div>
  );
};

export default Notifications;
