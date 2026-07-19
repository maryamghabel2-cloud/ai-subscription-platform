import { useState } from 'react';
import Link from 'next/link';
import { formatPrice, calculateDiscount } from '../utils/helpers';
import { Button } from './ui/Button';
import { Badge } from './ui/Badge';

const SparklesIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
  </svg>
);

const categories = {
  chat: 'چت و متن',
  image: 'ساخت عکس',
  video: 'ساخت ویدیو',
  coding: 'کد نویسی',
  music: 'موسیقی',
  subscription: 'اشتراک‌ها',
  api: 'APIها',
  shared: 'اشتراکی',
  all_in_one: 'همه در یک جا'
};

const categoryIcons = {
  chat: '💬',
  image: '🎨',
  video: '🎬',
  coding: '💻',
  music: '🎵',
  subscription: '📺',
  api: '🔌',
  shared: '👥',
  all_in_one: '🌐'
};

export default function ProductCard({ product, usdtRate }) {
  const [isHovered, setIsHovered] = useState(false);

  // Calculate price based on USDT rate
  const basePriceTomans = product.base_price_dollar * usdtRate;
  const finalPrice = product.final_price || Math.round(basePriceTomans * 1.3); // Default 30% margin
  const competitorPrice = product.competitor_average_price;
  const discount = competitorPrice ? calculateDiscount(finalPrice, competitorPrice) : 0;

  return (
    <div
      className="group relative bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden transition-all hover:shadow-md hover:border-primary"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Product Image */}
      <div className="aspect-w-16 aspect-h-12 bg-gray-50">
        <div className="h-48 flex items-center justify-center">
          {product.image_url ? (
            <img 
              src={product.image_url} 
              alt={product.product_name}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center">
              <SparklesIcon className="w-8 h-8 text-primary" />
            </div>
          )}
        </div>
      </div>

      {/* Product Content */}
      <div className="p-4">
        {/* Product Name */}
        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-1">
          {product.product_name}
        </h3>

        {/* Category and Type Badges */}
        <div className="flex items-center space-x-2 mb-3">
          {product.category && (
            <Badge variant="info">
              {categoryIcons[product.category] || categories[product.category] || product.category}
            </Badge>
          )}
          {product.product_type === 'shared' && (
            <Badge variant="warning">اشتراکی</Badge>
          )}
        </div>

        {/* Price Section */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <p className="text-2xl font-bold text-primary">
              {formatPrice(finalPrice)} تومان
            </p>
            {competitorPrice && (
              <p className="text-sm text-gray-500 line-through">
                {formatPrice(competitorPrice)} تومان
              </p>
            )}
          </div>
          {discount > 0 && (
            <Badge variant="success">
              {discount}% تخفیف
            </Badge>
          )}
        </div>

        {/* Action Button */}
        <Link
          href={`/order?product=${encodeURIComponent(product.product_name)}`}
          className="w-full"
        >
          <Button variant="primary" size="medium" className="w-full">
            خرید
          </Button>
        </Link>

        {/* Hover Details */}
        {isHovered && product.description && (
          <div className="absolute inset-0 bg-black bg-opacity-50 flex items-end p-4 rounded-xl">
            <p className="text-white text-sm line-clamp-2">{product.description}</p>
          </div>
        )}
      </div>
    </div>
  );
}
