import { Button } from "@/components/ui/enhanced-button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Clock, MapPin, Users, Plane, Train, Bus } from "lucide-react";

export interface TravelOption {
  id: string;
  type: 'flight' | 'train' | 'bus';
  source: string;
  destination: string;
  date: string;
  time: string;
  duration: string;
  price: number;
  availableSeats: number;
  airline?: string;
  operator?: string;
}

interface TravelCardProps {
  travel: TravelOption;
  onBook: (travel: TravelOption) => void;
}

const TravelCard = ({ travel, onBook }: TravelCardProps) => {
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

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'flight':
        return 'bg-blue-100 text-blue-800';
      case 'train':
        return 'bg-green-100 text-green-800';
      case 'bus':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
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
    });
  };

  return (
    <Card className="hover:shadow-travel-lg transition-all duration-300 hover:scale-[1.02] cursor-pointer group">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded-lg ${getTypeColor(travel.type)}`}>
              {getTypeIcon(travel.type)}
            </div>
            <div>
              <h3 className="font-semibold text-lg capitalize">{travel.type}</h3>
              <p className="text-sm text-muted-foreground">
                {travel.airline || travel.operator || `${travel.type} Service`}
              </p>
            </div>
          </div>
          <Badge variant="secondary" className="text-xs">
            {travel.availableSeats} seats left
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Route Information */}
        <div className="flex items-center justify-between">
          <div className="text-center">
            <p className="font-semibold text-lg capitalize">{travel.source.replace('-', ' ')}</p>
            <p className="text-sm text-muted-foreground">{travel.time}</p>
          </div>
          
          <div className="flex-1 px-4">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-muted"></div>
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">
                  {travel.duration}
                </span>
              </div>
            </div>
          </div>
          
          <div className="text-center">
            <p className="font-semibold text-lg capitalize">{travel.destination.replace('-', ' ')}</p>
            <p className="text-sm text-muted-foreground">
              {new Date(`${travel.date}T${travel.time}`).toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: false,
              })}
            </p>
          </div>
        </div>

        {/* Date and Additional Info */}
        <div className="flex items-center justify-between text-sm text-muted-foreground">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <Clock className="h-4 w-4" />
              <span>{formatDate(travel.date)}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Users className="h-4 w-4" />
              <span>{travel.availableSeats} available</span>
            </div>
          </div>
        </div>

        {/* Price and Book Button */}
        <div className="flex items-center justify-between pt-2 border-t">
          <div>
            <p className="text-2xl font-bold text-primary">{formatPrice(travel.price)}</p>
            <p className="text-xs text-muted-foreground">per person</p>
          </div>
          <Button 
            variant="travel" 
            onClick={() => onBook(travel)}
            className="group-hover:scale-105 transition-transform"
          >
            Book Now
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default TravelCard;