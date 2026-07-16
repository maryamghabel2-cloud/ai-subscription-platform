import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import axios from 'axios';

const CheckCircleIcon = () => (
  <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price);
};

export default function OrderSuccessPage({ usdtRate }) {
  const router = useRouter();
  const { order_id } = router.query;
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!order_id) return;

    const fetchOrder = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/orders/${order_id}`);
        setOrder(response.data);
        setError(null);
      } catch (err) {
        console.error('Error fetching order:', err);
        setError('خطا در دریافت اطلاعات سفارش.');
      } finally {
        setLoading(false);
      }
    };

    fetchOrder();
  }, [order_id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Head>
          <title>در حال دریافت اطلاعات... | AI Subscription Platform</title>
        </Head>
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">در حال دریافت اطلاعات سفارش...</p>
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
        <title>سفارش موفق! | AI Subscription Platform</title>
        <meta name="description" content="سفارش شما با موفقیت انجام شد" />
      </Head>

      <main className="max-w-4xl mx-auto py-20 px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden text-center">
          {/* Success Icon */}
          <div className="bg-green-100 py-12">
            <CheckCircleIcon className="text-green-600 mx-auto" />
          </div>

          {/* Success Message */}
          <div className="p-8">
            <h1 className="text-3xl font-bold text-dark-color mb-4">
              سفارش شما با موفقیت انجام شد!
            </h1>
            <p className="text-gray-600 mb-8">
              شماره سفارش: <span className="font-bold text-primary">#{order?.order_number}</span>
            </p>

            {/* Order Summary */}
            <div className="bg-gray-50 rounded-lg p-6 mb-8">
              <h2 className="font-semibold mb-4">جمع سفارش</h2>
              <div className="space-y-3 text-right">
                <div className="flex justify-between">
                  <span className="text-gray-500">محصول:</span>
                  <span className="font-medium">{order?.product?.name || 'نامشخص'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">تعداد:</span>
                  <span className="font-medium">{order?.quantity || 1}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">مبلغ پرداختی:</span>
                  <span className="price text-xl font-bold text-primary">
                    {formatPrice(order?.total_price_tomans || 0)} تومان
                  </span>
                </div>
              </div>
            </div>

            {/* Delivery Info */}
            {order?.delivery_info && (
              <div className="bg-blue-50 rounded-lg p-6 mb-8">
                <h2 className="font-semibold mb-4">اطلاعات اکانت</h2>
                <div className="bg-white rounded p-4 text-left">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                    {JSON.stringify(order.delivery_info, null, 2)}
                  </pre>
                </div>
                <p className="text-blue-600 text-sm mt-4">
                  اطلاعات اکانت به ایمیل شما نیز ارسال شده است.
                </p>
              </div>
            )}

            {/* Actions */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/" className="btn btn-primary">
                بازگشت به صفحه اصلی
              </Link>
              <Link href="/#products" className="btn btn-outline">
                مشاهده محصولات دیگر
              </Link>
            </div>

            {/* Support */}
            <div className="mt-8 pt-8 border-t border-gray-200">
              <p className="text-gray-500 mb-4">
                در صورت هرگونه سوال یا مشکل، می‌توانید با پشتیبانی تماس بگیرید.
              </p>
              <Link 
                href="/#contact" 
                className="btn btn-outline text-sm"
              >
                تماس با پشتیبانی
              </Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
