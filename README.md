# AI Subscription Platform 🚀

> **پلتفرم فروش اشتراک‌ها و APIهای هوش مصنوعی با قیمت‌های تخفیف‌دار**
> **Fully Automated with AI Agents | On-Demand Purchasing | Real-time Pricing**

---

## 📌 ویژگی‌های کلیدی

✅ **خرید به سفارش (On-Demand)** - فقط وقتی مشتری سفارش داد، خرید انجام می‌شود
✅ **محاسبه لحظه‌ای قیمت‌ها** - قیمت‌ها بر اساس نرخ واقعی تتر (USDT) به‌روزرسانی می‌شوند
✅ **AI Agents هوشمند** - اتوماسیون کامل خرید، تحویل و محاسبه قیمت‌ها
✅ **اکانت‌های اشتراکی** - گزینه‌های ارزان برای کاربران معمولی
✅ **پشتیبانی از سایت‌های خارجی** - تامین از GGSel, FunPay, Oyunfor, Kie.ai, ShareTool
✅ **پرداخت با کریپتو** - پشتیبانی از USDT, BTC, ETH (شبکه TRC20 پیش‌فرض)
✅ **حاشیه سود پویا** - قیمت‌گذاری هوشمند برای رقابت‌پذیری

---

## 🏗️ معماری پروژه

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Subscription Platform                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌───────────────────┐  │
│  │   Frontend   │    │   Backend    │    │    AI Agents      │  │
│  │  (Next.js)   │───▶│ (FastAPI)    │───▶│  (Pricing, Proc., │  │
│  └─────────────┘    └─────────────┘    │    Delivery, etc.) │  │
│                                          └──────────┬─────────┘  │
│                                                     │              │
│  ┌─────────────┐    ┌─────────────┐    ┌───────────▼───────┐  │
│  │   User       │───▶│   Order      │───▶│ External APIs    │  │
│  └─────────────┘    └─────────────┘    │ (GGSel, Oyunfor,  │  │
│                                          │  Kie.ai, etc.)     │  │
│                                          └───────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 ساختار پروژه

```
ai-subscription-platform/
├── backend/                          # Backend (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI Application
│   │   ├── config.py                 # تنظیمات
│   │   ├── database.py               # تنظیمات دیتابیس
│   │   │
│   │   ├── agents/                   # 🤖 AI Agents
│   │   │   ├── pricing_agent.py      # محاسبه قیمت‌ها
│   │   │   ├── procurement_agent.py # خرید خودکار
│   │   │   ├── delivery_agent.py     # تحویل خودکار
│   │   │   └── monitoring_agent.py   # مانیتورینگ
│   │   │
│   │   ├── models/                   # 🗃️ مدل‌های دیتابیس
│   │   │   └── models.py
│   │   │
│   │   ├── schemas/                  # 📜 Pydantic Schemas
│   │   │   └── schemas.py
│   │   │
│   │   ├── services/                 # 🔧 سرویس‌ها
│   │   │   ├── product_service.py
│   │   │   ├── order_service.py
│   │   │   └── payment_service.py
│   │   │
│   │   ├── utils/                    # 🔨 ابزارها
│   │   │   ├── exchange_rate.py      # نرخ لحظه‌ای تتر
│   │   │   ├── crypto_utils.py       # ابزارهای کریپتو
│   │   │   └── external_apis.py      # API سایت‌های خارجی
│   │   │
│   │   └── tasks.py                  # Celery Tasks
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                         # Frontend (Next.js)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
│
├── docker/                          # Docker Configs
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── conf.d/
│   │       └── default.conf
│   └── docker-compose.yml
│
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🚀 شروع سریع

### ✅ پیش‌نیازها

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Redis (برای Celery)
- Git

### 📥 نصب و راه‌اندازی

#### ۱. کلون کردن ریپازیتوری

```bash
git clone https://github.com/maryamghabel3-debug/ai-subscription-platform.git
cd ai-subscription-platform
```

#### ۲. تنظیم متغیرهای محیطی

```bash
# کپی فایل نمونه
cp backend/.env.example backend/.env

# ویرایش فایل .env و وارد کردن اطلاعات خود
nano backend/.env
```

**متغیرهای مهم:**
- `GGSEL_USERNAME`, `GGSEL_PASSWORD` - اطلاعات ورود به GGSel
- `FUNPAY_USERNAME`, `FUNPAY_PASSWORD` - اطلاعات ورود به FunPay
- `OYUNFOR_USERNAME`, `OYUNFOR_PASSWORD` - اطلاعات ورود به Oyunfor
- `KIE_AI_API_KEY` - API Key سایت Kie.ai
- `CRYPTO_PAYMENT_ADDRESS` - آدرس کیف پول برای دریافت پرداخت‌ها
- `SMTP_*` - تنظیمات ایمیل برای ارسال اطلاعیه‌ها

#### ۳. نصب وابستگی‌ها

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # در ویندوز: venv\Scripts\activate
pip install -r requirements.txt
cd ..

# Frontend (اختیاری - اگر می‌خواهید Frontend را هم اجرا کنید)
cd frontend
npm install
cd ..
```

