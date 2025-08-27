import { Button } from "@/components/ui/enhanced-button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Plane, Train, Bus, MapPin, Calendar, Users, Clock } from "lucide-react";

export interface Booking {
  id: string;
  travelId: string;
  type: 'flight' | 'train' | 'bus';
  source: string;
  destination: string;
  date: string;
  time: string;
  passengers: number;
  totalPrice: number;
  status: 'confirmed' | 'cancelled' | 'completed';
  bookingDate: string;
  passengerDetails: Array<{ name: string; age: number; }>;
}

interface BookingCardProps {
  booking: Booking;
  onCancel?: (bookingId: string) => void;
  showCancelButton?: boolean;
}

const BookingCard = ({ booking, onCancel, showCancelButton = true }: BookingCardProps) => {
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

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed':
        return 'bg-success text-success-foreground';
      case 'cancelled':
        return 'bg-destructive text-destructive-foreground';
      case 'completed':
        return 'bg-muted text-muted-foreground';
      default:
        return 'bg-secondary text-secondary-foreground';
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const isUpcoming = new Date(booking.date) > new Date();
  const canCancel = booking.status === 'confirmed' && isUpcoming;

  return (
    <Card className="shadow-travel-md hover:shadow-travel-lg transition-all duration-300">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-primary text-primary-foreground">
              {getTypeIcon(booking.type)}
            </div>
            <div>
              <h3 className="font-semibold text-lg capitalize">{booking.type}</h3>
              <p className="text-sm text-muted-foreground">Booking ID: {booking.id}</p>
            </div>
          </div>
          <Badge className={getStatusColor(booking.status)}>
            {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Route Information */}
        <div className="flex items-center justify-between">
          <div className="text-center">
            <p className="font-semibold text-lg capitalize">{booking.source.replace('-', ' ')}</p>
            <p className="text-sm text-muted-foreground">Departure</p>
          </div>
          
          <div className="flex-1 px-4">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-muted"></div>
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">
                  {booking.type}
                </span>
              </div>
            </div>
          </div>
          
          <div className="text-center">
            <p className="font-semibold text-lg capitalize">{booking.destination.replace('-', ' ')}</p>
            <p className="text-sm text-muted-foreground">Arrival</p>
          </div>
        </div>

        {/* Travel Details */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <Calendar className="h-4 w-4 text-muted-foreground" />
            <div>
              <p className="font-medium">{formatDate(booking.date)}</p>
              <p className="text-muted-foreground">Travel Date</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Clock className="h-4 w-4 text-muted-foreground" />
            <div>
              <p className="font-medium">{booking.time}</p>
              <p className="text-muted-foreground">Departure Time</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Users className="h-4 w-4 text-muted-foreground" />
            <div>
              <p className="font-medium">{booking.passengers}</p>
              <p className="text-muted-foreground">Passengers</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <div>
              <p className="font-medium text-primary">{formatPrice(booking.totalPrice)}</p>
              <p className="text-muted-foreground">Total Paid</p>
            </div>
          </div>
        </div>

        {/* Passengers List */}
        <div className="space-y-2">
          <h4 className="font-medium text-sm">Passengers:</h4>
          <div className="flex flex-wrap gap-2">
            {booking.passengerDetails.map((passenger, index) => (
              <Badge key={index} variant="outline" className="text-xs">
                {passenger.name} ({passenger.age}y)
              </Badge>
            ))}
          </div>
        </div>

        {/* Booking Info */}
        <div className="pt-3 border-t text-xs text-muted-foreground">
          <p>Booked on: {formatDate(booking.bookingDate)}</p>
        </div>

        {/* Action Buttons */}
        {canCancel && showCancelButton && onCancel && (
          <div className="pt-3 border-t">
            <Button 
              variant="destructive" 
              size="sm" 
              onClick={() => onCancel(booking.id)}
              className="w-full md:w-auto"
            >
              Cancel Booking
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default BookingCard;