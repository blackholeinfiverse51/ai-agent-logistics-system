import React from 'react';
import { Menu, Search, Bell, Moon, Sun, User } from 'lucide-react';
import { cn } from '@/utils/helpers';
import Button from '../common/ui/Button';
import Badge from '../common/ui/Badge';

export const Header = ({ onMenuClick, isDark, onThemeToggle }) => {
  const [notifications] = React.useState(3);

  return (
    <header className="h-16 bg-card shadow-sm backdrop-blur-sm border-b sticky top-0 z-30">
      <div className="h-full flex items-center justify-between px-4 sm:px-6">
        {/* Left section */}
        <div className="flex items-center gap-2 sm:gap-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={onMenuClick}
            className="lg:hidden hover:scale-110 transition-transform"
            aria-label="Open menu"
          >
            <Menu className="h-5 w-5" />
          </Button>
          
          <h2 className="text-lg sm:text-2xl font-heading font-bold tracking-tight truncate max-w-[150px] sm:max-w-none">
            <span className="hidden sm:inline">AI Agent Logistics System</span>
            <span className="sm:hidden">AI System</span>
          </h2>
        </div>

        {/* Right section */}
        <div className="flex items-center gap-1 sm:gap-3">
          {/* Search */}
          <div className="relative hidden md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
            <input
              type="text"
              placeholder="Search..."
              className="pl-10 pr-4 py-2 w-48 lg:w-64 rounded-lg border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring transition-all"
            />
          </div>

          {/* Mobile Search Button */}
          <Button 
            variant="ghost" 
            size="icon" 
            className="md:hidden hover:scale-110 transition-transform"
            aria-label="Search"
          >
            <Search className="h-5 w-5" />
          </Button>

          {/* Notifications */}
          <div className="relative">
            <Button 
              variant="ghost" 
              size="icon"
              className="hover:scale-110 transition-transform"
              aria-label="Notifications"
            >
              <Bell className="h-5 w-5" />
            </Button>
            {notifications > 0 && (
              <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-destructive text-[10px] font-bold text-destructive-foreground animate-pulse-slow">
                {notifications}
              </span>
            )}
          </div>

          {/* Theme Toggle */}
          <Button 
            variant="ghost" 
            size="icon"
            onClick={onThemeToggle}
            className="hover:scale-110 transition-transform"
            aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
          >
            {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </Button>

          {/* User Profile */}
          <div className="flex items-center gap-2 pl-2 sm:pl-3 border-l">
            <div className="w-8 h-8 rounded-full gradient-primary flex items-center justify-center shadow-glow-primary cursor-pointer hover:scale-110 transition-transform">
              <User className="h-4 w-4 text-primary-foreground" />
            </div>
            <div className="hidden lg:block">
              <p className="text-sm font-semibold">Admin User</p>
              <p className="text-xs text-muted-foreground">admin@system.com</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
