import { formatPrice, calculateDiscount } from '../utils/helpers';
import { Badge } from './ui/Badge';

export default function PriceDisplay({ 
  finalPrice, 
  competitorPrice,
  basePriceDollar,
  exchangeRate,
  showDiscount = true,
  className = ''
}) {
  const discount = competitorPrice ? calculateDiscount(finalPrice, competitorPrice) : 0;

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      {/* Final Price */}
      <span className="price text-2xl font-bold text-primary">
        {formatPrice(finalPrice)} تومان
      </span>

      {/* Competitor Price (if available) */}
      {competitorPrice && (
        <span className="text-gray-500 line-through text-sm">
          {formatPrice(competitorPrice)} تومان
        </span>
      )}

      {/* Discount Badge */}
      {showDiscount && discount > 0 && (
        <Badge variant="success" size="small">
          {discount}% تخفیف
        </Badge>
      )}

      {/* Base Price in Dollar */}
      {basePriceDollar && exchangeRate && (
        <div className="text-xs text-gray-500">
          ≈ ${basePriceDollar.toFixed(2)} (نرخ: {formatPrice(exchangeRate)})
        </div>
      )}
    </div>
  );
}
