import React from 'react';
import { Package } from 'lucide-react';

export const Products = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <Package className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-heading font-bold tracking-tight">Product Catalog</h1>
      </div>
      <p className="text-muted-foreground">Product catalog features coming soon...</p>
    </div>
  );
};

export default Products;
