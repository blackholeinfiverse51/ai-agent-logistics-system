import React, { useState } from 'react';
import { 
  LayoutDashboard, Package, Users, Building2, ShoppingCart, Bot,
  Workflow, Brain, GraduationCap, Bell, Mail, BarChart3, Settings,
  UsersRound, Menu, X, ChevronLeft, ChevronRight
} from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { cn } from '@/utils/helpers';
import { ROUTES } from '@/utils/constants';

const navigation = [
  { name: 'Dashboard', icon: LayoutDashboard, path: ROUTES.DASHBOARD },
  { 
    name: 'Core Business',
    items: [
      { name: 'Logistics', icon: Package, path: ROUTES.LOGISTICS },
      { name: 'CRM', icon: Users, path: ROUTES.CRM },
      { name: 'Infiverse', icon: UsersRound, path: ROUTES.INFIVERSE },
      { name: 'Inventory', icon: ShoppingCart, path: ROUTES.INVENTORY },
      { name: 'Suppliers', icon: Building2, path: ROUTES.SUPPLIERS },
      { name: 'Products', icon: Package, path: ROUTES.PRODUCTS },
    ]
  },
  {
    name: 'AI & Automation',
    items: [
      { name: 'AI Agents', icon: Bot, path: ROUTES.AGENTS },
      { name: 'Workflows', icon: Workflow, path: ROUTES.WORKFLOWS },
      { name: 'Decisions', icon: Brain, path: ROUTES.DECISIONS },
      { name: 'Learning', icon: GraduationCap, path: ROUTES.LEARNING },
    ]
  },
  {
    name: 'Communication',
    items: [
      { name: 'Notifications', icon: Bell, path: ROUTES.NOTIFICATIONS },
      { name: 'Emails', icon: Mail, path: ROUTES.EMAILS },
      { name: 'Reports', icon: BarChart3, path: ROUTES.REPORTS },
    ]
  },
  {
    name: 'System',
    items: [
      { name: 'Settings', icon: Settings, path: ROUTES.SETTINGS },
      { name: 'Users', icon: UsersRound, path: ROUTES.USERS },
    ]
  },
];

export const Sidebar = ({ isOpen, onToggle }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
          onClick={onToggle}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed left-0 top-0 z-50 h-screen bg-card shadow-xl backdrop-blur-sm transition-all duration-300',
          isCollapsed ? 'w-16' : 'w-64',
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
      >
        {/* Logo */}
        <div className="h-16 flex items-center justify-between px-4 border-b">
          {!isCollapsed && (
            <div className="gradient-primary rounded-lg px-3 py-2 shadow-glow-primary">
              <h1 className="text-lg font-heading font-bold text-primary-foreground">
                AI Agent
              </h1>
            </div>
          )}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="hidden lg:flex items-center justify-center w-8 h-8 rounded-md hover:bg-muted transition-colors"
          >
            {isCollapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </button>
          <button
            onClick={onToggle}
            className="lg:hidden flex items-center justify-center w-8 h-8 rounded-md hover:bg-muted transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-6">
          {navigation.map((section, idx) => (
            <div key={idx}>
              {section.items ? (
                // Section with items
                <div>
                  {!isCollapsed && (
                    <h3 className="px-3 mb-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                      {section.name}
                    </h3>
                  )}
                  <div className="space-y-1">
                    {section.items.map((item) => (
                      <NavItem key={item.path} item={item} isCollapsed={isCollapsed} />
                    ))}
                  </div>
                </div>
              ) : (
                // Single item
                <NavItem item={section} isCollapsed={isCollapsed} />
              )}
            </div>
          ))}
        </nav>
      </aside>
    </>
  );
};

const NavItem = ({ item, isCollapsed }) => {
  const Icon = item.icon;
  
  return (
    <NavLink
      to={item.path}
      className={({ isActive }) =>
        cn(
          'flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-300',
          isActive 
            ? 'gradient-primary text-primary-foreground shadow-lg' 
            : 'text-muted-foreground hover:bg-muted hover:text-foreground',
          isCollapsed && 'justify-center'
        )
      }
      title={isCollapsed ? item.name : undefined}
    >
      <Icon className="h-5 w-5 flex-shrink-0" />
      {!isCollapsed && <span className="font-medium">{item.name}</span>}
    </NavLink>
  );
};

export default Sidebar;
