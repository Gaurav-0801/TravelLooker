import { useState } from "react";
import { Button } from "@/components/ui/enhanced-button";
import { 
  Plane, 
  User, 
  Menu, 
  X,
  MapPin,
  Calendar,
  Users
} from "lucide-react";
import { cn } from "@/lib/utils";

interface HeaderProps {
  currentUser?: { name: string; email: string } | null;
  onLoginClick: () => void;
  onRegisterClick: () => void;
  onLogout: () => void;
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const Header = ({ 
  currentUser, 
  onLoginClick, 
  onRegisterClick, 
  onLogout,
  activeTab,
  onTabChange 
}: HeaderProps) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigation = [
    { id: 'search', label: 'Search Travels', icon: MapPin },
    { id: 'bookings', label: 'My Bookings', icon: Calendar },
    { id: 'profile', label: 'Profile', icon: User },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/80 shadow-travel-sm">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <div className="p-2 rounded-lg bg-gradient-hero shadow-travel-md">
            <Plane className="h-6 w-6 text-white drop-shadow-sm" />
          </div>
          <h1 className="text-xl font-bold bg-gradient-hero bg-clip-text text-transparent">
            TravelBooker
          </h1>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-6">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={cn(
                  "flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-all",
                  activeTab === item.id
                    ? "bg-primary text-primary-foreground shadow-travel-md"
                    : "text-muted-foreground hover:text-foreground hover:bg-accent"
                )}
              >
                <Icon className="h-4 w-4" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* User Actions */}
        <div className="flex items-center space-x-3">
          {currentUser ? (
            <div className="hidden md:flex items-center space-x-3">
              <div className="text-sm">
                <p className="font-medium">{currentUser.name}</p>
              </div>
              <Button variant="outline" size="sm" onClick={onLogout}>
                Logout
              </Button>
            </div>
          ) : (
            <div className="hidden md:flex items-center space-x-2">
              <Button variant="outline" size="sm" onClick={onLoginClick}>
                Login
              </Button>
              <Button variant="travel" size="sm" onClick={onRegisterClick}>
                Sign Up
              </Button>
            </div>
          )}

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X /> : <Menu />}
          </Button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden border-t bg-card">
          <div className="container mx-auto px-4 py-4 space-y-3">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onTabChange(item.id);
                    setIsMobileMenuOpen(false);
                  }}
                  className={cn(
                    "flex items-center space-x-3 w-full px-3 py-2 rounded-md text-sm font-medium transition-all",
                    activeTab === item.id
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:text-foreground hover:bg-accent"
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </button>
              );
            })}
            
            <div className="pt-3 border-t space-y-2">
              {currentUser ? (
                <>
                  <p className="text-sm font-medium px-3">{currentUser.name}</p>
                  <Button variant="outline" size="sm" onClick={onLogout} className="w-full">
                    Logout
                  </Button>
                </>
              ) : (
                <>
                  <Button variant="outline" size="sm" onClick={onLoginClick} className="w-full">
                    Login
                  </Button>
                  <Button variant="travel" size="sm" onClick={onRegisterClick} className="w-full">
                    Sign Up
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;