#### ۴. ایجاد دیتابیس

```bash
cd backend
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
cd ..
```

#### ۵. اجرا با Docker (پیشنهادی)

```bash
# ساخت و اجرا
sudo docker-compose up -d --build

# مشاهده لاگ‌ها
sudo docker-compose logs -f backend
```

سایت در آدرس **http://localhost** در دسترس خواهد بود.

#### ۶. اجرا بدون Docker (برای توسعه)

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (در ترمینال دیگری)
cd frontend
npm run dev
```

- Backend: **http://localhost:8000**
- Frontend: **http://localhost:3000**

---

## 🤖 AI Agents

### 1. **Pricing Agent** (`backend/app/agents/pricing_agent.py`)
- **وظیفه:** محاسبه هوشمند قیمت‌ها
- **ویژگی‌ها:**
  - دریافت قیمت پایه از سایت‌های خارجی
  - محاسبه قیمت‌ها بر اساس نرخ لحظه‌ای تتر
  - اعمال حاشیه سود پویا (بر اساس قیمت‌های رقبا)
  - بهینه‌سازی قیمت‌ها برای رقابت‌پذیری

### 2. **Procurement Agent** (`backend/app/agents/procurement_agent.py`)
- **وظیفه:** خرید خودکار از سایت‌های خارجی
- **ویژگی‌ها:**
  - خرید اکانت/API از GGSel, FunPay, Oyunfor, Kie.ai, ShareTool
  - مدیریت سفارش‌ها
  - ثبت لاگ خریدها
  - پشتیبانی از خرید عمده (در آینده)

### 3. **Delivery Agent** (`backend/app/agents/delivery_agent.py`)
- **وظیفه:** تحویل خودکار اکانت‌ها به مشتریان
- **ویژگی‌ها:**
  - ارسال ایمیل با اطلاعات اکانت
  - ارسال SMS (در آینده)
  - ذخیره اطلاعات در پروفایل کاربر

### 4. **Monitoring Agent** (`backend/app/agents/monitoring_agent.py`)
- **وظیفه:** مانیتورینگ سیستم
- **ویژگی‌ها:**
  - بررسی سلامت سیستم
  - رصد خطاهای خرید
  - بررسی موجودی اکانت‌های اشتراکی
  - ارسال هشدارها

---

## 🔌 API Endpoints

### 📊 Exchange Rate
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/exchange-rate` | دریافت نرخ لحظه‌ای تتر |
| GET | `/api/exchange-rates` | دریافت تمام نرخ‌های ارز |

### 📦 Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | دریافت تمام محصولات |
| GET | `/api/products/{id}` | دریافت یک محصول خاص |
| GET | `/api/products/prices` | دریافت قیمت‌های محاسبه شده تمام محصولات |
| POST | `/api/products/calculate-price` | محاسبه قیمت برای یک محصول |

### 🛒 Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orders/` | ایجاد سفارش جدید |
| GET | `/api/orders/{id}` | دریافت جزئیات سفارش |
| POST | `/api/orders/{id}/confirm-payment` | تایید پرداخت کریپتو |
| GET | `/api/orders/{id}/status` | دریافت وضعیت سفارش |

### 👥 Shared Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/shared-accounts/` | ایجاد اکانت‌های اشتراکی جدید |
| GET | `/api/shared-accounts/{id}` | دریافت اطلاعات اکانت اشتراکی |

### 🔐 Admin (نیاز به احراز هویت)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/admin/products/` | ایجاد محصول جدید |
| POST | `/api/admin/competitor-prices/` | اضافه کردن قیمت رقیب |

---

## 💰 قیمت‌گذاری هوشمند

سیستم قیمت‌گذاری این پلتفرم **به صورت کاملا خودکار** و **هوشمند** عمل می‌کند:

1. **دریافت نرخ لحظه‌ای تتر** از سایت‌های ایرانی (بیت‌پین، نوبیتکس، والکس)
2. **محاسبه قیمت پایه تومانی** بر اساس قیمت دلاری محصول
3. **اعمال حاشیه سود پویا** بر اساس:
   - قیمت‌های رقبا (سایت‌های ایرانی)
   - دسته‌بندی محصول
   - نوع محصول
