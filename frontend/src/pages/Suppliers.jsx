import React from 'react';
import { Building2 } from 'lucide-react';

export const Suppliers = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <Building2 className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-heading font-bold tracking-tight">Supplier Management</h1>
      </div>
      <p className="text-muted-foreground">Supplier management features coming soon...</p>
    </div>
  );
};

export default Suppliers;
