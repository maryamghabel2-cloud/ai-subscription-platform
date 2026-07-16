import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import axios from 'axios';

// Icon components (simple SVG icons)
const SparklesIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
  </svg>
);

const ClockIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const ShieldCheckIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
  </svg>
);

const LightningBoltIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
  </svg>
);

const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price);
};

const calculateDiscount = (ourPrice, competitorPrice) => {
  if (!competitorPrice || competitorPrice === 0) return 0;
  return Math.round(((competitorPrice - ourPrice) / competitorPrice) * 100);
};

export default function Home({ usdtRate, loadingRate }) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Categories
  const categories = [
    { id: 'all', name: 'همه محصولات', icon: '🌐' },
    { id: 'chat', name: 'چت و متن', icon: '💬' },
    { id: 'image', name: 'ساخت عکس', icon: '🎨' },
    { id: 'video', name: 'ساخت ویدیو', icon: '🎬' },
    { id: 'coding', name: 'کد نویسی', icon: '💻' },
    { id: 'music', name: 'موسیقی', icon: '🎵' },
    { id: 'subscription', name: 'اشتراک‌ها', icon: '📺' },
    { id: 'api', name: 'APIها', icon: '🔌' },
    { id: 'shared', name: 'اشتراکی', icon: '👥' }
  ];

  // Fetch products
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/products/prices');
        setProducts(response.data.prices || []);
        setError(null);
      } catch (err) {
        console.error('Error fetching products:', err);
        setError('خطا در دریافت محصولات. لطفاً بعداً امتحان کنید.');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();

    // Refresh every 30 seconds
    const interval = setInterval(fetchProducts, 30000);
    return () => clearInterval(interval);
  }, []);

  // Filter products by category
  const filteredProducts = selectedCategory === 'all' 
    ? products 
    : products.filter(p => p.category === selectedCategory);

  // Featured products
  const featuredProducts = products.filter(p => 
    ['chatgpt_plus', 'midjourney_basic', 'netflix_turkey', 'gpt4_api'].includes(p.product_name.replace(/\s+/g, '_').toLowerCase())
  );

  if (loading && !products.length) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Head>
          <title>در حال بارگذاری... | AI Subscription Platform</title>
        </Head>
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">در حال دریافت اطلاعات...</p>
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
          <button 
            onClick={() => window.location.reload()}
            className="btn btn-primary"
          >
            تلاش مجدد
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>AI Subscription Platform - خرید اشتراک‌های هوش مصنوعی</title>
        <meta name="description" content="خرید اشتراک‌های نتفلیکس، اسپاتیفای، چت‌جی‌پی‌تی، میدجورنی و APIهای هوش مصنوعی با قیمت‌های تخفیف‌دار" />
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

            {/* Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              <Link href="/#products" className="text-gray-600 hover:text-primary transition-colors">
                محصولات
              </Link>
              <Link href="/#pricing" className="text-gray-600 hover:text-primary transition-colors">
                قیمت‌ها
              </Link>
              <Link href="/#how-it-works" className="text-gray-600 hover:text-primary transition-colors">
                چگونه کار می‌کند؟
              </Link>
              <Link href="/#contact" className="text-gray-600 hover:text-primary transition-colors">
                تماس با ما
              </Link>
            </nav>

            {/* User Actions */}
            <div className="flex items-center space-x-4">
              <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-600">
                <span>نرخ تتر:</span>
                <span className="font-bold text-primary">{formatPrice(usdtRate)} تومان</span>
              </div>
              <Link href="/login" className="btn btn-outline hidden sm:inline-flex">
                ورود
              </Link>
              <Link href="/register" className="btn btn-primary hidden sm:inline-flex">
                ثبت‌نام
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main>
        {/* Hero Section */}
        <section className="bg-gradient-to-r from-primary to-secondary text-white py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div>
                <h1 className="text-4xl md:text-5xl font-bold mb-6">
                  خرید اشتراک‌های هوش مصنوعی
                  <br />
                  <span className="text-yellow-300">با تخفیف ۵۰% تا ۹۹%</span>
                </h1>
                <p className="text-xl mb-8 text-blue-100">
                  با استفاده از پلتفرم ما، می‌توانید تمام ابزارهای هوش مصنوعی را با
                  قیمت‌های بسیار پایین‌تر از سایت‌های اصلی خریداری کنید.
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <Link href="#products" className="btn btn-secondary">
                    مشاهده محصولات
                  </Link>
                  <Link href="/#how-it-works" className="btn btn-outline text-white border-white hover:bg-white hover:text-primary">
                    چگونه کار می‌کند؟
                  </Link>
                </div>
              </div>
              <div className="hidden lg:block">
                <div className="relative">
                  <div className="absolute inset-0 bg-primary rounded-2xl transform rotate-6 shadow-2xl"></div>
                  <div className="relative bg-white rounded-2xl p-6 shadow-2xl">
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <span className="text-gray-600">ChatGPT Plus</span>
                        <span className="font-bold text-green-600">۱،۹۰۰،۰۰۰ تومان</span>
                      </div>
                      <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <span className="text-gray-600">Midjourney</span>
                        <span className="font-bold text-green-600">۱،۰۰۰،۰۰۰ تومان</span>
                      </div>
                      <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <span className="text-gray-600">Netflix</span>
                        <span className="font-bold text-green-600">۴۰۰،۰۰۰ تومان</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-dark-color mb-4">
                چرا ما را انتخاب کنید؟
              </h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                پلتفرم ما با ویژگی‌های منحصر به فرد خود، بهترین گزینه برای خرید اشتراک‌های هوش مصنوعی است.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {/* Feature 1 */}
              <div className="card p-6">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <LightningBoltIcon className="w-6 h-6 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">خرید به سفارش</h3>
                <p className="text-gray-600 text-sm">
                  فقط وقتی مشتری سفارش داد، خرید انجام می‌شود. هیچ موجودی اضافی و ریسک مالی نیست.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="card p-6">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                  <ClockIcon className="w-6 h-6 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">قیمت‌های لحظه‌ای</h3>
                <p className="text-gray-600 text-sm">
                  قیمت‌ها بر اساس نرخ واقعی تتر به صورت لحظه‌ای محاسبه و به‌روزرسانی می‌شوند.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="card p-6">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                  <SparklesIcon className="w-6 h-6 text-purple-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">اتوماسیون کامل</h3>
                <p className="text-gray-600 text-sm">
                  تمام فرآیندها از سفارش تا تحویل به صورت خودکار توسط AI Agents انجام می‌شوند.
                </p>
              </div>

              {/* Feature 4 */}
              <div className="card p-6">
                <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
                  <ShieldCheckIcon className="w-6 h-6 text-orange-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">امنیت و گارانتی</h3>
                <p className="text-gray-600 text-sm">
                  خرید از سایت‌های معتبر خارجی با گارانتی و پشتیبانی کامل.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Featured Products Section */}
        <section id="products" className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-dark-color mb-4">
                محصولات پرطرفدار
              </h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                محبوب‌ترین محصولات با بهترین قیمت‌ها
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {featuredProducts.map((product) => (
                <div key={product.product_name} className="card group">
                  <div className="p-4">
                    {/* Product Image */}
                    <div className="aspect-w-16 aspect-h-12 mb-4">
                      <div className="bg-gray-100 rounded-lg h-48 flex items-center justify-center">
                        {product.image_url ? (
                          <img 
                            src={product.image_url} 
                            alt={product.product_name}
                            className="w-full h-full object-cover rounded-lg"
                          />
                        ) : (
                          <div className="w-16 h-16 bg-primary rounded-lg flex items-center justify-center">
                            <SparklesIcon className="w-8 h-8 text-white" />
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Product Info */}
                    <div className="px-4 pb-4">
                      <h3 className="font-semibold text-lg mb-2">{product.product_name}</h3>
                      
                      {/* Category Badge */}
                      <div className="flex items-center space-x-2 mb-3">
                        <span className="badge badge-info">
                          {categories.find(c => c.id === product.category)?.name || product.category}
                        </span>
                        {product.product_type === 'shared' && (
                          <span className="badge badge-warning">اشتراکی</span>
                        )}
                      </div>

                      {/* Price */}
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <p className="price text-2xl font-bold text-primary">
                            {formatPrice(product.final_price)} تومان
                          </p>
                          {product.competitor_average_price && (
                            <p className="old-price">
                              {formatPrice(product.competitor_average_price)} تومان
                            </p>
                          )}
                        </div>
                        <div>
                          {product.competitor_average_price && (
                            <span className="badge badge-success">
                              {calculateDiscount(product.final_price, product.competitor_average_price)}% ارزان‌تر
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Action Button */}
                      <Link 
                        href={`/order?product=${encodeURIComponent(product.product_name)}`}
                        className="btn btn-primary w-full"
                      >
                        خرید
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* All Products Section */}
        <section id="all-products" className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-dark-color mb-4">
                تمام محصولات
              </h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                لیست کامل محصولات با قیمت‌های تخفیف‌دار
              </p>
            </div>

            {/* Category Filter */}
            <div className="flex flex-wrap justify-center gap-2 mb-12">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                    selectedCategory === category.id
                      ? 'bg-primary text-white shadow-md'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {category.icon} {category.name}
                </button>
              ))}
            </div>

            {/* Products Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredProducts.map((product) => (
                <div key={product.product_name} className="card group">
                  <div className="p-4">
                    {/* Product Image */}
                    <div className="aspect-w-16 aspect-h-12 mb-4">
                      <div className="bg-gray-100 rounded-lg h-48 flex items-center justify-center">
                        {product.image_url ? (
                          <img 
                            src={product.image_url} 
                            alt={product.product_name}
                            className="w-full h-full object-cover rounded-lg"
                          />
                        ) : (
                          <div className="w-16 h-16 bg-primary rounded-lg flex items-center justify-center">
                            <SparklesIcon className="w-8 h-8 text-white" />
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Product Info */}
                    <div className="px-4 pb-4">
                      <h3 className="font-semibold text-lg mb-2 line-clamp-1">{product.product_name}</h3>
                      
                      {/* Category Badge */}
                      <div className="flex items-center space-x-2 mb-3">
                        <span className="badge badge-info">
                          {categories.find(c => c.id === product.category)?.name || product.category}
                        </span>
                        {product.product_type === 'shared' && (
                          <span className="badge badge-warning">اشتراکی</span>
                        )}
                      </div>

                      {/* Price */}
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <p className="price text-2xl font-bold text-primary">
                            {formatPrice(product.final_price)} تومان
                          </p>
                          {product.competitor_average_price && (
                            <p className="old-price">
                              {formatPrice(product.competitor_average_price)} تومان
                            </p>
                          )}
                        </div>
                        <div>
                          {product.is_competitive && (
                            <span className="badge badge-success">
                              ارزان‌تر از رقبا
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Action Button */}
                      <Link 
                        href={`/order?product=${encodeURIComponent(product.product_name)}`}
                        className="btn btn-primary w-full"
                      >
                        خرید
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section id="how-it-works" className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-dark-color mb-4">
                چگونه کار می‌کند؟
              </h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                فرآیند خرید در پلتفرم ما بسیار ساده و سریع است
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Step 1 */}
              <div className="card p-6 text-center">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl font-bold text-white">۱</span>
                </div>
                <h3 className="text-xl font-semibold mb-4">انتخاب محصول</h3>
                <p className="text-gray-600">
                  محصول مورد نظر خود را از لیست محصولات انتخاب کنید.
                  قیمت‌ها به صورت لحظه‌ای محاسبه می‌شوند.
                </p>
              </div>

              {/* Step 2 */}
              <div className="card p-6 text-center">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl font-bold text-white">۲</span>
                </div>
                <h3 className="text-xl font-semibold mb-4">پرداخت</h3>
                <p className="text-gray-600">
                  مبلغ را به آدرس کیف پول نمایش داده شده پرداخت کنید.
                  پس از تایید پرداخت، سفارش شما پردازش می‌شود.
                </p>
              </div>

              {/* Step 3 */}
              <div className="card p-6 text-center">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl font-bold text-white">۳</span>
                </div>
                <h3 className="text-xl font-semibold mb-4">دریافت اکانت</h3>
                <p className="text-gray-600">
                  پس از پردازش سفارش، اطلاعات اکانت به صورت خودکار برای شما ارسال می‌شود.
                  می‌توانید بلافاصله از اکانت استفاده کنید.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <section id="pricing" className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-dark-color mb-4">
                قیمت‌ها
              </h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                قیمت‌ها بر اساس نرخ لحظه‌ای تتر محاسبه می‌شوند
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* Pricing Card 1 */}
              <div className="card p-8 text-center">
                <h3 className="text-xl font-bold mb-4">اکانت‌های اختصاصی</h3>
                <p className="text-gray-600 mb-6">
                  اکانت‌های اختصاصی با دسترسی کامل
                </p>
                <ul className="space-y-4 mb-8 text-right">
                  <li className="flex items-center justify-end">
                    <span className="ml-2">دسترسی کامل</span>
                  </li>
                  <li className="flex items-center justify-end">
                    <span className="ml-2">حریم خصوصی کامل</span>
                  </li>
                  <li className="flex items-center justify-end">
                    <span className="ml-2">بدون محدودیت</span>
                  </li>
                  <li className="flex items-center justify-end">
                    <span className="ml-2">گارانتی کامل</span>
                  </li>
                </ul>
                <p className="text-3xl font-bold text-primary mb-6">
                  از ۱،۰۰۰،۰۰۰ تومان
                </p>
                <Link href="#products" className="btn btn-primary w-full">
                  مشاهده محصولات
                </Link>
              </div>

              {/* Pricing Card 2 */}
              <div className="card p-8 text-center border-2 border-primary">
                <div className="bg-primary text-white px-4 py-1 rounded-full text-sm font-medium mb-4">
                  محبوب‌تر
                </div>
                <h3 className="text-xl font-bold mb-4">اکانت‌های اشتراکی</h3>
                <p className="text-gray-600 mb-6">
                  اکانت‌های اشتراکی با قیمت بسیار پایین
                </p>
                <ul className="space-y-4 mb-8 text-right">
                  <li className="flex items-center justify-end">
                    <span className="ml-2">قیمت بسیار پایین</span>
                  </li>
                  <li className="flex items-center justify-end">
                    <span className="ml-2">اعتبار محدود</span>
                  </li>
                  <li className="flex items-center justify-end">
                    <span className="ml-2">مخصوص استفاده معمولی</span>
                  </li>
                  <li className="flex items-center justify-end">
                    <span className="ml-2">تخفیف ۹۰%+</span>
                  </li>
                </ul>
                <p className="text-3xl font-bold text-primary mb-6">
                  از ۲۰۰،۰۰۰ تومان
                </p>
                <Link href="#products" className="btn btn-primary w-full">
                  مشاهده محصولات
                </Link>
              </div>

              {/* Pricing Card 3 */}
              <div className="card p-8 text-center">
                <h3 className="text-xl font-bold mb-4">اعتبار API</h3>
                <p className="text-gray-600 mb-6">
                  اعتبار API برای توسعه‌دهندگان
                </p>
                <ul className="space-y-4 mb-8 text-right">
                  <li className="flex items-center justify-end">
                    <span className="ml-2">پرداخت به ازای استفاده</span>
                  </li>
                  <li className="flex items-center justify-end">
                    <span className="ml-2">بدون محدودیت زمانی</span>
                  </li>
                  <li className="flex items-center justify-end">
                    <span className="ml-2">پشتیبانی از چند مدل</span>
                  </li>
                  <li className="flex items-center justify-end">
                    <span className="ml-2">تخفیف ۲۰-۸۶%</span>
                  </li>
                </ul>
                <p className="text-3xl font-bold text-primary mb-6">
                  از ۱۰،۰۰۰ تومان
                </p>
                <Link href="#products" className="btn btn-primary w-full">
                  مشاهده محصولات
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section id="faq" className="py-20 bg-gray-50">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-dark-color mb-4">
                سوالات متداول
              </h2>
              <p className="text-gray-600">
                پاسخ به سوالات رایج کاربران
              </p>
            </div>

            <div className="space-y-6">
              {/* FAQ Item 1 */}
              <div className="card">
                <button 
                  className="w-full flex items-center justify-between p-6 text-left"
                  onClick={() => {
                    const content = document.getElementById('faq-1');
                    content.classList.toggle('hidden');
                  }}
                >
                  <span className="font-semibold text-lg">چگونه سفارش بدهم؟</span>
                  <svg className="w-6 h-6 transform transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div id="faq-1" className="hidden px-6 pb-6">
                  <p className="text-gray-600">
                    برای سفارش، ابتدا محصول مورد نظر خود را از لیست محصولات انتخاب کنید.
                    سپس روی دکمه "خرید" کلیک کنید. در صفحه بعدی، آدرس کیف پول و مبلغی که
                    باید پرداخت کنید نمایش داده می‌شود. پس از پرداخت، سفارش شما به صورت
                    خودکار پردازش می‌شود.
                  </p>
                </div>
              </div>

              {/* FAQ Item 2 */}
              <div className="card">
                <button 
                  className="w-full flex items-center justify-between p-6 text-left"
                  onClick={() => {
                    const content = document.getElementById('faq-2');
                    content.classList.toggle('hidden');
                  }}
                >
                  <span className="font-semibold text-lg">چه روش‌های پرداختی پشتیبانی می‌شوند؟</span>
                  <svg className="w-6 h-6 transform transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div id="faq-2" className="hidden px-6 pb-6">
                  <p className="text-gray-600">
                    در حال حاضر، تنها پرداخت با ارزهای دیجیتال (کریپتو) پشتیبانی می‌شود.
                    شما می‌توانید از USDT (شبکه TRC20)، BTC، ETH و سایر ارزهای دیجیتال
                    استفاده کنید. آدرس کیف پول و مبلغ دقیق در صفحه پرداخت نمایش داده می‌شود.
                  </p>
                </div>
              </div>

              {/* FAQ Item 3 */}
              <div className="card">
                <button 
                  className="w-full flex items-center justify-between p-6 text-left"
                  onClick={() => {
                    const content = document.getElementById('faq-3');
                    content.classList.toggle('hidden');
                  }}
                >
                  <span className="font-semibold text-lg">اکانت‌ها چقدر طول می‌کشند تا تحویل شوند؟</span>
                  <svg className="w-6 h-6 transform transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div id="faq-3" className="hidden px-6 pb-6">
                  <p className="text-gray-600">
                    اکثر سفارش‌ها در کمتر از ۱ ساعت تحویل می‌شوند. سفارش‌های اکانت‌های اشتراکی
                    به صورت فوری تحویل می‌شوند. در موارد نادر، اگر سایت تامین کننده دچار مشکل
                    باشد، تحویل ممکن است تا ۲۴ ساعت طول بکشد.
                  </p>
                </div>
              </div>

              {/* FAQ Item 4 */}
              <div className="card">
                <button 
                  className="w-full flex items-center justify-between p-6 text-left"
                  onClick={() => {
                    const content = document.getElementById('faq-4');
                    content.classList.toggle('hidden');
                  }}
                >
                  <span className="font-semibold text-lg">آیا اکانت‌ها قانونی هستند؟</span>
                  <svg className="w-6 h-6 transform transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div id="faq-4" className="hidden px-6 pb-6">
                  <p className="text-gray-600">
                    بله، تمام اکانت‌ها از سایت‌های معتبر خارجی خریداری می‌شوند و کاملا قانونی هستند.
                    اکانت‌های اختصاصی به صورت کامل در اختیار شما قرار می‌گیرند و می‌توانید آنها
                    را روی ایمیل شخصی خود فعال کنید.
                  </p>
                </div>
              </div>

              {/* FAQ Item 5 */}
              <div className="card">
                <button 
                  className="w-full flex items-center justify-between p-6 text-left"
                  onClick={() => {
                    const content = document.getElementById('faq-5');
                    content.classList.toggle('hidden');
                  }}
                >
                  <span className="font-semibold text-lg">تفاوت اکانت اختصاصی و اشتراکی چیست؟</span>
                  <svg className="w-6 h-6 transform transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div id="faq-5" className="hidden px-6 pb-6">
                  <p className="text-gray-600">
                    اکانت‌های اختصاصی به صورت کامل در اختیار شما قرار می‌گیرند و هیچ کس دیگری
                    به آنها دسترسی ندارد. اکانت‌های اشتراکی بین چندین کاربر تقسیم می‌شوند
                    و هر کاربر اعتبار محدودی دارد. اکانت‌های اشتراکی بسیار ارزان‌تر هستند
                    ولی ممکن است در زمان‌های پرترافیک سرعت پایین‌تری داشته باشند.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section id="contact" className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-dark-color mb-4">
                تماس با ما
              </h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                برای سوالات و پیشنهادات با ما تماس بگیرید
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Contact Card 1 */}
              <div className="card p-6 text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">ایمیل</h3>
                <p className="text-gray-600 mb-4">support@yoursite.com</p>
                <p className="text-sm text-gray-500">پاسخگویی در کمتر از ۲۴ ساعت</p>
              </div>

              {/* Contact Card 2 */}
              <div className="card p-6 text-center">
                <div className="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">چت آنلاین</h3>
                <p className="text-gray-600 mb-4">تلگرام</p>
                <p className="text-sm text-gray-500">@yoursite_support</p>
              </div>

              {/* Contact Card 3 */}
              <div className="card p-6 text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">آدرس</h3>
                <p className="text-gray-600 mb-4">تهران، ایران</p>
                <p className="text-sm text-gray-500">ساعت کاری: ۹:۰۰ تا ۱۸:۰۰</p>
              </div>
            </div>
          </div>
        </section>

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
      </main>
    </div>
  );
}
