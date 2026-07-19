"""
Configuration for 25+ SEO Agents
These agents will be integrated into the platform for professional SEO
"""

# Configuration for all SEO agents
SEO_AGENTS = [
    # ========== CONTENT GENERATION AGENTS ==========
    {
        "id": "content_writer_agent",
        "name": "Content Writer Agent",
        "description": "تولید مقالات سئو شده با کلمات کلیدی هدف",
        "type": "content_generation",
        "capabilities": [
            "Generate SEO-optimized articles (500-2000 words)",
            "Include target keywords naturally",
            "Create engaging introductions and conclusions",
            "Add internal linking suggestions",
            "Generate meta descriptions"
        ],
        "github_repo": "https://github.com/microsoft/autogen",
        "implementation": "AutogenBasedContentWriter",
        "priority": "high",
        "is_active": True,
        "config": {
            "max_tokens": 4000,
            "temperature": 0.7,
            "top_p": 0.9
        }
    },
    {
        "id": "blog_post_agent",
        "name": "Blog Post Agent",
        "description": "تولید پست‌های وبلاگ حرفه‌ای با ساختار سئو",
        "type": "content_generation",
        "capabilities": [
            "Create blog post outlines",
            "Write complete blog posts",
            "Optimize for featured snippets",
            "Add FAQ sections",
            "Include schema markup suggestions"
        ],
        "github_repo": "https://github.com/langchain-ai/langchain",
        "implementation": "LangChainBlogWriter",
        "priority": "high",
        "is_active": True
    },
    {
        "id": "meta_description_agent",
        "name": "Meta Description Agent",
        "description": "تولید متا دیسکریپشن‌های جذاب و سئو شده",
        "type": "content_generation",
        "capabilities": [
            "Generate meta descriptions (150-160 characters)",
            "Include primary keywords",
            "Create compelling call-to-actions",
            "Optimize for CTR",
            "A/B testing suggestions"
        ],
        "github_repo": "https://github.com/hwchase17/langchain",
        "implementation": "MetaDescriptionGenerator",
        "priority": "high",
        "is_active": True
    },
    {
        "id": "title_generator_agent",
        "name": "Title Generator Agent",
        "description": "تولید تیترهای جذاب و سئو شده",
        "type": "content_generation",
        "capabilities": [
            "Generate SEO-optimized titles (50-60 characters)",
            "Include primary and secondary keywords",
            "Create emotional triggers",
            "Optimize for social sharing",
            "Suggest multiple variations"
        ],
        "github_repo": "https://github.com/ai-seo-tools/ai-seo-tools",
        "implementation": "TitleGenerator",
        "priority": "high",
        "is_active": True
    },
    {
        "id": "faq_generator_agent",
        "name": "FAQ Generator Agent",
        "description": "تولید سوالات متداول برای صفحات محصول",
        "type": "content_generation",
        "capabilities": [
            "Generate FAQ based on product features",
            "Include common user questions",
            "Optimize for featured snippets",
            "Add schema markup",
            "Suggest related questions"
        ],
        "github_repo": "https://github.com/serpapi/google-search-results-python",
        "implementation": "FAQGenerator",
        "priority": "medium",
        "is_active": True
    },
    {
        "id": "schema_markup_agent",
        "name": "Schema Markup Agent",
        "description": "تولید کدهای Schema Markup برای سئو",
        "type": "content_generation",
        "capabilities": [
            "Generate Product schema",
            "Create FAQPage schema",
            "Add BreadcrumbList schema",
            "Implement Organization schema",
            "Generate Review schema"
        ],
        "github_repo": "https://github.com/schemaorg/schemaorg",
        "implementation": "SchemaMarkupGenerator",
        "priority": "high",
        "is_active": True
    },
    {
        "id": "image_alt_text_agent",
        "name": "Image Alt Text Agent",
        "description": "تولید متن‌های alt برای تصاویر",
        "type": "content_generation",
        "capabilities": [
            "Generate descriptive alt text",
            "Include relevant keywords",
            "Optimize for accessibility",
            "Create for all images on page",
            "Suggest image file name optimization"
        ],
        "implementation": "InternalImageOptimizer",
        "priority": "medium",
        "is_active": True
    },
    {
        "id": "internal_linking_agent",
        "name": "Internal Linking Agent",
        "description": "پیشنهاد لینک‌های داخلی برای بهبود سئو",
        "type": "content_generation",
        "capabilities": [
            "Suggest relevant internal links",
            "Analyze content for linking opportunities",
            "Optimize anchor text",
            "Create link silos",
            "Track internal link structure"
        ],
        "implementation": "InternalLinkingSuggester",
        "priority": "high",
        "is_active": True
    },

    # ========== KEYWORD RESEARCH AGENTS ==========
    {
        "id": "keyword_research_agent",
        "name": "Keyword Research Agent",
        "description": "تحقیق کلمات کلیدی جامع برای سئو",
        "type": "keyword_research",
        "capabilities": [
            "Find long-tail keywords",
            "Analyze search volume",
            "Calculate keyword difficulty",
            "Suggest related keywords",
            "Identify content gaps",
            "Competitor keyword analysis"
        ],
        "github_repo": "https://github.com/serpapi/google-search-results-python",
        "implementation": "SerpAPIKeywordResearcher",
        "priority": "critical",
        "is_active": True,
        "config": {
            "api_key_required": True,
            "search_engine": "google",
            "location": "IR"
        }
    },
    {
        "id": "long_tail_keyword_agent",
        "name": "Long-Tail Keyword Agent",
        "description": "یافتن کلمات کلیدی دم بلند با پتانسیل بالا",
        "type": "keyword_research",
        "capabilities": [
            "Identify long-tail opportunities",
            "Analyze user intent",
            "Suggest question-based keywords",
            "Find low-competition keywords",
            "Generate keyword clusters"
        ],
        "github_repo": "https://github.com/neil916/keyword-extractor",
        "implementation": "LongTailKeywordFinder",
        "priority": "high",
        "is_active": True
    },
    {
        "id": "competitor_analysis_agent",
        "name": "Competitor Analysis Agent",
        "description": "آنالیز رقبا و یافتن فرصت‌های سئو",
        "type": "keyword_research",
        "capabilities": [
            "Analyze competitor websites",
            "Identify their top keywords",
            "Find backlink sources",
            "Discover content gaps",
            "Track ranking changes"
        ],
        "github_repo": "https://github.com/seo-tools/seo-competitor-analysis",
        "implementation": "CompetitorAnalyzer",
        "priority": "high",
        "is_active": True
    },
    {
        "id": "keyword_difficulty_agent",
        "name": "Keyword Difficulty Agent",
        "description": "محاسبه سختی کلمات کلیدی",
        "type": "keyword_research",
        "capabilities": [
            "Calculate keyword difficulty score",
            "Analyze SERP features",
            "Evaluate domain authority of competitors",
            "Predict ranking potential",
            "Suggest achievable keywords"
        ],
        "github_repo": "https://github.com/moz/mechanize",
        "implementation": "KeywordDifficultyCalculator",
        "priority": "medium",
        "is_active": True
    },
    {
        "id": "search_intent_agent",
        "name": "Search Intent Agent",
        "description": "آنالیز هدف جستجوی کاربران",
        "type": "keyword_research",
        "capabilities": [
            "Identify user search intent",
            "Classify as informational/navigational/commercial/transactional",
            "Suggest content type based on intent",
            "Optimize content for intent",
            "Analyze SERP for intent signals"
        ],
        "implementation": "SearchIntentAnalyzer",
        "priority": "medium",
        "is_active": True
    },

    # ========== TECHNICAL SEO AGENTS ==========
    {
        "id": "site_audit_agent",
        "name": "Site Audit Agent",
        "description": "بررسی کامل سایت برای مشکلات سئو",
        "type": "technical_seo",
        "capabilities": [
            "Crawl entire website",
            "Identify broken links",
            "Check for duplicate content",
            "Analyze page speed",
            "Detect mobile usability issues",
            "Check HTTPS implementation",
            "Validate structured data"
        ],
        "github_repo": "https://github.com/screamingfrog/seo-spider",
        "implementation": "SiteAuditor",
        "priority": "critical",
        "is_active": True,
        "config": {
            "crawl_limit": 1000,
            "check_external_links": True
        }
    },
    {
        "id": "page_speed_agent",
        "name": "Page Speed Agent",
        "description": "بهینه‌سازی سرعت صفحات",
        "type": "technical_seo",
        "capabilities": [
            "Analyze page load speed",
            "Identify render-blocking resources",
            "Suggest image optimization",
            "Recommend caching strategies",
            "Check for lazy loading opportunities",
            "Generate Lighthouse reports"
        ],
        "github_repo": "https://github.com/GoogleChrome/lighthouse",
        "implementation": "PageSpeedOptimizer",
        "priority": "high",
        "is_active": True
    },
    {
        "id": "mobile_friendly_agent",
        "name": "Mobile Friendly Agent",
        "description": "بررسی و بهینه‌سازی برای موبایل",
        "type": "technical_seo",
        "capabilities": [
            "Check mobile responsiveness",
            "Test touch targets",
            "Analyze viewport settings",
            "Identify mobile usability issues",
            "Suggest mobile optimizations",
            "Validate mobile-first indexing"
        ],
        "github_repo": "https://github.com/GoogleChrome/mobile-friendly-test-api",
        "implementation": "MobileFriendlyChecker",
        "priority": "high",
        "is_active": True
    },
    {
        "id": "xml_sitemap_agent",
        "name": "XML Sitemap Agent",
        "description": "تولید و مدیریت نقشه سایت XML",
        "type": "technical_seo",
        "capabilities": [
            "Generate XML sitemap",
            "Update sitemap automatically",
            "Include all important pages",
            "Set priority and change frequency",
            "Submit to search engines",
            "Monitor sitemap errors"
        ],
        "implementation": "XMLSitemapGenerator",
        "priority": "medium",
        "is_active": True
    },

    # ========== LINK BUILDING AGENTS ==========
    {
        "id": "backlink_analysis_agent",
        "name": "Backlink Analysis Agent",
        "description": "آنالیز بک‌لینک‌ها و استراتژی لینک‌سازی",
        "type": "link_building",
        "capabilities": [
            "Analyze existing backlinks",
            "Identify toxic links",
            "Suggest link building opportunities",
            "Track backlink growth",
            "Monitor competitor backlinks",
            "Calculate domain authority"
        ],
        "github_repo": "https://github.com/ahrefs/ahrefs-api-python",
        "implementation": "BacklinkAnalyzer",
        "priority": "medium",
        "is_active": True
    },
    {
        "id": "guest_post_agent",
        "name": "Guest Post Agent",
        "description": "یافتن فرصت‌های پست مهمان",
        "type": "link_building",
        "capabilities": [
            "Find relevant blogs for guest posting",
            "Analyze domain authority",
            "Suggest outreach templates",
            "Track guest post opportunities",
            "Monitor backlink acquisition"
        ],
        "implementation": "GuestPostOpportunityFinder",
        "priority": "low",
        "is_active": False  # Requires manual review
    },
    {
        "id": "broken_link_agent",
        "name": "Broken Link Agent",
        "description": "یافتن لینک‌های شکسته و فرصت‌های لینک‌سازی",
        "type": "link_building",
        "capabilities": [
            "Find broken links on target sites",
            "Identify link reclamation opportunities",
            "Suggest replacement content",
            "Track broken link building",
            "Monitor link health"
        ],
        "implementation": "BrokenLinkFinder",
        "priority": "medium",
        "is_active": True
    },

    # ========== MONITORING AGENTS ==========
    {
        "id": "rank_tracking_agent",
        "name": "Rank Tracking Agent",
        "description": "رصد رتبه کلمات کلیدی",
        "type": "monitoring",
        "capabilities": [
            "Track keyword rankings",
            "Monitor position changes",
            "Analyze ranking trends",
            "Compare with competitors",
            "Generate ranking reports",
            "Send alerts for ranking changes"
        ],
        "github_repo": "https://github.com/serpapi/google-search-results-python",
        "implementation": "RankTracker",
        "priority": "critical",
        "is_active": True,
        "config": {
            "check_frequency": "daily",
            "locations": ["IR"],
            "devices": ["desktop", "mobile"]
        }
    },
    {
        "id": "traffic_analysis_agent",
        "name": "Traffic Analysis Agent",
        "description": "آنالیز ترافیک سایت",
        "type": "monitoring",
        "capabilities": [
            "Analyze traffic sources",
            "Track user behavior",
            "Identify top pages",
            "Monitor bounce rate",
            "Suggest traffic improvements",
            "Generate traffic reports"
        ],
        "github_repo": "https://github.com/googleanalytics/google-analytics-data",
        "implementation": "TrafficAnalyzer",
        "priority": "high",
        "is_active": True
    },
    {
        "id": "seo_performance_agent",
        "name": "SEO Performance Agent",
        "description": "بررسی عملکرد کلی سئو",
        "type": "monitoring",
        "capabilities": [
            "Calculate overall SEO score",
            "Track improvements over time",
            "Identify areas for improvement",
            "Compare with industry benchmarks",
            "Generate comprehensive reports",
            "Suggest actionable recommendations"
        ],
        "implementation": "SEOPerformanceMonitor",
        "priority": "high",
        "is_active": True
    },

    # ========== LOCAL SEO AGENTS ==========
    {
        "id": "local_seo_agent",
        "name": "Local SEO Agent",
        "description": "بهینه‌سازی سئو محلی",
        "type": "local_seo",
        "capabilities": [
            "Optimize Google My Business",
            "Generate local citations",
            "Analyze local competition",
            "Suggest local keywords",
            "Monitor local rankings",
            "Manage reviews and ratings"
        ],
        "implementation": "LocalSEOOptimizer",
        "priority": "medium",
        "is_active": True
    },
    {
        "id": "google_my_business_agent",
        "name": "Google My Business Agent",
        "description": "مدیریت و بهینه‌سازی پروفایل Google My Business",
        "type": "local_seo",
        "capabilities": [
            "Create GMB profile",
            "Optimize business information",
            "Manage posts and updates",
            "Respond to reviews",
            "Add photos and videos",
            "Monitor insights"
        ],
        "implementation": "GoogleMyBusinessManager",
        "priority": "medium",
        "is_active": True
    }
]


def get_agent_by_id(agent_id: str) -> Optional[Dict]:
    """Get SEO agent by ID"""
    for agent in SEO_AGENTS:
        if agent["id"] == agent_id:
            return agent
    return None


def get_agents_by_type(agent_type: str) -> List[Dict]:
    """Get all SEO agents of a specific type"""
    return [agent for agent in SEO_AGENTS if agent["type"] == agent_type]


def get_active_agents() -> List[Dict]:
    """Get all active SEO agents"""
    return [agent for agent in SEO_AGENTS if agent.get("is_active", False)]


def get_agents_by_priority(priority: str) -> List[Dict]:
    """Get all SEO agents by priority level"""
    return [agent for agent in SEO_AGENTS if agent.get("priority") == priority]
