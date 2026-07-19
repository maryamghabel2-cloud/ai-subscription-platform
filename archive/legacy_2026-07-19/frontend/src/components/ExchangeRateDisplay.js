import { useState, useEffect } from 'react';
import { formatPrice } from '../utils/helpers';
import axios from 'axios';

export default function ExchangeRateDisplay({ initialRate = 190000 }) {
  const [usdtRate, setUsdtRate] = useState(initialRate);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    const fetchRate = async () => {
      try {
        const response = await axios.get('/api/exchange-rate');
        if (response.data) {
          setUsdtRate(response.data.rate);
          setLastUpdated(response.data.last_updated);
        }
      } catch (error) {
        console.error('Error fetching exchange rate:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRate();

    // Refresh every 30 seconds
    const interval = setInterval(fetchRate, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center space-x-2">
        <span>نرخ تتر:</span>
        <span className="font-bold text-primary">{formatPrice(initialRate)} تومان</span>
        <span className="animate-pulse">...</span>
      </div>
    );
  }

  return (
    <div className="flex items-center space-x-2">
      <span>نرخ تتر:</span>
      <span className="font-bold text-primary">{formatPrice(usdtRate)} تومان</span>
      {lastUpdated && (
        <span className="text-xs text-gray-500">
          (به‌روزرسانی: {new Date(lastUpdated).toLocaleTimeString('fa-IR')})
        </span>
      )}
    </div>
  );
}
