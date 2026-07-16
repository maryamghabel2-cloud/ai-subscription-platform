import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Head from 'next/head';

const SparklesIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
  </svg>
);

const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price);
};

export default function Layout({ children, usdtRate, loadingRate }) {
  const router = useRouter();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <>
      <Head>
        <title>AI Subscription Platform</title>
        <meta name="description" content="خرید اشتراک‌های هوش مصنوعی با قیمت‌های تخفیف‌دار" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center">
              <Link href="/" className="flex items-center space-x-2">
                <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                  <SparklesIcon className="text-white" />
                </div>
                <span className="text-xl font-bold text-dark-color">AI Subscription</span>
              </Link>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              <Link 
                href="/"
                className={`text-gray-600 hover:text-primary transition-colors ${
                  router.pathname === '/' ? 'text-primary font-medium' : ''
                }`}
              >
                صفحه اصلی
              </Link>
              <Link 
                href="#products"
                className="text-gray-600 hover:text-primary transition-colors"
              >
                محصولات
              </Link>
              <Link 
                href="#pricing"
                className="text-gray-600 hover:text-primary transition-colors"
              >
                قیمت‌ها
              </Link>
              <Link 
                href="#how-it-works"
                className="text-gray-600 hover:text-primary transition-colors"
              >
                چگونه کار می‌کند؟
              </Link>
              <Link 
                href="#contact"
                className="text-gray-600 hover:text-primary transition-colors"
              >
                تماس با ما
              </Link>
            </nav>

            {/* Right side */}
            <div className="flex items-center space-x-4">
              {!loadingRate && (
                <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-600">
                  <span>نرخ تتر:</span>
                  <span className="font-bold text-primary">{formatPrice(usdtRate)} تومان</span>
                </div>
              )}
              <Link href="/login" className="btn btn-outline hidden sm:inline-flex">
                ورود
              </Link>
              <Link href="/register" className="btn btn-primary hidden sm:inline-flex">
                ثبت‌نام
              </Link>
              
              {/* Mobile menu button */}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2 rounded-md text-gray-600 hover:text-primary hover:bg-gray-100"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-white border-t">
            <div className="px-4 py-3 space-y-2">
              <Link 
                href="/"
                className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                onClick={() => setMobileMenuOpen(false)}
              >
                صفحه اصلی
              </Link>
              <Link 
                href="#products"
                className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                onClick={() => setMobileMenuOpen(false)}
              >
                محصولات
              </Link>
              <Link 
                href="#pricing"
                className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                onClick={() => setMobileMenuOpen(false)}
              >
                قیمت‌ها
              </Link>
              <Link 
                href="#how-it-works"
                className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                onClick={() => setMobileMenuOpen(false)}
              >
                چگونه کار می‌کند؟
              </Link>
              <Link 
                href="#contact"
                className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                onClick={() => setMobileMenuOpen(false)}
              >
                تماس با ما
              </Link>
              <div className="border-t pt-3 space-y-2">
                <Link 
                  href="/login"
                  className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  ورود
                </Link>
                <Link 
                  href="/register"
                  className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  ثبت‌نام
                </Link>
              </div>
            </div>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main>{children}</main>

      {/* Footer */}
      <footer className="bg-dark-color text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Column 1 */}
            <div>
              <h3 className="text-lg font-semibold mb-4">AI Subscription</h3>
              <p className="text-gray-400 text-sm">
                پلتفرم خرید اشتراک‌های هوش مصنوعی با قیمت‌های تخفیف‌دار
              </p>
            </div>

            {/* Column 2 */}
            <div>
              <h3 className="text-lg font-semibold mb-4">محصولات</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link href="#products" className="hover:text-white transition-colors">چت و متن</Link></li>
                <li><Link href="#products" className="hover:text-white transition-colors">ساخت عکس</Link></li>
                <li><Link href="#products" className="hover:text-white transition-colors">ساخت ویدیو</Link></li>
                <li><Link href="#products" className="hover:text-white transition-colors">کد نویسی</Link></li>
                <li><Link href="#products" className="hover:text-white transition-colors">موسیقی</Link></li>
              </ul>
            </div>

            {/* Column 3 */}
            <div>
              <h3 className="text-lg font-semibold mb-4">لینک‌های مفید</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link href="#how-it-works" className="hover:text-white transition-colors">چگونه کار می‌کند؟</Link></li>
                <li><Link href="#pricing" className="hover:text-white transition-colors">قیمت‌ها</Link></li>
                <li><Link href="#faq" className="hover:text-white transition-colors">سوالات متداول</Link></li>
                <li><Link href="#contact" className="hover:text-white transition-colors">تماس با ما</Link></li>
              </ul>
            </div>

            {/* Column 4 */}
            <div>
              <h3 className="text-lg font-semibold mb-4">شبکه‌های اجتماعی</h3>
              <div className="flex space-x-4">
                <Link href="#" className="w-10 h-10 bg-gray-700 rounded-lg flex items-center justify-center hover:bg-primary transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.189 4.217 2.938 5.395-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.622-.695 1.093-1.336 1.542-2.038z" />
                  </svg>
                </Link>
                <Link href="#" className="w-10 h-10 bg-gray-700 rounded-lg flex items-center justify-center hover:bg-primary transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.85s-.011 3.584-.069 4.85c-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07s-3.584-.012-4.85-.07c-3.252-.148-4.771-1.691-4.919-4.919-.058-1.265-.069-1.645-.069-4.85s.011-3.584.069-4.85c.149-3.225 1.664-4.771 4.919-4.919C8.416 2.175 8.796 2.163 12 2.163zm0 1.802C8.845 3.965 8.558 3.977 7.24 4.033c-2.66.12-3.656 1.117-4.35 2.814-.143.428-.227.93-.227 1.463s.084 1.035.227 1.463c.694 1.697 1.69 2.694 4.35 2.814 1.318.058 1.605.07 4.759.07s3.441-.012 4.759-.07c2.66-.12 3.656-1.117 4.35-2.814.143-.428.227-.93.227-1.463s-.084-1.035-.227-1.463c-.694-1.697-1.69-2.694-4.35-2.814C15.442 3.977 15.155 3.965 12 3.965zm0 4.25c-2.328 0-4.22 1.892-4.22 4.22s1.892 4.22 4.22 4.22 4.22-1.892 4.22-4.22-1.892-4.22-4.22-4.22zm0 7.168c-1.705 0-3.086-1.381-3.086-3.086s1.381-3.086 3.086-3.086 3.086 1.381 3.086 3.086-1.381 3.086-3.086 3.086zm5.618-7.22c-.518 0-.938.42-1.158.842l-.286.572-2.202-1.102c-.528-.264-1.055-.264-1.582 0L8.242 9.71l-.286-.572c-.22-.422-.64-.842-1.158-.842-1.036 0-1.898 1.389-1.898 3.086s.862 3.086 1.898 3.086c.518 0 .938-.42 1.158-.842l.286-.572 2.202 1.102c.528.264 1.055.264 1.582 0l2.202-1.102.286.572c.22.422.64.842 1.158.842 1.035 0 1.898-1.389 1.898-3.086s-.863-3.086-1.898-3.086z" />
                  </svg>
                </Link>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-700 mt-12 pt-8 text-center text-sm text-gray-400">
            <p>
              © {new Date().getFullYear()} AI Subscription Platform. تمام حقوق محفوظ است.
            </p>
          </div>
        </div>
      </footer>
    </>
  );
}
