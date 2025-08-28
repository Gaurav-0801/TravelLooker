import { useState, useEffect } from "react";
import Header from "@/components/layout/Header";
import LoginForm from "@/components/auth/LoginForm";
import RegisterForm from "@/components/auth/RegisterForm";
import TravelSearchForm from "@/components/travel/TravelSearchForm";
import TravelCard, { TravelOption } from "@/components/travel/TravelCard";
import BookingModal from "@/components/travel/BookingModal";
import BookingCard, { Booking } from "@/components/booking/BookingCard";
import { Button } from "@/components/ui/enhanced-button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Globe, Calendar, MapPin, Star } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import heroImage from "@/assets/hero-travel.jpg";

// Base API URL
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "https://travellooker.onrender.com";

// Mock travel data
const mockTravels: TravelOption[] = [
  {
    id: "FL001",
    type: "flight",
    source: "new-york",
    destination: "los-angeles",
    date: "2024-09-15",
    time: "08:30",
    duration: "5h 30m",
    price: 299,
    availableSeats: 12,
    airline: "American Airlines"
  },
  {
    id: "TR002",
    type: "train",
    source: "chicago",
    destination: "denver",
    date: "2024-09-16",
    time: "14:15",
    duration: "18h 45m",
    price: 89,
    availableSeats: 24,
    operator: "Amtrak"
  },
];

interface User {
  name: string;
  email: string;
}

const Index = () => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [showRegisterForm, setShowRegisterForm] = useState(false);
  const [activeTab, setActiveTab] = useState("search");
  const [searchResults, setSearchResults] = useState<TravelOption[]>([]);
  const [selectedTravel, setSelectedTravel] = useState<TravelOption | null>(null);
  const [userBookings, setUserBookings] = useState<Booking[]>([]);
  const { toast } = useToast();

  useEffect(() => setSearchResults(mockTravels), []);

  /** LOGIN HANDLER */
  const handleLogin = (user: User) => {
    setCurrentUser(user);
    setShowLoginForm(false);
    setActiveTab("search");
    toast({
      title: "Welcome back!",
      description: "You have successfully logged in.",
    });
  };

  /** REGISTER HANDLER */
  const handleRegister = async (username: string, email: string, password: string, passwordConfirm: string) => {
  try {
    const response = await fetch(`${API_BASE}/accounts/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        username, 
        email, 
        password, 
        password_confirm: passwordConfirm 
      }),
    });

    if (!response.ok) throw new Error("Registration failed");

    const data = await response.json();

    // ✅ Save token for future requests
    if (data.token) localStorage.setItem("token", data.token);

    // ✅ Set current user using the returned "user" object
    setCurrentUser({
      name: data.user.username,
      email: data.user.email,
    });

    // ✅ Close register form & switch to search tab
    setShowRegisterForm(false);
    setActiveTab("search");

    toast({
      title: "Account Created",
      description: `Welcome ${data.user.username}!`,
    });
  } catch (error: any) {
    toast({
      title: "Registration Failed",
      description: error.message || "Something went wrong. Please try again.",
      variant: "destructive",
    });
  }
};


  /** LOGOUT */
  const handleLogout = () => {
    localStorage.removeItem("token");
    setCurrentUser(null);
    setActiveTab("search");
    toast({
      title: "Logged out",
      description: "You have been successfully logged out.",
    });
  };

  /** SEARCH HANDLER */
  const handleSearch = (filters: any) => {
    const filtered = mockTravels.filter(t =>
      (!filters.type || t.type === filters.type) &&
      (!filters.source || t.source === filters.source) &&
      (!filters.destination || t.destination === filters.destination) &&
      (!filters.date || t.date === filters.date)
    );
    setSearchResults(filtered);
    toast({
      title: "Search Results",
      description: `Found ${filtered.length} travel options`,
    });
  };

  /** HERO SECTION */
  const renderHero = () => (
    <section className="relative h-[70vh] flex items-center justify-center overflow-hidden">
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: `url(${heroImage})` }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-black/60 to-black/30"></div>
      </div>
      <div className="relative z-10 text-center text-white max-w-4xl px-4">
        <h1 className="text-5xl md:text-7xl font-bold mb-6">
          Discover Your Next
          <span className="block bg-gradient-to-r from-blue-400 to-orange-400 bg-clip-text text-transparent">
            Adventure
          </span>
        </h1>
        {!currentUser && (
          <div className="flex flex-wrap justify-center gap-4">
            <Button variant="hero" size="xl" onClick={() => setActiveTab("search")}>
              <MapPin className="mr-2 h-5 w-5" /> Start Your Journey
            </Button>
            <Button variant="outline" size="xl" onClick={() => setShowRegisterForm(true)}>
              <Star className="mr-2 h-5 w-5" /> Join TravelBooker
            </Button>
          </div>
        )}
      </div>
    </section>
  );

  /** SEARCH TAB */
  const renderSearchTab = () => (
    <div className="space-y-8">
      {!currentUser && renderHero()}
      <div className="container mx-auto px-4">
        <TravelSearchForm onSearch={handleSearch} />
        {searchResults.length > 0 ? (
          <div className="mt-8 grid gap-6 md:grid-cols-2">
            {searchResults.map(t => (
              <TravelCard key={t.id} travel={t} onBook={() => setSelectedTravel(t)} />
            ))}
          </div>
        ) : (
          <Card className="mt-8 text-center py-12">
            <CardContent>
              <Globe className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No travels found</h3>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-background">
      <Header
        currentUser={currentUser}
        onLoginClick={() => setShowLoginForm(true)}
        onRegisterClick={() => setShowRegisterForm(true)}
        onLogout={handleLogout}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      <main>
        {activeTab === "search" && renderSearchTab()}
      </main>

      {showLoginForm && (
        <LoginForm
          onLogin={handleLogin}
          onSwitchToRegister={() => { setShowLoginForm(false); setShowRegisterForm(true); }}
          onClose={() => setShowLoginForm(false)}
        />
      )}

      {showRegisterForm && (
        <RegisterForm
          onRegister={handleRegister}
          onSwitchToLogin={() => { setShowRegisterForm(false); setShowLoginForm(true); }}
          onClose={() => setShowRegisterForm(false)}
        />
      )}

      {selectedTravel && (
        <BookingModal
          travel={selectedTravel}
          onConfirm={() => setSelectedTravel(null)}
          onClose={() => setSelectedTravel(null)}
        />
      )}
    </div>
  );
};

export default Index;
