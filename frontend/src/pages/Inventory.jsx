import React from 'react';
import { ShoppingCart } from 'lucide-react';

export const Inventory = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <ShoppingCart className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-heading font-bold tracking-tight">Inventory Management</h1>
      </div>
      <p className="text-muted-foreground">Inventory management features coming soon...</p>
    </div>
  );
};

export default Inventory;
