import { useState } from "react";
import { Button } from "@/components/ui/enhanced-button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Plane, Train, Bus, Users, Calendar, MapPin, CreditCard } from "lucide-react";
import { TravelOption } from "./TravelCard";
import { useToast } from "@/hooks/use-toast";

interface BookingModalProps {
  travel: TravelOption;
  onConfirm: (bookingData: {
    travelId: string;
    passengers: number;
    totalPrice: number;
    passengerDetails: Array<{ name: string; age: number; }>;
  }) => void;
  onClose: () => void;
  maxPassengers?: number;
}

const BookingModal = ({ travel, onConfirm, onClose, maxPassengers = 4 }: BookingModalProps) => {
  const [passengers, setPassengers] = useState(1);
  const [passengerDetails, setPassengerDetails] = useState([{ name: "", age: 0 }]);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'flight':
        return <Plane className="h-5 w-5" />;
      case 'train':
        return <Train className="h-5 w-5" />;
      case 'bus':
        return <Bus className="h-5 w-5" />;
      default:
        return <MapPin className="h-5 w-5" />;
    }
  };

  const handlePassengerCountChange = (count: number) => {
    setPassengers(count);
    const newDetails = Array.from({ length: count }, (_, i) => 
      passengerDetails[i] || { name: "", age: 0 }
    );
    setPassengerDetails(newDetails);
  };

  const updatePassengerDetail = (index: number, field: 'name' | 'age', value: string | number) => {
    const updated = [...passengerDetails];
    updated[index] = { ...updated[index], [field]: value };
    setPassengerDetails(updated);
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const totalPrice = travel.price * passengers;

  const handleConfirm = async () => {
    // Validation
    const hasEmptyDetails = passengerDetails.some(p => !p.name.trim() || p.age < 1);
    if (hasEmptyDetails) {
      toast({
        title: "Incomplete Details",
        description: "Please fill in all passenger details",
        variant: "destructive",
      });
      return;
    }

    if (passengers > travel.availableSeats) {
      toast({
        title: "Not Enough Seats",
        description: `Only ${travel.availableSeats} seats available`,
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);

    // Simulate booking process
    setTimeout(() => {
      onConfirm({
        travelId: travel.id,
        passengers,
        totalPrice,
        passengerDetails,
      });
      setIsLoading(false);
      toast({
        title: "Booking Confirmed!",
        description: `Your ${travel.type} booking has been confirmed.`,
      });
    }, 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm">
      <Card className="w-full max-w-2xl shadow-travel-lg max-h-[90vh] overflow-y-auto">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-2xl font-bold">Complete Your Booking</CardTitle>
            <Button variant="ghost" size="icon" onClick={onClose}>
              ×
            </Button>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {/* Travel Summary */}
          <div className="p-4 bg-muted/50 rounded-lg">
            <div className="flex items-center space-x-3 mb-3">
              <div className="p-2 rounded-lg bg-primary text-primary-foreground">
                {getTypeIcon(travel.type)}
              </div>
              <div>
                <h3 className="font-semibold capitalize">{travel.type}</h3>
                <Badge variant="secondary" className="text-xs">
                  ID: {travel.id}
                </Badge>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="flex items-center space-x-2">
                <MapPin className="h-4 w-4 text-muted-foreground" />
                <span className="capitalize">{travel.source.replace('-', ' ')} → {travel.destination.replace('-', ' ')}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <span>{new Date(travel.date).toLocaleDateString()} at {travel.time}</span>
              </div>
            </div>
          </div>

          {/* Passenger Count */}
          <div className="space-y-3">
            <Label>Number of Passengers</Label>
            <div className="flex items-center space-x-2">
              <Users className="h-4 w-4 text-muted-foreground" />
              <select
                value={passengers}
                onChange={(e) => handlePassengerCountChange(parseInt(e.target.value))}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              >
                {Array.from({ length: Math.min(travel.availableSeats, maxPassengers) }, (_, i) => i + 1).map(num => (
                  <option key={num} value={num}>
                    {num} {num === 1 ? 'Passenger' : 'Passengers'}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Passenger Details */}
          <div className="space-y-4">
            <Label className="text-base font-semibold">Passenger Details</Label>
            {passengerDetails.map((passenger, index) => (
              <div key={index} className="p-4 border rounded-lg space-y-3">
                <h4 className="font-medium">Passenger {index + 1}</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <Label htmlFor={`name-${index}`}>Full Name</Label>
                    <Input
                      id={`name-${index}`}
                      type="text"
                      placeholder="Enter full name"
                      value={passenger.name}
                      onChange={(e) => updatePassengerDetail(index, 'name', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor={`age-${index}`}>Age</Label>
                    <Input
                      id={`age-${index}`}
                      type="number"
                      placeholder="Age"
                      min="1"
                      max="120"
                      value={passenger.age || ''}
                      onChange={(e) => updatePassengerDetail(index, 'age', parseInt(e.target.value) || 0)}
                      required
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>

          <Separator />

          {/* Price Summary */}
          <div className="space-y-3">
            <h3 className="font-semibold flex items-center space-x-2">
              <CreditCard className="h-4 w-4" />
              <span>Price Summary</span>
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Base price per person:</span>
                <span>{formatPrice(travel.price)}</span>
              </div>
              <div className="flex justify-between">
                <span>Number of passengers:</span>
                <span>{passengers}</span>
              </div>
              <Separator />
              <div className="flex justify-between text-lg font-semibold">
                <span>Total Amount:</span>
                <span className="text-primary">{formatPrice(totalPrice)}</span>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <Button variant="outline" onClick={onClose} className="flex-1">
              Cancel
            </Button>
            <Button 
              variant="travel" 
              onClick={handleConfirm} 
              disabled={isLoading}
              className="flex-1"
            >
              {isLoading ? "Processing..." : `Confirm Booking - ${formatPrice(totalPrice)}`}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default BookingModal;