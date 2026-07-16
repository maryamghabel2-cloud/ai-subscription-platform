import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import Head from 'next/head';

export default function PaymentPage() {
  const router = useRouter();
  const { product, amount, payment_method: initialPaymentMethod } = router.query;
  const [paymentDetails, setPaymentDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState(initialPaymentMethod || 'crypto');
  const [txHash, setTxHash] = useState('');
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState(null);

  // Format price in Persian format
  const formatPrice = (price) => {
    return new Intl.NumberFormat('fa-IR').format(price);
  };

  // Fetch payment details
  useEffect(() => {
    if (!product || !amount) {
      router.push('/');
      return;
    }

    const fetchPaymentDetails = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await axios.post('/api/payments/create', {
          product_name: product,
          amount: parseInt(amount),
          payment_method: paymentMethod,
          callback_url: typeof window !== 'undefined' ? window.location.origin + '/payment/verify' : ''
        });

        setPaymentDetails(response.data);
      } catch (err) {
        console.error('Payment error:', err);
        setError('خطا در ایجاد پرداخت. لطفاً دوباره امتحان کنید.');
      } finally {
        setLoading(false);
      }
    };

    fetchPaymentDetails();
  }, [product, amount, paymentMethod]);

  const handlePaymentMethodChange = (method) => {
    setPaymentMethod(method);
  };

  const handleVerifyCryptoPayment = async (e) => {
    e.preventDefault();
    
    if (!txHash || txHash.length < 40) {
      setError('لطفاً شماره تراکنش (Tx Hash) معتبر وارد کنید');
      return;
    }

    try {
      setIsVerifying(true);
      setError(null);
      
      const response = await axios.post('/api/payments/verify', {
        payment_method: 'crypto',
        payment_id: paymentDetails.payment_id,
        tx_hash: txHash
      });

      setVerificationResult(response.data);
      
      if (response.data.verified) {
        // Redirect to success page
        setTimeout(() => {
          router.push(`/order-success?product=${encodeURIComponent(product)}&amount=${amount}&payment_method=crypto`);
        }, 2000);
      }
    } catch (err) {
      console.error('Verification error:', err);
      setError('خطا در تایید پرداخت. لطفاً شماره تراکنش را بررسی کنید.');
    } finally {
      setIsVerifying(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Head><title>در حال آماده‌سازی پرداخت...</title></Head>
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">در حال آماده‌سازی درگاه پرداخت...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Head><title>خطا در پرداخت</title></Head>
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
          <h2 className="text-red-600 text-xl font-bold mb-4">خطا!</h2>
          <p className="text-red-700 mb-4">{error}</p>
          <div className="flex space-x-4">
            <button onClick={() => router.back()} className="btn btn-outline text-red-600 border-red-200 hover:bg-red-50">
              بازگشت
            </button>
            <button onClick={() => window.location.reload()} className="btn btn-primary">
              تلاش مجدد
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <Head>
        <title>پرداخت | {product}</title>
        <meta name="description" content={`پرداخت برای ${product} - مبلغ: ${formatPrice(parseInt(amount))} تومان`} />
      </Head>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Breadcrumb */}
        <nav className="text-sm text-gray-500 mb-6" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2">
            <li>
              <button onClick={() => router.push('/')} className="hover:text-primary">
                خانه
              </button>
            </li>
            <li className="text-gray-400">/</li>
            <li>
              <button onClick={() => router.push('/products')} className="hover:text-primary">
                محصولات
              </button>
            </li>
            <li className="text-gray-400">/</li>
            <li className="text-gray-700">پرداخت</li>
          </ol>
        </nav>

        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Payment Header */}
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-dark-color mb-2">پرداخت سفارش</h1>
            <p className="text-gray-600">
              محصول: <span className="font-semibold">{product}</span>
            </p>
            <p className="text-gray-600">
              مبلغ: <span className="font-semibold text-primary">{formatPrice(parseInt(amount))} تومان</span>
            </p>
          </div>

          {/* Payment Method Selection */}
          <div className="mb-8">
            <h2 className="text-lg font-semibold mb-4 text-right">روش پرداخت را انتخاب کنید:</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Crypto Payment Option */}
              <button
                onClick={() => handlePaymentMethodChange('crypto')}
                className={`payment-method-card ${paymentMethod === 'crypto' ? 'active' : ''}`}
              >
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center mr-3">
                    <span className="text-white font-bold text-sm">₮</span>
                  </div>
                  <div className="text-left">
                    <h3 className="font-semibold">پرداخت با تتر (USDT)</h3>
                    <p className="text-sm text-gray-600">پرداخت با ارز دیجیتال - تحویل فوری</p>
                  </div>
                  <div className="mr-auto">
                    {paymentMethod === 'crypto' && (
                      <svg className="w-5 h-5 text-primary" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                </div>
              </button>

              {/* Zarinpal Payment Option */}
              <button
                onClick={() => handlePaymentMethodChange('zarinpal')}
                className={`payment-method-card ${paymentMethod === 'zarinpal' ? 'active' : ''}`}
              >
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center mr-3">
                    <span className="text-white font-bold text-sm">Z</span>
                  </div>
                  <div className="text-left">
                    <h3 className="font-semibold">زرین‌پال</h3>
                    <p className="text-sm text-gray-600">پرداخت با کارت بانکی - تحویل پس از تایید</p>
                  </div>
                  <div className="mr-auto">
                    {paymentMethod === 'zarinpal' && (
                      <svg className="w-5 h-5 text-primary" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                </div>
              </button>
            </div>
          </div>

          {/* Payment Instructions */}
          {paymentDetails && (
            <div className="payment-instructions">
              {paymentMethod === 'crypto' ? (
                <div className="crypto-payment">
                  <h3 className="text-lg font-semibold mb-4 text-right">اطلاعات پرداخت با تتر:</h3>
                  
                  {/* Payment Info Card */}
                  <div className="bg-blue-50 rounded-lg p-6 mb-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-4">
                        <div>
                          <p className="text-sm text-gray-600 mb-1">مبلغ:</p>
                          <p className="text-2xl font-bold text-primary">
                            {paymentDetails.usdt_amount} USDT
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600 mb-1">شبکه:</p>
                          <p className="font-semibold">{paymentDetails.network}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600 mb-1">معادل:</p>
                          <p className="font-semibold">
                            {formatPrice(paymentDetails.amount_toman)} تومان
                          </p>
                        </div>
                      </div>
                      <div className="space-y-4">
                        <div>
                          <p className="text-sm text-gray-600 mb-1">آدرس کیف پول:</p>
                          <p className="font-mono text-sm bg-white p-2 rounded border break-all">
                            {paymentDetails.usdt_address}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600 mb-1">شناسه پرداخت:</p>
                          <p className="font-mono text-sm bg-white p-2 rounded border">
                            {paymentDetails.payment_id}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* QR Code */}
                  <div className="text-center mb-6">
                    <p className="text-gray-600 mb-4">کد QR برای پرداخت:</p>
                    <div className="bg-white p-4 rounded-lg shadow-md inline-block">
                      <img
                        src={paymentDetails.qrcode_url}
                        alt="QR Code for payment"
                        className="w-64 h-64"
                      />
                    </div>
                  </div>

                  {/* Instructions */}
                  <div className="bg-yellow-50 rounded-lg p-4 mb-6">
                    <h4 className="font-semibold mb-2 text-right">راهنمای پرداخت:</h4>
                    <ol className="list-decimal list-inside space-y-2 text-sm text-gray-700 text-right">
                      <li>مبلغ {paymentDetails.usdt_amount} USDT را به آدرس بالا پرداخت کنید</li>
                      <li>از شبکه {paymentDetails.network} استفاده کنید</li>
                      <li>پس از پرداخت، شماره تراکنش (Tx Hash) را کپی کنید</li>
                      <li>در فرم زیر وارد کنید و روی "تایید پرداخت" کلیک کنید</li>
                      <li>پس از تایید، اطلاعات اکانت برای شما ارسال خواهد شد</li>
                    </ol>
                  </div>

                  {/* Verification Form */}
                  {!verificationResult ? (
                    <form onSubmit={handleVerifyCryptoPayment} className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium mb-2 text-right">شماره تراکنش (Tx Hash)</label>
                        <input
                          type="text"
                          value={txHash}
                          onChange={(e) => setTxHash(e.target.value)}
                          className="input w-full text-right"
                          placeholder="مثال: 0x1234567890abcdef1234567890abcdef1234567890abcdef"
                          required
                          dir="ltr"
                        />
                      </div>
                      <button
                        type="submit"
                        disabled={isVerifying}
                        className="btn btn-primary w-full"
                      >
                        {isVerifying ? (
                          <>
                            <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                            در حال تایید...
                          </>
                        ) : (
                          'تایید پرداخت'
                        )}
                      </button>
                    </form>
                  ) : verificationResult.verified ? (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                      <svg className="w-8 h-8 text-green-500 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <p className="text-green-700 font-semibold">پرداخت با موفقیت تایید شد!</p>
                      <p className="text-green-600 text-sm mt-1">در حال انتقال به صفحه تایید...</p>
                    </div>
                  ) : (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
                      <svg className="w-8 h-8 text-red-500 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                      <p className="text-red-700 font-semibold">تایید پرداخت ناموفق بود</p>
                      <p className="text-red-600 text-sm mt-1">لطفاً شماره تراکنش را بررسی کنید</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="zarinpal-payment text-center">
                  <h3 className="text-lg font-semibold mb-4 text-right">پرداخت با زرین‌پال</h3>
                  <p className="text-gray-600 mb-6 text-right">
                    شما به درگاه پرداخت زرین‌پال هدایت خواهید شد.
                  </p>
                  <a
                    href={paymentDetails.payment_url}
                    className="btn btn-primary btn-lg inline-flex items-center"
                  >
                    <span>رفتن به درگاه پرداخت زرین‌پال</span>
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                  
                  {/* Zarinpal test info */}
                  <div className="bg-blue-50 rounded-lg p-4 mt-6 text-right">
                    <p className="font-semibold mb-2">اطلاعات تست زرین‌پال (Sandbox):</p>
                    <p className="text-sm text-gray-600">
                      کارت تست موفق: <span className="font-mono">6037-6991-1289-4956</span>
                    </p>
                    <p className="text-sm text-gray-600">
                      CVV2: <span className="font-mono">1234</span>
                    </p>
                    <p className="text-sm text-gray-600">
                      تاریخ انقضا: <span className="font-mono">01/30</span>
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Help Section */}
        <div className="mt-8 bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4 text-right">نیاز به کمک دارید؟</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-right">
            <div>
              <p className="text-sm text-gray-600 mb-1">پشتیبانی تلگرام:</p>
              <p className="font-mono">@aisubscription_support</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">ایمیل:</p>
              <p className="font-mono">support@yourdomain.ir</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">تلفن:</p>
              <p className="font-mono">021-12345678</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
