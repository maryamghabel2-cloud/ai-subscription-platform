import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  const router = useRouter();
  const [usdtRate, setUsdtRate] = useState(190000);
  const [loading, setLoading] = useState(true);

  // Fetch USDT rate on app load
  useEffect(() => {
    const fetchUsdtRate = async () => {
      try {
        const response = await fetch('/api/exchange-rate');
        if (response.ok) {
          const data = await response.json();
          setUsdtRate(data.rate);
        }
      } catch (error) {
        console.error('Error fetching USDT rate:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUsdtRate();

    // Refresh rate every 30 seconds
    const interval = setInterval(fetchUsdtRate, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <Head>
        <title>AI Subscription Platform - خرید اشتراک‌های هوش مصنوعی</title>
        <meta name="description" content="خرید اشتراک‌های نتفلیکس، اسپاتیفای، چت‌جی‌پی‌تی، میدجورنی و APIهای هوش مصنوعی با قیمت‌های تخفیف‌دار" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <Component 
        {...pageProps} 
        usdtRate={usdtRate} 
        loadingRate={loading}
      />
    </>
  );
}

export default MyApp;
