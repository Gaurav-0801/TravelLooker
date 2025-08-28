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
import { Plane, MapPin, Calendar, Clock, Star, Globe } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import heroImage from "@/assets/hero-travel.jpg";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "https://travellooker.onrender.com";

// Mock travels
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
  {
    id: "BS003",
    type: "bus",
    source: "san-francisco",
    destination: "seattle",
    date: "2024-09-17",
    time: "10:00",
    duration: "12h 30m",
    price: 45,
    availableSeats: 8,
    operator: "Greyhound"
  }
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

  useEffect(() => {
    setSearchResults(mockTravels);
  }, []);

  // ✅ Login/Signup handlers
  const handleLoginSuccess = (user: User, token: string) => {
    localStorage.setItem("token", token);
    setCurrentUser(user);
    setActiveTab("search");
    setShowLoginForm(false);
  };

  const handleRegisterSuccess = (user: User, token: string) => {
    localStorage.setItem("token", token);
    setCurrentUser(user);
    setActiveTab("search");
    setShowRegisterForm(false);
  };

  const handleLogout = async () => {
    try {
      await fetch(`${API_BASE}/accounts/logout/`, { method: "POST", credentials: "include" });
    } catch (err) {
      console.warn("Logout failed", err);
    }
    localStorage.removeItem("token");
    setCurrentUser(null);
    setActiveTab("search");
    toast({ title: "Logged out", description: "You have been logged out." });
  };

  const handleSearch = (filters: any) => {
    const filtered = mockTravels.filter(travel => {
      return (!filters.type || travel.type === filters.type) &&
             (!filters.source || travel.source === filters.source) &&
             (!filters.destination || travel.destination === filters.destination) &&
             (!filters.date || travel.date === filters.date);
    });
    setSearchResults(filtered);
    toast({ title: "Search Results", description: `Found ${filtered.length} travel options` });
  };

  const handleBookTravel = (travel: TravelOption) => {
    if (!currentUser) {
      setShowLoginForm(true);
      return;
    }
    setSelectedTravel(travel);
  };

  const handleConfirmBooking = (bookingData: any) => {
    const newBooking: Booking = {
      id: `BK${Date.now()}`,
      travelId: bookingData.travelId,
      type: selectedTravel!.type,
      source: selectedTravel!.source,
      destination: selectedTravel!.destination,
      date: selectedTravel!.date,
      time: selectedTravel!.time,
      passengers: bookingData.passengers,
      totalPrice: bookingData.totalPrice,
      status: 'confirmed',
      bookingDate: new Date().toISOString().split('T')[0],
      passengerDetails: bookingData.passengerDetails
    };
    setUserBookings(prev => [newBooking, ...prev]);
    setSelectedTravel(null);
    setActiveTab("bookings");
  };

  const handleCancelBooking = (bookingId: string) => {
    setUserBookings(prev =>
      prev.map(booking =>
        booking.id === bookingId ? { ...booking, status: 'cancelled' as const } : booking
      )
    );
    toast({ title: "Booking Cancelled", description: "Your booking has been cancelled successfully." });
  };

  const renderHeroSection = () => (
    <section className="relative h-[70vh] flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: `url(${heroImage})` }}>
        <div className="absolute inset-0 bg-gradient-to-r from-black/60 to-black/30"></div>
      </div>
      <div className="relative z-10 text-center text-white max-w-4xl px-4">
        <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-float">
          Discover Your Next
          <span className="block bg-gradient-to-r from-blue-400 to-orange-400 bg-clip-text text-transparent">
            Adventure
          </span>
        </h1>
        <p className="text-xl md:text-2xl mb-8 text-white/90">
          Book flights, trains, and buses worldwide
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Button variant="hero" size="xl" onClick={() => setActiveTab("search")}>
            <MapPin className="mr-2 h-5 w-5" /> Start Your Journey
          </Button>
          {!currentUser && (
            <Button variant="outline" size="xl" onClick={() => setShowRegisterForm(true)}>
              <Star className="mr-2 h-5 w-5" /> Join TravelBooker
            </Button>
          )}
        </div>
      </div>
    </section>
  );

  const renderSearchTab = () => (
    <div className="space-y-8">
      {!currentUser && renderHeroSection()}
      <div className="container mx-auto px-4">
        <TravelSearchForm onSearch={handleSearch} />
        {searchResults.length > 0 ? (
          <div className="mt-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">Available Travels</h2>
              <Badge variant="secondary" className="text-sm">{searchResults.length} options found</Badge>
            </div>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-1">
              {searchResults.map(travel => (
                <TravelCard key={travel.id} travel={travel} onBook={handleBookTravel} />
              ))}
            </div>
          </div>
        ) : (
          <Card className="mt-8 text-center py-12">
            <CardContent>
              <Globe className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No travels found</h3>
              <p className="text-muted-foreground">Try adjusting your search criteria</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );

  const renderBookingsTab = () => (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">My Bookings</h1>
      {userBookings.length > 0 ? (
        <div className="space-y-6">
          {userBookings.map(booking => (
            <BookingCard key={booking.id} booking={booking} onCancel={handleCancelBooking} />
          ))}
        </div>
      ) : (
        <Card className="text-center py-12">
          <CardContent>
            <Calendar className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No bookings yet</h3>
            <p className="text-muted-foreground mb-4">Start exploring and book your first travel adventure</p>
            <Button variant="travel" onClick={() => setActiveTab("search")}>Browse Travels</Button>
          </CardContent>
        </Card>
      )}
    </div>
  );

  const renderProfileTab = () => (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Profile</h1>
      {currentUser ? (
        <Card className="max-w-md">
          <CardContent className="pt-6 space-y-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground">Name</label>
              <p className="text-lg font-semibold">{currentUser.name}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Email</label>
              <p className="text-lg">{currentUser.email}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Total Bookings</label>
              <p className="text-lg font-semibold">{userBookings.length}</p>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card className="text-center py-12">
          <CardContent>
            <p className="text-muted-foreground mb-4">Please log in to view your profile</p>
            <Button variant="travel" onClick={() => setShowLoginForm(true)}>Log In</Button>
          </CardContent>
        </Card>
      )}
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
        {activeTab === "bookings" && renderBookingsTab()}
        {activeTab === "profile" && renderProfileTab()}
      </main>

      {showLoginForm && (
        <LoginForm
          onLogin={handleLoginSuccess}
          onSwitchToRegister={() => { setShowLoginForm(false); setShowRegisterForm(true); }}
          onClose={() => setShowLoginForm(false)}
        />
      )}

      {showRegisterForm && (
        <RegisterForm
          onRegister={handleRegisterSuccess}
          onSwitchToLogin={() => { setShowRegisterForm(false); setShowLoginForm(true); }}
          onClose={() => setShowRegisterForm(false)}
        />
      )}

      {selectedTravel && (
        <BookingModal
          travel={selectedTravel}
          onConfirm={handleConfirmBooking}
          onClose={() => setSelectedTravel(null)}
        />
      )}
    </div>
  );
};

export default Index;
