import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';

const ServerErrorIcon = () => (
  <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
  </svg>
);

export default function ServerErrorPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to home after 10 seconds
    const timer = setTimeout(() => {
      router.push('/');
    }, 10000);
    return () => clearTimeout(timer);
  }, [router]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Head>
        <title>خطای سرور | AI Subscription Platform</title>
        <meta name="description" content="خطای سرور رخ داده است" />
      </Head>

      <div className="text-center">
        <div className="bg-white rounded-2xl shadow-lg p-12 max-w-md mx-auto">
          <ServerErrorIcon className="text-red-500 mx-auto mb-6" />
          
          <h1 className="text-4xl font-bold text-gray-900 mb-4">۵۰۰</h1>
          
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            خطای سرور
          </h2>
          
          <p className="text-gray-500 mb-8">
            متاسفانه خطایی در سرور رخ داده است. لطفاً بعداً مجدداً امتحان کنید.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/" className="btn btn-primary">
              بازگشت به صفحه اصلی
            </Link>
            <button 
              onClick={() => router.reload()}
              className="btn btn-outline"
            >
              بارگذاری مجدد
            </button>
          </div>
          
          <p className="text-xs text-gray-400 mt-6">
            شما پس از ۱۰ ثانیه به صورت خودکار به صفحه اصلی هدایت می‌شوید...
          </p>
        </div>
      </div>
    </div>
  );
}
