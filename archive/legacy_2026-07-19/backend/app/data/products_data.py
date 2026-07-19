"""
Complete list of AI products with categories, prices, and descriptions
This file contains all available products for the AI Subscription Platform
"""

# ========== CHAT & TEXT AI ==========
CHAT_AI_PRODUCTS = [
    {
        "id": "chatgpt_plus_monthly",
        "name": "ChatGPT Plus (ماهانه)",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "دسترسی به GPT-4 و GPT-4o با سرعت و کیفیت بالا، بدون محدودیت استفاده",
        "base_price_usd": 20.00,
        "discount_percent": 75,
        "supplier": ["ggsel", "funpay"],
        "delivery_time": "1-2 hours",
        "type": "personal",
        "features": ["GPT-4 Access", "GPT-4o Access", "No Usage Limits", "Priority Support"],
        "image_url": "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/OpenAI-logo.png",
        "tags": ["chatgpt", "gpt4", "ai_chat", "premium"],
        "competitor_price_toman": 6000000,
        "is_popular": True,
        "stock_available": True,
        "min_order": 1,
        "max_order": 10
    },
    {
        "id": "chatgpt_plus_3months",
        "name": "ChatGPT Plus (۳ ماهه)",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "اشتراک ۳ ماهه ChatGPT Plus با تخفیف ویژه",
        "base_price_usd": 50.00,
        "discount_percent": 80,
        "supplier": ["ggsel"],
        "delivery_time": "1-2 hours",
        "type": "personal",
        "features": ["3 Months Access", "GPT-4", "GPT-4o", "Cost Effective"],
        "tags": ["chatgpt", "gpt4", "long_term", "discount"],
        "competitor_price_toman": 15000000,
        "is_popular": True
    },
    {
        "id": "chatgpt_plus_yearly",
        "name": "ChatGPT Plus (سالانه)",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "اشتراک یک ساله ChatGPT Plus با بیشترین تخفیف",
        "base_price_usd": 150.00,
        "discount_percent": 85,
        "supplier": ["ggsel"],
        "delivery_time": "2-4 hours",
        "type": "personal",
        "features": ["1 Year Access", "GPT-4", "GPT-4o", "Maximum Discount"],
        "tags": ["chatgpt", "gpt4", "annual", "best_deal"],
        "competitor_price_toman": 45000000
    },
    {
        "id": "claude_3_5_sonnet",
        "name": "Claude 3.5 Sonnet",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "مدل هوش مصنوعی Claude 3.5 Sonnet - قدرتمندترین مدل فعلی Anthropic",
        "base_price_usd": 20.00,
        "discount_percent": 70,
        "supplier": ["ggsel", "sharetool"],
        "delivery_time": "1-3 hours",
        "type": "personal",
        "features": ["200K Context Window", "Advanced Reasoning", "Code Generation", "File Analysis"],
        "image_url": "https://www.anthropic.com/api/_next/image?url=%2Fimages%2Fclaude-3-5-sonnet.png&w=1920&q=75",
        "tags": ["claude", "anthropic", "ai_assistant", "coding"],
        "competitor_price_toman": 7000000,
        "is_popular": True,
        "is_new": True
    },
    {
        "id": "claude_3_haiku",
        "name": "Claude 3 Haiku",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "مدل سریع Claude 3 Haiku - مناسب برای چت‌های روزمره",
        "base_price_usd": 5.00,
        "discount_percent": 65,
        "supplier": ["ggsel"],
        "delivery_time": "30 min - 1 hour",
        "type": "personal",
        "features": ["Fast Response", "Everyday Use", "Cost Effective"],
        "tags": ["claude", "fast", "budget"],
        "competitor_price_toman": 2000000
    },
    {
        "id": "claude_3_opus",
        "name": "Claude 3 Opus",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "قدرت‌مندترین مدل Claude 3 - برای کارهای حرفه‌ای و پیچیده",
        "base_price_usd": 50.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "2-4 hours",
        "type": "personal",
        "features": ["Most Powerful", "Complex Tasks", "Enterprise Grade"],
        "tags": ["claude", "opus", "premium", "enterprise"],
        "competitor_price_toman": 18000000,
        "is_popular": True
    },
    {
        "id": "gpt5_6",
        "name": "GPT-5.6 (Access)",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "دسترسی به جدیدترین مدل OpenAI - GPT-5.6 با قابلیت‌های بی‌نظیر",
        "base_price_usd": 30.00,
        "discount_percent": 80,
        "supplier": ["ggsel", "oyunfor"],
        "delivery_time": "1-2 hours",
        "type": "personal",
        "features": ["Latest GPT Model", "Multimodal", "Advanced Capabilities"],
        "image_url": "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/OpenAI-logo.png",
        "tags": ["gpt5", "openai", "latest", "multimodal"],
        "competitor_price_toman": 12000000,
        "is_popular": True,
        "is_new": True
    },
    {
        "id": "gpt4_o",
        "name": "GPT-4o (Omni)",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "مدل چندوجهی OpenAI - پشتیبانی از متن، تصویر، صدا و ویدیو",
        "base_price_usd": 15.00,
        "discount_percent": 70,
        "supplier": ["ggsel", "funpay"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["Multimodal", "Text + Image + Audio", "Real-time Processing"],
        "tags": ["gpt4o", "multimodal", "openai", "omni"],
        "competitor_price_toman": 5000000,
        "is_popular": True
    },
    {
        "id": "gpt4_turbo",
        "name": "GPT-4 Turbo",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "نسخه سریع‌تر GPT-4 با هزینه کمتر و کارایی بیشتر",
        "base_price_usd": 10.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["Faster Responses", "Lower Cost", "128K Context"],
        "tags": ["gpt4", "turbo", "fast", "cost_effective"]
    },
    {
        "id": "gpt4_32k",
        "name": "GPT-4 32K Context",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "GPT-4 با حافظه ۳۲ هزار توکن - مناسب برای متن‌های بلند",
        "base_price_usd": 12.00,
        "discount_percent": 70,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["32K Context", "Long Documents", "Detailed Analysis"],
        "tags": ["gpt4", "long_context", "documents"]
    },
    {
        "id": "gemini_ultra",
        "name": "Gemini Ultra",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "قدرت‌مندترین مدل Google Gemini - رقابت مستقیم با GPT-4",
        "base_price_usd": 18.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "1-2 hours",
        "type": "personal",
        "features": ["Google AI", "Multimodal", "Advanced Reasoning"],
        "tags": ["gemini", "google", "ultra", "multimodal"]
    },
    {
        "id": "gemini_pro",
        "name": "Gemini Pro",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "مدل حرفه‌ای Google Gemini - تعادل بین کیفیت و قیمت",
        "base_price_usd": 8.00,
        "discount_percent": 70,
        "supplier": ["ggsel"],
        "delivery_time": "30 min - 1 hour",
        "type": "personal",
        "features": ["Professional Grade", "Cost Effective", "Reliable"],
        "tags": ["gemini", "google", "pro", "reliable"]
    },
    {
        "id": "mistral_ai",
        "name": "Mistral AI",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "مدل هوش مصنوعی اروپایی - باز و قدرتمند",
        "base_price_usd": 5.00,
        "discount_percent": 65,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["Open Source", "European Model", "Privacy Focused"],
        "tags": ["mistral", "open_source", "european", "privacy"]
    },
    {
        "id": "llama_3_70b",
        "name": "Llama 3 70B",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "جدیدترین مدل Meta Llama 3 با ۷۰ میلیارد پارامتر",
        "base_price_usd": 3.00,
        "discount_percent": 60,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["Meta AI", "Open Source", "70B Parameters"],
        "tags": ["llama", "meta", "open_source", "70b"],
        "is_new": True
    },
    {
        "id": "perplexity_pro",
        "name": "Perplexity Pro",
        "category": "chat",
        "subcategory": "text_generation",
        "description": "چت‌بات هوش مصنوعی با قابلیت جستجوی آنلاین و منابع معتبر",
        "base_price_usd": 10.00,
        "discount_percent": 70,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["Online Search", "Cited Sources", "Real-time Information"],
        "tags": ["perplexity", "search", "real_time", "sources"]
    },
]

# ========== IMAGE GENERATION AI ==========
IMAGE_AI_PRODUCTS = [
    {
        "id": "midjourney_v6",
        "name": "Midjourney V6",
        "category": "image",
        "subcategory": "image_generation",
        "description": "جدیدترین نسخه Midjourney - کیفیتی بی‌نظیر در ساخت تصویر",
        "base_price_usd": 10.00,
        "discount_percent": 85,
        "supplier": ["ggsel", "funpay"],
        "delivery_time": "1-2 hours",
        "type": "personal",
        "features": ["V6 Model", "High Quality", "Artistic Styles", "Commercial Use"],
        "image_url": "https://www.midjourney.com/static/images/logo-full.svg",
        "tags": ["midjourney", "v6", "image_generation", "art"],
        "competitor_price_toman": 7000000,
        "is_popular": True,
        "is_new": True
    },
    {
        "id": "midjourney_basic",
        "name": "Midjourney Basic (اشتراکی)",
        "category": "image",
        "subcategory": "image_generation",
        "description": "اشتراک پایه Midjourney - مناسب برای شروع",
        "base_price_usd": 5.42,
        "discount_percent": 90,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "shared",
        "features": ["200 Jobs/Month", "Basic Access", "Community Gallery"],
        "tags": ["midjourney", "basic", "shared", "budget"],
        "competitor_price_toman": 5000000,
        "is_popular": True
    },
    {
        "id": "midjourney_standard",
        "name": "Midjourney Standard (اشتراکی)",
        "category": "image",
        "subcategory": "image_generation",
        "description": "اشتراک استاندارد Midjourney - برای کاربران حرفه‌ای",
        "base_price_usd": 16.34,
        "discount_percent": 85,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "shared",
        "features": ["Unlimited Jobs", "Stealth Mode", "Priority Generation"],
        "tags": ["midjourney", "standard", "unlimited", "priority"],
        "competitor_price_toman": 12000000
    },
    {
        "id": "dalle3",
        "name": "DALL·E 3",
        "category": "image",
        "subcategory": "image_generation",
        "description": "مدل تصویر OpenAI - کیفیت بالا و انطباق عالی با متن",
        "base_price_usd": 0.04,
        "discount_percent": 80,
        "supplier": ["kie.ai", "ggsel"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["High Resolution", "Text-to-Image", "OpenAI Model"],
        "tags": ["dalle3", "openai", "image", "api"],
        "competitor_price_toman": 80000
    },
    {
        "id": "stable_diffusion_xl",
        "name": "Stable Diffusion XL",
        "category": "image",
        "subcategory": "image_generation",
        "description": "مدل باز منبع برای ساخت تصویر - کاملا رایگان و قابل شخصی‌سازی",
        "base_price_usd": 0.02,
        "discount_percent": 85,
        "supplier": ["kie.ai"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["Open Source", "Customizable", "High Quality"],
        "tags": ["stable_diffusion", "xl", "open_source", "customizable"]
    },
    {
        "id": "leonardo_ai",
        "name": "Leonardo.AI",
        "category": "image",
        "subcategory": "image_generation",
        "description": "پلتفرم حرفه‌ای ساخت تصویر با مدل‌های متنوع",
        "base_price_usd": 12.00,
        "discount_percent": 80,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["Multiple Models", "Custom Training", "Commercial License"],
        "image_url": "https://leonardo.ai/favicon.ico",
        "tags": ["leonardo", "image", "professional", "training"],
        "competitor_price_toman": 8000000
    },
    {
        "id": "playground_ai",
        "name": "Playground AI",
        "category": "image",
        "subcategory": "image_generation",
        "description": "پلتفرم آسان برای ساخت تصویر با هوش مصنوعی",
        "base_price_usd": 8.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["User-Friendly", "Multiple Models", "Daily Free Credits"],
        "tags": ["playground", "image", "easy", "user_friendly"]
    },
    {
        "id": "bing_image_creator",
        "name": "Bing Image Creator",
        "category": "image",
        "subcategory": "image_generation",
        "description": "ساخت تصویر رایگان با هوش مصنوعی مایکروسافت",
        "base_price_usd": 0.01,
        "discount_percent": 90,
        "supplier": ["kie.ai"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["Free Tier", "DALL·E Powered", "Microsoft"],
        "tags": ["bing", "microsoft", "free", "dalle"]
    },
    {
        "id": "nightcafe",
        "name": "NightCafe",
        "category": "image",
        "subcategory": "image_generation",
        "description": "پلتفرم ساخت تصویر با مدل‌های متنوع و جامعه فعال",
        "base_price_usd": 6.00,
        "discount_percent": 80,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["Multiple Models", "Community", "Creative Tools"],
        "tags": ["nightcafe", "image", "community", "creative"]
    },
    {
        "id": "bluewillow",
        "name": "BlueWillow",
        "category": "image",
        "subcategory": "image_generation",
        "description": "رقیب Midjourney - کیفیت بالا با قیمت مناسب",
        "base_price_usd": 7.00,
        "discount_percent": 85,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["Midjourney Alternative", "High Quality", "Affordable"],
        "tags": ["bluewillow", "image", "alternative", "affordable"]
    },
]

# ========== VIDEO GENERATION AI ==========
VIDEO_AI_PRODUCTS = [
    {
        "id": "sora",
        "name": "Sora",
        "category": "video",
        "subcategory": "video_generation",
        "description": "مدل ویدیوی OpenAI - ساخت ویدیو از متن با کیفیت سینمایی",
        "base_price_usd": 25.00,
        "discount_percent": 80,
        "supplier": ["ggsel"],
        "delivery_time": "2-4 hours",
        "type": "personal",
        "features": ["Text-to-Video", "High Quality", "Up to 60 Seconds"],
        "image_url": "https://openai.com/assets/images/sora.png",
        "tags": ["sora", "openai", "video", "text_to_video"],
        "competitor_price_toman": 20000000,
        "is_popular": True,
        "is_new": True
    },
    {
        "id": "kling_ai",
        "name": "Kling AI",
        "category": "video",
        "subcategory": "video_generation",
        "description": "مدل ویدیوی چینی - رقیب Sora با کیفیت بالا",
        "base_price_usd": 20.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "2-3 hours",
        "type": "personal",
        "features": ["Chinese Model", "High Quality", "Long Duration"],
        "tags": ["kling", "video", "chinese", "sora_alternative"],
        "is_new": True
    },
    {
        "id": "veo",
        "name": "Veo",
        "category": "video",
        "subcategory": "video_generation",
        "description": "مدل ویدیوی Google - ساخت ویدیو با کیفیت حرفه‌ای",
        "base_price_usd": 18.00,
        "discount_percent": 70,
        "supplier": ["ggsel"],
        "delivery_time": "2 hours",
        "type": "personal",
        "features": ["Google AI", "High Quality", "1080p Resolution"],
        "tags": ["veo", "google", "video", "high_quality"]
    },
    {
        "id": "pika_labs",
        "name": "Pika Labs",
        "category": "video",
        "subcategory": "video_generation",
        "description": "پلتفرم ساخت ویدیو با هوش مصنوعی - مناسب برای همه",
        "base_price_usd": 15.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["User-Friendly", "Multiple Styles", "Fast Generation"],
        "image_url": "https://pika.art/favicon.ico",
        "tags": ["pika", "video", "user_friendly", "fast"]
    },
    {
        "id": "runway_ml",
        "name": "Runway ML",
        "category": "video",
        "subcategory": "video_generation",
        "description": "پلتفرم حرفه‌ای ساخت ویدیو و ویرایش با هوش مصنوعی",
        "base_price_usd": 12.00,
        "discount_percent": 80,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["Professional Tools", "Video Editing", "Green Screen"],
        "tags": ["runway", "video", "editing", "professional"],
        "competitor_price_toman": 9000000
    },
    {
        "id": "luma_ai",
        "name": "Luma AI",
        "category": "video",
        "subcategory": "video_generation",
        "description": "ساخت مدل‌های ۳D و ویدیو با کیفیت بالا",
        "base_price_usd": 10.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["3D Generation", "High Quality", "Immersive"],
        "tags": ["luma", "3d", "video", "immersive"]
    },
    {
        "id": "heygen",
        "name": "HeyGen",
        "category": "video",
        "subcategory": "video_generation",
        "description": "ساخت آواتار و ویدیو با هوش مصنوعی - مناسب برای کسب و کارها",
        "base_price_usd": 20.00,
        "discount_percent": 70,
        "supplier": ["ggsel"],
        "delivery_time": "2 hours",
        "type": "personal",
        "features": ["Avatar Creation", "Business Videos", "Multiple Languages"],
        "image_url": "https://heygen.com/favicon.ico",
        "tags": ["heygen", "avatar", "video", "business"],
        "competitor_price_toman": 14000000
    },
    {
        "id": "synthesia",
        "name": "Synthesia",
        "category": "video",
        "subcategory": "video_generation",
        "description": "ساخت ویدیو با آواتارهای AI - بدون نیاز به دوربین",
        "base_price_usd": 25.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "2-3 hours",
        "type": "personal",
        "features": ["AI Avatars", "100+ Languages", "Professional Quality"],
        "tags": ["synthesia", "avatar", "video", "multilingual"],
        "competitor_price_toman": 18000000
    },
]

# ========== CODING AI ==========
CODING_AI_PRODUCTS = [
    {
        "id": "github_copilot",
        "name": "GitHub Copilot",
        "category": "coding",
        "subcategory": "code_assistant",
        "description": "کمک برنامه‌نویس هوش مصنوعی - داخل ویرایشگر کد شما",
        "base_price_usd": 10.00,
        "discount_percent": 70,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["Code Completion", "Chat Support", "Multiple Languages"],
        "image_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        "tags": ["github", "copilot", "coding", "programming"],
        "competitor_price_toman": 3000000,
        "is_popular": True
    },
    {
        "id": "cursor_ai",
        "name": "Cursor AI",
        "category": "coding",
        "subcategory": "code_editor",
        "description": "ویرایشگر کد هوشمند با هوش مصنوعی یکپارچه",
        "base_price_usd": 15.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["AI-Powered Editor", "Code Generation", "Debugging"],
        "tags": ["cursor", "editor", "coding", "ai_powered"],
        "is_popular": True
    },
    {
        "id": "replit_ghostwriter",
        "name": "Replit Ghostwriter",
        "category": "coding",
        "subcategory": "code_assistant",
        "description": "کمک برنامه‌نویس در محیط Replit - مناسب برای تازه‌کارها",
        "base_price_usd": 5.00,
        "discount_percent": 65,
        "supplier": ["ggsel"],
        "delivery_time": "Instant",
        "type": "personal",
        "features": ["Code Assistance", "Learning Tools", "Collaborative"],
        "tags": ["replit", "ghostwriter", "coding", "learning"]
    },
    {
        "id": "tabnine",
        "name": "Tabnine",
        "category": "coding",
        "subcategory": "code_assistant",
        "description": "کمک برنامه‌نویس هوش مصنوعی - پیش‌بینی کد در زمان واقعی",
        "base_price_usd": 8.00,
        "discount_percent": 70,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["Code Prediction", "Multi-Language", "IDE Integration"],
        "tags": ["tabnine", "coding", "prediction", "ide"]
    },
]

# ========== MUSIC AI ==========
MUSIC_AI_PRODUCTS = [
    {
        "id": "boomy",
        "name": "Boomy",
        "category": "music",
        "subcategory": "music_generation",
        "description": "ساخت موسیقی با هوش مصنوعی - حتی بدون دانش موسیقی",
        "base_price_usd": 5.00,
        "discount_percent": 80,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["AI Music Creation", "Multiple Genres", "Instant Generation"],
        "image_url": "https://boomy.com/favicon.ico",
        "tags": ["boomy", "music", "ai", "generation"]
    },
    {
        "id": "soundraw",
        "name": "Soundraw",
        "category": "music",
        "subcategory": "music_generation",
        "description": "ساخت موسیقی حرفه‌ای با هوش مصنوعی - مناسب برای ویدیوها",
        "base_price_usd": 8.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["Professional Music", "Royalty-Free", "Customizable"],
        "tags": ["soundraw", "music", "professional", "royalty_free"]
    },
    {
        "id": "udio",
        "name": "Udio",
        "category": "music",
        "subcategory": "music_generation",
        "description": "ساخت موسیقی با کیفیت استودیویی با هوش مصنوعی",
        "base_price_usd": 10.00,
        "discount_percent": 70,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["Studio Quality", "Multiple Instruments", "AI Mastering"],
        "tags": ["udio", "music", "studio", "ai"],
        "is_new": True
    },
    {
        "id": "suno_ai",
        "name": "Suno AI",
        "category": "music",
        "subcategory": "music_generation",
        "description": "ساخت موسیقی کامل با هوش مصنوعی - از ملودی تا کلمات",
        "base_price_usd": 12.00,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "1-2 hours",
        "type": "personal",
        "features": ["Full Song Creation", "Lyrics + Music", "Multiple Genres"],
        "image_url": "https://suno.com/favicon.ico",
        "tags": ["suno", "music", "full_song", "lyrics"],
        "is_popular": True
    },
]

# ========== SUBSCRIPTION SERVICES ==========
SUBSCRIPTION_PRODUCTS = [
    {
        "id": "netflix_pakistan",
        "name": "Netflix پاکستان (Premium)",
        "category": "subscription",
        "subcategory": "streaming",
        "description": "اشتراک نتفلیکس پاکستان با تمام محتواهای اصلی - قیمت بسیار پایین",
        "base_price_usd": 2.86,
        "discount_percent": 85,
        "supplier": ["ggsel", "funpay"],
        "delivery_time": "1-2 hours",
        "type": "personal",
        "features": ["4K Quality", "All Regions Content", "4 Screens", "No Ads"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
        "tags": ["netflix", "pakistan", "streaming", "cheap"],
        "competitor_price_toman": 2000000,
        "is_popular": True
    },
    {
        "id": "netflix_turkey",
        "name": "Netflix ترکیه (Standard)",
        "category": "subscription",
        "subcategory": "streaming",
        "description": "اشتراک نتفلیکس ترکیه - تعادل بین قیمت و کیفیت",
        "base_price_usd": 3.75,
        "discount_percent": 80,
        "supplier": ["ggsel", "funpay"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["1080p Quality", "2 Screens", "No Ads"],
        "tags": ["netflix", "turkey", "streaming", "standard"],
        "competitor_price_toman": 2500000,
        "is_popular": True
    },
    {
        "id": "netflix_argentina",
        "name": "Netflix آرژانتین (Basic)",
        "category": "subscription",
        "subcategory": "streaming",
        "description": "اشتراک نتفلیکس آرژانتین - ارزان‌ترین گزینه",
        "base_price_usd": 8.28,
        "discount_percent": 65,
        "supplier": ["ggsel"],
        "delivery_time": "2 hours",
        "type": "personal",
        "features": ["720p Quality", "1 Screen", "No Ads"],
        "tags": ["netflix", "argentina", "streaming", "basic"]
    },
    {
        "id": "spotify_premium",
        "name": "Spotify Premium",
        "category": "subscription",
        "subcategory": "music_streaming",
        "description": "اشتراک اسپاتیفای پرمیوم - موسیقی و پادکست بدون آگهی",
        "base_price_usd": 1.50,
        "discount_percent": 85,
        "supplier": ["ggsel", "funpay"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["No Ads", "Download Music", "High Quality", "Skip Unlimited"],
        "image_url": "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Black.png",
        "tags": ["spotify", "premium", "music", "no_ads"],
        "competitor_price_toman": 1000000,
        "is_popular": True
    },
    {
        "id": "disney_plus",
        "name": "Disney+",
        "category": "subscription",
        "subcategory": "streaming",
        "description": "اشتراک دیزنی پلاس - دسترسی به تمام محتواهای دیزنی، مارول، استار ورز",
        "base_price_usd": 4.99,
        "discount_percent": 75,
        "supplier": ["ggsel", "funpay"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["4K Quality", "Disney", "Marvel", "Star Wars", "National Geographic"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg",
        "tags": ["disney", "streaming", "marvel", "star_wars"],
        "competitor_price_toman": 3000000
    },
    {
        "id": "hbo_max",
        "name": "HBO Max",
        "category": "subscription",
        "subcategory": "streaming",
        "description": "اشتراک HBO Max - دسترسی به سریال‌ها و فیلم‌های انحصاری HBO",
        "base_price_usd": 6.99,
        "discount_percent": 70,
        "supplier": ["ggsel"],
        "delivery_time": "1-2 hours",
        "type": "personal",
        "features": ["4K Quality", "HBO Originals", "Warner Bros", "DC Universe"],
        "tags": ["hbo", "max", "streaming", "series"]
    },
    {
        "id": "amazon_prime",
        "name": "Amazon Prime Video",
        "category": "subscription",
        "subcategory": "streaming",
        "description": "اشتراک آمازون پرایم ویدیو - فیلم‌ها و سریال‌های انحصاری آمازون",
        "base_price_usd": 5.99,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["4K Quality", "Amazon Originals", "Free Shipping (if applicable)"],
        "tags": ["amazon", "prime", "streaming", "video"]
    },
    {
        "id": "apple_tv_plus",
        "name": "Apple TV+",
        "category": "subscription",
        "subcategory": "streaming",
        "description": "اشتراک Apple TV+ - دسترسی به محتواهای انحصاری اپل",
        "base_price_usd": 4.99,
        "discount_percent": 80,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["4K Quality", "Apple Originals", "Family Sharing"],
        "tags": ["apple", "tv_plus", "streaming", "exclusive"]
    },
    {
        "id": "crunchyroll",
        "name": "Crunchyroll Premium",
        "category": "subscription",
        "subcategory": "streaming",
        "description": "اشتراک Crunchyroll - دسترسی به انیمه‌ها و دراماهای آسیایی",
        "base_price_usd": 4.99,
        "discount_percent": 75,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["Ad-Free", "Simulcast", "Subbed & Dubbed", "Manga"],
        "tags": ["crunchyroll", "anime", "streaming", "japanese"]
    },
]

# ========== API SERVICES ==========
API_PRODUCTS = [
    {
        "id": "gpt4_api",
        "name": "GPT-4 API Credit",
        "category": "api",
        "subcategory": "text_api",
        "description": "اعتبار API GPT-4 - برای توسعه‌دهندگان",
        "base_price_usd": 0.004,
        "discount_percent": 86,
        "supplier": ["kie.ai"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["GPT-4 Access", "8K Context", "JSON Mode"],
        "tags": ["gpt4", "api", "developer", "openai"],
        "competitor_price_toman": 7000,
        "is_popular": True
    },
    {
        "id": "gpt4_32k_api",
        "name": "GPT-4 32K API Credit",
        "category": "api",
        "subcategory": "text_api",
        "description": "اعتبار API GPT-4 با حافظه ۳۲ هزار توکن",
        "base_price_usd": 0.01,
        "discount_percent": 83,
        "supplier": ["kie.ai"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["32K Context", "Long Documents", "Complex Tasks"],
        "tags": ["gpt4", "32k", "api", "long_context"]
    },
    {
        "id": "gpt3_5_api",
        "name": "GPT-3.5 API Credit",
        "category": "api",
        "subcategory": "text_api",
        "description": "اعتبار API GPT-3.5 - اقتصادی و کارآمد",
        "base_price_usd": 0.001,
        "discount_percent": 85,
        "supplier": ["kie.ai"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["Cost Effective", "Fast", "Reliable"],
        "tags": ["gpt3_5", "api", "economic", "fast"],
        "competitor_price_toman": 2000
    },
    {
        "id": "claude_3_api",
        "name": "Claude 3 API Credit",
        "category": "api",
        "subcategory": "text_api",
        "description": "اعتبار API Claude 3 - برای کاربردهای حرفه‌ای",
        "base_price_usd": 0.005,
        "discount_percent": 80,
        "supplier": ["kie.ai"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["Claude 3 Access", "100K Context", "Advanced Reasoning"],
        "tags": ["claude", "api", "developer", "advanced"],
        "is_popular": True
    },
    {
        "id": "dalle3_api",
        "name": "DALL·E 3 API Credit",
        "category": "api",
        "subcategory": "image_api",
        "description": "اعتبار API DALL·E 3 - ساخت تصویر با کیفیت بالا",
        "base_price_usd": 0.04,
        "discount_percent": 80,
        "supplier": ["kie.ai"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["High Resolution", "Text-to-Image", "Commercial Use"],
        "tags": ["dalle3", "api", "image", "high_quality"]
    },
    {
        "id": "stable_diffusion_api",
        "name": "Stable Diffusion API Credit",
        "category": "api",
        "subcategory": "image_api",
        "description": "اعتبار API Stable Diffusion - باز و قابل شخصی‌سازی",
        "base_price_usd": 0.02,
        "discount_percent": 85,
        "supplier": ["kie.ai"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["Open Source", "Customizable", "High Quality"],
        "tags": ["stable_diffusion", "api", "open_source", "customizable"]
    },
    {
        "id": "whisper_api",
        "name": "Whisper API Credit",
        "category": "api",
        "subcategory": "audio_api",
        "description": "اعتبار API Whisper - تبدیل صدا به متن با دقت بالا",
        "base_price_usd": 0.006,
        "discount_percent": 80,
        "supplier": ["kie.ai"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["Speech-to-Text", "High Accuracy", "Multiple Languages"],
        "tags": ["whisper", "api", "speech_to_text", "audio"]
    },
    {
        "id": "tts_api",
        "name": "TTS (Text-to-Speech) API Credit",
        "category": "api",
        "subcategory": "audio_api",
        "description": "اعتبار API تبدیل متن به صدا - صدای طبیعی و با کیفیت",
        "base_price_usd": 0.008,
        "discount_percent": 75,
        "supplier": ["kie.ai"],
        "delivery_time": "Instant",
        "type": "api_credit",
        "features": ["Text-to-Speech", "Natural Voice", "Multiple Voices"],
        "tags": ["tts", "api", "text_to_speech", "voice"]
    },
]

# ========== ALL-IN-ONE PLATFORMS ==========
ALL_IN_ONE_PRODUCTS = [
    {
        "id": "unified_ai_hub",
        "name": "Unified AI Hub (1 ماه)",
        "category": "api",
        "subcategory": "all_in_one",
        "description": "دسترسی به تمام APIهای هوش مصنوعی در یک پلتفرم - تخفیف ۹۰%+",
        "base_price_usd": 10.00,
        "discount_percent": 90,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["All AI APIs", "Single Platform", "90%+ Discount", "Unlimited Access"],
        "image_url": "https://via.placeholder.com/150",
        "tags": ["all_in_one", "ai", "platform", "discount"],
        "competitor_price_toman": 10000000,
        "is_popular": True
    },
    {
        "id": "cabina_ai",
        "name": "Cabina.AI (1 ماه)",
        "category": "api",
        "subcategory": "all_in_one",
        "description": "پلتفرم همه‌کاره هوش مصنوعی - دسترسی به صدها ابزار",
        "base_price_usd": 4.72,
        "discount_percent": 85,
        "supplier": ["ggsel"],
        "delivery_time": "30 min",
        "type": "personal",
        "features": ["Hundreds of Tools", "All Categories", "85%+ Discount"],
        "tags": ["cabina", "all_in_one", "tools", "discount"]
    },
    {
        "id": "poe_premium",
        "name": "Poe Premium (1 ماه)",
        "category": "chat",
        "subcategory": "all_in_one",
        "description": "دسترسی به تمام چت‌بات‌های هوش مصنوعی در یک پلتفرم",
        "base_price_usd": 15.00,
        "discount_percent": 70,
        "supplier": ["ggsel"],
        "delivery_time": "1 hour",
        "type": "personal",
        "features": ["All AI Chatbots", "Single Platform", "Premium Access"],
        "tags": ["poe", "chatbots", "platform", "premium"]
    },
]

# ========== COMBINE ALL PRODUCTS ==========
ALL_PRODUCTS = (
    CHAT_AI_PRODUCTS +
    IMAGE_AI_PRODUCTS +
    VIDEO_AI_PRODUCTS +
    CODING_AI_PRODUCTS +
    MUSIC_AI_PRODUCTS +
    SUBSCRIPTION_PRODUCTS +
    API_PRODUCTS +
    ALL_IN_ONE_PRODUCTS
)

# Categories configuration
CATEGORIES = {
    "chat": {
        "name": "چت و متن",
        "icon": "💬",
        "description": "چت‌بات‌ها و ابزارهای تولید متن با هوش مصنوعی",
        "color": "#4F46E5"
    },
    "image": {
        "name": "ساخت عکس",
        "icon": "🎨",
        "description": "ابزارهای ساخت و ویرایش تصویر با هوش مصنوعی",
        "color": "#EC4899"
    },
    "video": {
        "name": "ساخت ویدیو",
        "icon": "🎬",
        "description": "ابزارهای ساخت و ویرایش ویدیو با هوش مصنوعی",
        "color": "#F59E0B"
    },
    "coding": {
        "name": "کد نویسی",
        "icon": "💻",
        "description": "ابزارهای کمک به برنامه‌نویسی با هوش مصنوعی",
        "color": "#10B981"
    },
    "music": {
        "name": "موسیقی",
        "icon": "🎵",
        "description": "ابزارهای ساخت موسیقی با هوش مصنوعی",
        "color": "#8B5CF6"
    },
    "subscription": {
        "name": "اشتراک‌ها",
        "icon": "📺",
        "description": "اشتراک سرویس‌های استریمینگ و پلتفرم‌ها",
        "color": "#EF4444"
    },
    "api": {
        "name": "APIها",
        "icon": "🔌",
        "description": "اعتبار APIهای هوش مصنوعی برای توسعه‌دهندگان",
        "color": "#6366F1"
    }
}

# Subcategories
SUBCATEGORIES = {
    "text_generation": "تولید متن",
    "image_generation": "تولید تصویر",
    "video_generation": "تولید ویدیو",
    "code_assistant": "کمک برنامه‌نویس",
    "code_editor": "ویرایشگر کد",
    "music_generation": "تولید موسیقی",
    "streaming": "استریمینگ",
    "music_streaming": "استریمینگ موسیقی",
    "text_api": "API متن",
    "image_api": "API تصویر",
    "audio_api": "API صدا",
    "all_in_one": "همه‌کاره"
}

# Product types
PRODUCT_TYPES = {
    "personal": "اختصاصی",
    "shared": "اشتراکی",
    "api_credit": "اعتبار API"
}


def get_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
    """Get a product by its ID"""
    for product in ALL_PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def get_products_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all products in a category"""
    return [product for product in ALL_PRODUCTS if product["category"] == category]


def get_products_by_type(product_type: str) -> List[Dict[str, Any]]:
    """Get all products of a specific type"""
    return [product for product in ALL_PRODUCTS if product["type"] == product_type]


def search_products(query: str) -> List[Dict[str, Any]]:
    """Search products by name or description"""
    query = query.lower()
    results = []
    for product in ALL_PRODUCTS:
        if query in product["name"].lower() or query in product["description"].lower():
            results.append(product)
    return results


def get_popular_products(limit: int = 8) -> List[Dict[str, Any]]:
    """Get popular products"""
    popular = [product for product in ALL_PRODUCTS if product.get("is_popular", False)]
    return sorted(popular, key=lambda x: x.get("competitor_price_toman", 0), reverse=True)[:limit]


def get_new_products(limit: int = 8) -> List[Dict[str, Any]]:
    """Get new products"""
    new_products = [product for product in ALL_PRODUCTS if product.get("is_new", False)]
    return sorted(new_products, key=lambda x: x.get("base_price_usd", 0))[:limit]


def get_featured_products() -> List[Dict[str, Any]]:
    """Get featured products for homepage"""
    featured_ids = [
        "chatgpt_plus_monthly",
        "midjourney_v6", 
        "netflix_pakistan",
        "gpt4_api",
        "claude_3_5_sonnet",
        "sora",
        "spotify_premium",
        "unified_ai_hub"
    ]
    return [product for product in ALL_PRODUCTS if product["id"] in featured_ids]
