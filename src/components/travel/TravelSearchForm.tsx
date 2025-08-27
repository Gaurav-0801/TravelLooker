import { useState } from "react";
import { Button } from "@/components/ui/enhanced-button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MapPin, Calendar, Users, Search } from "lucide-react";

interface TravelSearchFormProps {
  onSearch: (filters: {
    type: string;
    source: string;
    destination: string;
    date: string;
    passengers: number;
  }) => void;
}

const TravelSearchForm = ({ onSearch }: TravelSearchFormProps) => {
  const [type, setType] = useState("");
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [date, setDate] = useState("");
  const [passengers, setPassengers] = useState(1);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch({
      type,
      source,
      destination,
      date,
      passengers,
    });
  };

  const cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle",
    "Denver", "Washington DC", "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City"
  ];

  return (
    <Card className="w-full shadow-travel-lg bg-gradient-card">
      <CardHeader>
        <CardTitle className="text-center text-2xl font-bold">Find Your Perfect Journey</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Travel Type */}
            <div className="space-y-2">
              <Label htmlFor="type">Travel Type</Label>
              <Select value={type} onValueChange={setType} required>
                <SelectTrigger>
                  <SelectValue placeholder="Select travel type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="flight">✈️ Flight</SelectItem>
                  <SelectItem value="train">🚆 Train</SelectItem>
                  <SelectItem value="bus">🚌 Bus</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Source */}
            <div className="space-y-2">
              <Label htmlFor="source">From</Label>
              <div className="relative">
                <MapPin className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Select value={source} onValueChange={setSource} required>
                  <SelectTrigger className="pl-10">
                    <SelectValue placeholder="Departure city" />
                  </SelectTrigger>
                  <SelectContent>
                    {cities.map((city) => (
                      <SelectItem key={city} value={city.toLowerCase().replace(/\s+/g, '-')}>
                        {city}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Destination */}
            <div className="space-y-2">
              <Label htmlFor="destination">To</Label>
              <div className="relative">
                <MapPin className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Select value={destination} onValueChange={setDestination} required>
                  <SelectTrigger className="pl-10">
                    <SelectValue placeholder="Destination city" />
                  </SelectTrigger>
                  <SelectContent>
                    {cities.map((city) => (
                      <SelectItem key={city} value={city.toLowerCase().replace(/\s+/g, '-')}>
                        {city}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Date */}
            <div className="space-y-2">
              <Label htmlFor="date">Departure Date</Label>
              <div className="relative">
                <Calendar className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="date"
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="pl-10"
                  min={new Date().toISOString().split('T')[0]}
                  required
                />
              </div>
            </div>

            {/* Passengers */}
            <div className="space-y-2">
              <Label htmlFor="passengers">Passengers</Label>
              <div className="relative">
                <Users className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Select value={passengers.toString()} onValueChange={(value) => setPassengers(parseInt(value))}>
                  <SelectTrigger className="pl-10">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {[1, 2, 3, 4, 5, 6, 7, 8].map((num) => (
                      <SelectItem key={num} value={num.toString()}>
                        {num} {num === 1 ? 'Passenger' : 'Passengers'}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Search Button */}
            <div className="flex items-end">
              <Button 
                type="submit" 
                variant="hero" 
                size="lg" 
                className="w-full"
              >
                <Search className="h-4 w-4 mr-2" />
                Search Travels
              </Button>
            </div>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default TravelSearchForm;