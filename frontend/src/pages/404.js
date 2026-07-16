import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';

const AlertIcon = () => (
  <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
  </svg>
);

export default function NotFoundPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to home after 5 seconds
    const timer = setTimeout(() => {
      router.push('/');
    }, 5000);
    return () => clearTimeout(timer);
  }, [router]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Head>
        <title>صفحه یافت نشد | AI Subscription Platform</title>
        <meta name="description" content="صفحه مورد نظر یافت نشد" />
      </Head>

      <div className="text-center">
        <div className="bg-white rounded-2xl shadow-lg p-12 max-w-md mx-auto">
          <AlertIcon className="text-red-500 mx-auto mb-6" />
          
          <h1 className="text-4xl font-bold text-gray-900 mb-4">۴۰۴</h1>
          
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            صفحه یافت نشد
          </h2>
          
          <p className="text-gray-500 mb-8">
            متاسفانه صفحه‌ای که به دنبال آن هستید یافت نشد.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/" className="btn btn-primary">
              بازگشت به صفحه اصلی
            </Link>
            <button 
              onClick={() => router.back()}
              className="btn btn-outline"
            >
              بازگشت به صفحه قبل
            </button>
          </div>
          
          <p className="text-xs text-gray-400 mt-6">
            شما پس از ۵ ثانیه به صورت خودکار به صفحه اصلی هدایت می‌شوید...
          </p>
        </div>
      </div>
    </div>
  );
}