4. **اضافه کردن کارمزد پرداخت** (۱% پیش‌فرض)
5. **بهینه‌سازی قیمت نهایی** برای:
   - تضمین سودآوری
   - رقابت‌پذیری

### مثال محاسبه قیمت:

```
محصول: ChatGPT Plus
قیمت پایه دلاری: $7
نرخ تتر: ۱۹۰،۰۰۰ تومان
قیمت پایه تومانی: ۷ × ۱۹۰،۰۰۰ = ۱،۳۳۰،۰۰۰ تومان

قیمت رقبا (میانگین): ۱،۹۷۵،۰۰۰ تومان
حاشیه سود پویا: ۴۳.۵% (برای رقابت‌پذیری)
قیمت قبل از کارمزد: ۱،۳۳۰،۰۰۰ × ۱.۴۳۵ = ۱،۹۰۷،۵۵۰ تومان
کارمزد پرداخت (۱%): ۱۹،۰۷۵ تومان

قیمت نهایی: ۱،۹۰۷،۵۵۰ + ۱۹،۰۷۵ = ۱،۹۲۶،۶۲۵ تومان ≈ ۱،۹۲۷،۰۰۰ تومان
```

---

## 🌍 سایت‌های تامین کننده

پلتفرم از سایت‌های خارجی زیر برای تامین اکانت‌ها و APIها استفاده می‌کند:

| سایت | لینک | محصولات | تخفیف |
|------|------|----------|--------|
| GGSel | [ggsel.net](https://ggsel.net) | اکانت‌های هوش مصنوعی | ۶۰-۹۰% |
| FunPay | [funpay.com](https://funpay.com) | اکانت‌های هوش مصنوعی | ۵۰-۸۰% |
| Oyunfor | [oyunfor.com](https://www.oyunfor.com) | گیفت کارت ترکیه | ۹۰%+ |
| Kie.ai | [kie.ai](https://kie.ai) | اعتبار API | ۲۰-۸۶% |
| ShareTool | [sharetool.net](https://sharetool.net) | اکانت‌های اشتراکی | ۹۵-۹۹% |

---

## 📊 محصولات پشتیبانی شده

### 💬 چت و متن (Chat & Text AI)
- ChatGPT Plus
- Claude Pro/Max
- Grok (xAI)
- Gemini Advanced
- Mistral AI

### 🎨 ساخت عکس (Image Generation AI)
- Midjourney (Basic/Standard/Pro)
- DALL-E 3
- Stable Diffusion
- Leonardo.AI
- Ideogram

### 🎬 ساخت ویدیو (Video Generation AI)
- Runway ML
- Pika Labs
- Sora
- Kling AI
- Veo

### 💻 کد نویسی (Coding AI)
- GitHub Copilot
- Cursor AI
- Tabnine

### 🎵 موسیقی (Audio AI)
- Suno AI
- Udio
- ElevenLabs

### 🌐 همه در یک جا (All-in-One)
- Unified AI Hub
- Cabina.AI
- Krater.ai

---

## 🛡️ امنیت

- **حفظ اطلاعات کاربر** - اطلاعات کاربران به صورت ایمن ذخیره می‌شوند
- **پرداخت‌های ایمن** - استفاده از شبکه TRC20 برای کارمزد پایین
- **اکانت‌های معتبر** - خرید از سایت‌های معتبر خارجی
- **گارانتی** - گارانتی تا پایان دوره اشتراک

---

## 📈 مقیاس‌پذیری

پلتفرم برای **مقیاس‌پذیری بالا** طراحی شده است:

- **Docker Containerization** - اجرا در هر محیطی
- **Celery Tasks** - پردازش پس‌زمینه سفارش‌ها
- **Redis Cache** - ذخیره موقت اطلاعات
- **Load Balancing** - آماده برای ترافیک بالا

---

## 🤝 همکاری

برای همکاری در توسعه این پروژه:

1. ریپازیتوری را Fork کنید
2. یک Branch جدید ایجاد کنید (`git checkout -b feature/your-feature`)
3. تغییرات خود را Commit کنید (`git commit -m 'Add some feature'`)
4. به Branch اصلی Push کنید (`git push origin feature/your-feature`)
5. Pull Request ایجاد کنید

---

## 📜 مجوز

این پروژه تحت **مجوز MIT** منتشر شده است. برای اطلاعات بیشتر، فایل [LICENSE](LICENSE) را مشاهده کنید.

---

## 💬 تماس

برای سوالات و پیشنهادات:
- ایمیل: support@yoursite.com
- تلگرام: @yoursite

---

**✨ با استفاده از این پلتفرم، می‌توانید تمام ابزارهای هوش مصنوعی را با تخفیف ۵۰% تا ۹۹% خریداری کنید!**

**🚀 اولین خرید خود را امروز انجام دهید!**
