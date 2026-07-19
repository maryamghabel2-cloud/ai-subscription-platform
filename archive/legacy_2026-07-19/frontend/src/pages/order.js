import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import axios from 'axios';

const ArrowLeftIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
  </svg>
);

const CheckCircleIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const ClockIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price);
};

export default function OrderPage({ usdtRate }) {
  const router = useRouter();
  const { product } = router.query;
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [paymentVerified, setPaymentVerified] = useState(false);
  const [txHash, setTxHash] = useState('');

  // Fetch product price and create order
  useEffect(() => {
    if (!product) return;

    const createOrder = async () => {
      try {
        setLoading(true);
        
        // Calculate price first
        const priceResponse = await axios.post('/api/products/calculate-price', {
          product_name: product
        });
        
        const priceData = priceResponse.data;
        
        // Create order
        const orderResponse = await axios.post('/api/orders/', {
          product_id: 1, // For demo, we'll use product_id 1
          quantity: 1,
          payment_method: 'crypto'
        });
        
        setOrder({
          ...orderResponse.data,
          product_name: product,
          final_price: priceData.final_price,
          base_price_dollar: priceData.base_price_dollar
        });
        setError(null);
      } catch (err) {
        console.error('Error creating order:', err);
        setError('خطا در ایجاد سفارش. لطفاً مجدداً امتحان کنید.');
      } finally {
        setLoading(false);
      }
    };

    createOrder();
  }, [product]);

  // Poll for payment verification
  useEffect(() => {
    if (!order || !paymentVerified) return;

    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`/api/orders/${order.id}/status`);
        if (response.data.status === 'delivered') {
          clearInterval(interval);
          router.push(`/order-success?order_id=${order.id}`);
        }
      } catch (err) {
        console.error('Error checking order status:', err);
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [order, paymentVerified]);

  const handleVerifyPayment = async () => {
    if (!order || !txHash) return;

    try {
      setLoading(true);
      const response = await axios.post(
        `/api/orders/${order.id}/confirm-payment`,
        { tx_hash: txHash }
      );
      
      if (response.data.status === 'success') {
        setPaymentVerified(true);
      }
    } catch (err) {
      console.error('Error verifying payment:', err);
      setError('خطا در تایید پرداخت. لطفاً اطلاعات را بررسی کنید.');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !order) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Head>
          <title>در حال ایجاد سفارش... | AI Subscription Platform</title>
        </Head>
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">در حال ایجاد سفارش...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Head>
          <title>خطا | AI Subscription Platform</title>
        </Head>
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
          <h2 className="text-red-600 text-xl font-bold mb-4">خطا!</h2>
          <p className="text-red-700 mb-4">{error}</p>
          <div className="flex space-x-4">
            <button 
              onClick={() => router.push('/')}
              className="btn btn-outline"
            >
              بازگشت به صفحه اصلی
            </button>
            <button 
              onClick={() => window.location.reload()}
              className="btn btn-primary"
            >
              تلاش مجدد
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>سفارش - {product} | AI Subscription Platform</title>
        <meta name="description" content={`سفارش ${product}`} />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center space-x-2">
              <ArrowLeftIcon />
              <span>بازگشت به صفحه اصلی</span>
            </Link>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          {/* Order Summary */}
          <div className="p-8 border-b border-gray-200">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold text-dark-color">سفارش شما</h1>
                <p className="text-gray-500 mt-1">
                  شماره سفارش: #{order?.order_number || '...'}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                {order?.status === 'delivered' && (
                  <span className="badge badge-success">تحویل شده</span>
                )}
                {order?.status === 'paid' && (
                  <span className="badge badge-info">در حال پردازش</span>
                )}
                {order?.status === 'pending' && (
                  <span className="badge badge-warning">در انتظار پرداخت</span>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Product Info */}
              <div>
                <h3 className="font-semibold mb-4">اطلاعات محصول</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-500">نام محصول:</span>
                    <span className="font-medium">{product}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">تعداد:</span>
                    <span className="font-medium">۱</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">قیمت دلاری:</span>
                    <span className="font-medium">${order?.base_price_dollar || '...'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">نرخ تتر:</span>
                    <span className="font-medium">{formatPrice(usdtRate)} تومان</span>
                  </div>
                </div>
              </div>

              {/* Price Info */}
              <div>
                <h3 className="font-semibold mb-4">اطلاعات پرداخت</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-500">مبلغ قابل پرداخت:</span>
                    <span className="price text-xl font-bold text-primary">
                      {formatPrice(order?.final_price || 0)} تومان
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">روش پرداخت:</span>
                    <span className="font-medium">کریپتو (USDT)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">مبلغ به USDT:</span>
                    <span className="font-medium">
                      {order?.payment_amount_crypto ? order.payment_amount_crypto.toFixed(2) : '...'} USDT
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Payment Instructions */}
          <div className="p-8 border-b border-gray-200">
            <h2 className="text-xl font-bold mb-6 flex items-center">
              <ClockIcon className="ml-2" />
              روش پرداخت
            </h2>

            <div className="bg-blue-50 rounded-lg p-6 mb-6">
              <h3 className="font-semibold mb-3">آدرس کیف پول برای پرداخت:</h3>
              <div className="flex items-center space-x-2">
                <code className="bg-blue-100 px-3 py-1 rounded text-sm font-mono">
                  {order?.payment_address || '...'}
                </code>
                <button 
                  onClick={() => {
                    if (order?.payment_address) {
                      navigator.clipboard.writeText(order.payment_address);
                      alert('آدرس کیف پول کپی شد!');
                    }
                  }}
                  className="btn btn-outline text-sm"
                >
                  کپی
                </button>
              </div>
            </div>

            <div className="bg-yellow-50 rounded-lg p-6 mb-6">
              <h3 className="font-semibold mb-3">مبلغ پرداخت:</h3>
              <p className="text-2xl font-bold text-yellow-700">
                {order?.payment_amount_crypto ? order.payment_amount_crypto.toFixed(2) : '...'} USDT
              </p>
              <p className="text-sm text-yellow-600 mt-1">
                (معادل {formatPrice(order?.final_price || 0)} تومان)
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="font-semibold mb-3">دستورالعمل پرداخت:</h3>
              <ol className="list-decimal list-inside space-y-2 text-gray-600">
                <li>به کیف پول خود (مثل Trust Wallet, Binance, etc.) وارد شوید.</li>
                <li>ارز USDT را انتخاب کنید.</li>
                <li>آدرس فوق را به عنوان آدرس مقصد وارد کنید.</li>
                <li>مبلغ {order?.payment_amount_crypto ? order.payment_amount_crypto.toFixed(2) : '...'} USDT را وارد کنید.</li>
                <li>پرداخت را انجام دهید.</li>
                <li>شبه تراکنش (TX Hash) را کپی کنید.</li>
                <li>شبه تراکنش را در فیلد زیر وارد کنید و روی "تایید پرداخت" کلیک کنید.</li>
              </ol>
            </div>
          </div>

          {/* Payment Verification */}
          {!paymentVerified && order?.status === 'pending' && (
            <div className="p-8">
              <h2 className="text-xl font-bold mb-6 flex items-center">
                <CheckCircleIcon className="ml-2" />
                تایید پرداخت
              </h2>

              <div className="max-w-md">
                <label htmlFor="tx-hash" className="block text-sm font-medium text-gray-700 mb-2">
                  شبه تراکنش (TX Hash)
                </label>
                <input
                  type="text"
                  id="tx-hash"
                  value={txHash}
                  onChange={(e) => setTxHash(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all"
                  placeholder="مثلا: 0x1234567890abcdef..."
                  dir="ltr"
                />
                <button
                  onClick={handleVerifyPayment}
                  disabled={loading || !txHash}
                  className="btn btn-primary w-full mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'در حال بررسی...' : 'تایید پرداخت'}
                </button>
              </div>
            </div>
          )}

          {/* Order Status */}
          {order?.status !== 'pending' && (
            <div className="p-8 bg-green-50 rounded-lg">
              <div className="flex items-center mb-4">
                <CheckCircleIcon className="w-8 h-8 text-green-600 ml-2" />
                <h2 className="text-xl font-bold text-green-700">سفارش شما با موفقیت ثبت شد!</h2>
              </div>
              
              {order?.status === 'delivered' && (
                <p className="text-green-600">
                  سفارش شما تحویل شده است. لطفاً ایمیل خود را بررسی کنید.
                </p>
              )}
              
              {order?.status === 'paid' && (
                <p className="text-blue-600">
                  پرداخت شما دریافت شد. سفارش در حال پردازش است.
                  این فرآیند ممکن است چند دقیقه طول بکشد.
                </p>
              )}

              {order?.status === 'processing' && (
                <p className="text-blue-600">
                  سفارش شما در حال پردازش است. لطفاً صبر کنید...
                </p>
              )}

              <div className="mt-6">
                <Link href="/" className="btn btn-outline">
                  بازگشت به صفحه اصلی
                </Link>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
