// ─── E-Commerce Trust & Verification App Data ───────────────────────────────

export const EXAMPLES = [
  'AirPods Pro 2 for $29 are genuine Apple',
  'Sony WH-1000XM5 70% off flash deal is real',
  '100% Mulberry Silk sheet set for $18.99',
  'Earbuds with 15k 5-star reviews have no fake reviews',
  'Seller offers free 30-day returns with no fees',
]

export const SOURCES_DB = {
  'airpods pro 2 for $29 are genuine apple': [
    { name: 'Apple Brand Registry & Security', url: 'checkcoverage.apple.com', kind: 'Manufacturer Database', relevance: 98, credibility: 99, date: 'Oct 2025', stance: 'Contradicts', initials: 'APL', excerpt: 'Serial numbers listed by this marketplace merchant belong to cloned replacement parts. Authentic AirPods Pro 2 have an MSRP of $249 and are not distributed through unauthorized third-party discount brokers.', color: '#0f172a' },
    { name: 'FakeSpot Product Analysis', url: 'fakespot.com/product/airpods-pro-2-clone', kind: 'Counterfeit & Review AI', relevance: 94, credibility: 96, date: 'Sep 2025', stance: 'Contradicts', initials: 'FS', excerpt: 'Our hardware teardown algorithms and listing telemetry confirm high risk of counterfeit reproduction. Packaging lacks genuine Apple embossing and uses non-standard H1 knockoff chips.', color: '#2563eb' },
    { name: 'CamelCamelCamel Price Tracker', url: 'camelcamelcamel.com/product/airpods-pro-2', kind: 'Historical Price Index', relevance: 88, credibility: 95, date: 'Oct 2025', stance: 'Contradicts', initials: 'CCC', excerpt: 'Historical price floor for authentic units is $179.99 during Black Friday. Any listing at $29 represents an 88% deviation from wholesale cost, strongly indicating replica goods.', color: '#f59e0b' },
    { name: 'Better Business Bureau (BBB)', url: 'bbb.org/profile/superdeals-marketplace', kind: 'Consumer Protection', relevance: 85, credibility: 94, date: 'Aug 2025', stance: 'Contradicts', initials: 'BBB', excerpt: 'Merchant has 48 open complaints regarding unauthorized electronic replicas, delayed refunds, and counterfeit wireless earbuds shipped in unbranded packaging.', color: '#0284c7' },
    { name: 'Trustpilot Merchant Reviews', url: 'trustpilot.com/review/superdealz.com', kind: 'Consumer Review Platform', relevance: 82, credibility: 86, date: 'Sep 2025', stance: 'Contradicts', initials: 'TP', excerpt: 'Average customer rating is 1.3/5. 94% of buyer reports confirm receiving knockoff earbuds that malfunctioned within 2 weeks.', color: '#10b981' },
    { name: 'Discount Deal Blog', url: 'cheaptechhunter.net/airpods-sale', kind: 'Affiliate Publisher', relevance: 65, credibility: 62, date: 'Oct 2025', stance: 'Supports', initials: 'DH', excerpt: 'Overstock liquidation claim: Warehouse clearance enables massive discount on premium audio gear while inventory lasts.', color: '#ef4444' },
  ],
  'default': [
    { name: 'FakeSpot E-Commerce Intel', url: 'fakespot.com', kind: 'Review & Product Audit', relevance: 92, credibility: 96, date: 'Oct 2025', stance: 'Contradicts', initials: 'FS', excerpt: 'Automated listing telemetry identified irregular seller patterns, unverified buyer reviews, and manipulated product specifications.', color: '#2563eb' },
    { name: 'CamelCamelCamel Price Tracker', url: 'camelcamelcamel.com', kind: 'Price History Engine', relevance: 89, credibility: 95, date: 'Oct 2025', stance: 'Contradicts', initials: 'CCC', excerpt: 'Historical pricing logs reveal artificial MSRP inflation prior to the promotional event to create a deceptive discount percentage.', color: '#f59e0b' },
    { name: 'Trustpilot Verified Reviews', url: 'trustpilot.com', kind: 'Consumer Feedback', relevance: 84, credibility: 90, date: 'Sep 2025', stance: 'Contradicts', initials: 'TP', excerpt: 'Multiple verified buyers report receipt of goods that differed substantially from promotional photos and stated specifications.', color: '#10b981' },
    { name: 'Consumer Reports Product Lab', url: 'consumerreports.org', kind: 'Independent Testing', relevance: 81, credibility: 98, date: 'Aug 2025', stance: 'Supports', initials: 'CR', excerpt: 'Independent testing shows budget alternatives can offer acceptable utility, though advertised premium claims remain unsubstantiated.', color: '#0891b2' },
  ]
}

export const VERDICTS_DB = {
  'airpods pro 2 for $29 are genuine apple': {
    verdict: 'False',
    confidence: 97,
    color: '#c91e2a',
    bg: 'linear-gradient(135deg,#fff4f4,#fffafa)',
    border: '#f8e4e6',
    symbolColor: '#f14f57',
    symbolBorder: '#ffb4b8',
    symbolGlow: '#ffe4e5',
    barColor: '#ef4444',
    summary: 'Counterfeit replica alert: This listing sells knockoff AirPods Pro. Apple serial numbers fail warranty verification, the seller is unauthorized, and pricing is 88% below genuine wholesale cost.',
    type: 'Product Authenticity',
    domain: 'Consumer Electronics',
    topics: ['Apple', 'AirPods', 'Counterfeit Detection', 'Unauthorized Seller', 'Hardware Replica'],
    sourcesCount: 14,
    analysisTime: '3.1 seconds',
    reasoning: [
      'Apple Brand Registry and CheckCoverage confirm the serial numbers provided on packaging are duplicated cloned identifiers.',
      'CamelCamelCamel historical data confirms the lowest recorded genuine price is $179.99; a $29 price point is economically impossible for authentic hardware.',
      'FakeSpot telemetry identified 96% suspicious review patterns and merchant is flagged for shipping clone chipsets.'
    ],
    takeaway: 'Do not purchase. This is a high-risk counterfeit item. Genuine AirPods Pro 2 are never sold new at $29 by authorized Apple distributors.',
    analysis: 'Cross-platform verification confirms this listing is a counterfeit operation. The merchant uses cloned serial barcodes from legitimate products to bypass basic filters, but hardware teardowns and price history confirm replica components.',
    image: 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=1200&q=85',
    imageAlt: 'Wireless earbuds and charging case',
    quote: '"Unauthorized vendors selling flagship audio electronics below wholesale cost represent a 97% probability of counterfeit replica hardware."',
    quoteSource: '— FakeSpot Product Security Lab',
    supporting: 1,
    contradicting: 11,
    lowCred: 2
  },
  'sony wh-1000xm5 70% off flash deal is real': {
    verdict: 'Misleading',
    confidence: 89,
    color: '#b45309',
    bg: 'linear-gradient(135deg,#fffbeb,#fefce8)',
    border: '#fde68a',
    symbolColor: '#d97706',
    symbolBorder: '#fcd34d',
    symbolGlow: '#fef3c7',
    barColor: '#f59e0b',
    summary: 'Deceptive discount tactic: The seller artificially raised the reference MSRP to $899 (actual retail is $399) to claim a 70% discount. The deal price is standard market rate, not an extraordinary saving.',
    type: 'Price Manipulation',
    domain: 'Pricing & Deals',
    topics: ['Sony', 'Fake Discount', 'Price Gouging', 'CamelCamelCamel', 'Flash Sale'],
    sourcesCount: 9,
    analysisTime: '2.8 seconds',
    reasoning: [
      'Price tracking records show the product never sold for the claimed $899 anchor price on any major marketplace.',
      'The actual selling price of $279 is within typical seasonal discount range (20-30% off standard $399 MSRP).',
      'The merchant manipulated the "original price" strike-through tag to manufacture false urgency.'
    ],
    takeaway: 'The headphones are legitimate, but the advertised 70% discount is deceptive. You are getting a modest 25% discount, not 70%.',
    analysis: 'Reference price inflation is a common retail manipulation tactic. The seller doubles the anchor price in product metadata so automated filters generate a "Huge 70% Off" promotional tag.',
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=85',
    imageAlt: 'Premium wireless headphones on stand',
    quote: '"Anchor price inflation tricks consumers into perceived windfalls while charging standard prevailing rates."',
    quoteSource: '— CamelCamelCamel Historical Pricing Index',
    supporting: 1,
    contradicting: 7,
    lowCred: 1
  },
  '100% mulberry silk sheet set for $18.99': {
    verdict: 'False',
    confidence: 96,
    color: '#c91e2a',
    bg: 'linear-gradient(135deg,#fff4f4,#fffafa)',
    border: '#f8e4e6',
    symbolColor: '#f14f57',
    symbolBorder: '#ffb4b8',
    symbolGlow: '#ffe4e5',
    barColor: '#ef4444',
    summary: 'Material misrepresentation: Real Mulberry silk raw materials cost over $110 per king sheet. Fabric laboratory tests confirm this item is 100% polyester satin microfiber, not natural silk.',
    type: 'Material Authenticity',
    domain: 'Home & Bedding',
    topics: ['Mulberry Silk', 'Fabric Testing', 'Polyester Satin', 'False Advertising'],
    sourcesCount: 11,
    analysisTime: '3.4 seconds',
    reasoning: [
      'Raw natural Mulberry silk costs $35-$45 per pound at wholesale; a full sheet set requires 3.5 lbs of fabric.',
      'Consumer Product Safety Commission and lab reports confirm tested samples from this vendor contain 0% natural protein fiber.',
      'The seller uses ambiguous keywords "Silk Feeling" and "Satin Weave" in legal disclosures while advertising "100% Mulberry Silk" on image banners.'
    ],
    takeaway: 'This product is synthetic polyester, not real silk. If you have sensitive skin or expect genuine silk benefits, avoid this listing.',
    analysis: 'Synthetic polyester satin is frequently marketed as "Mulberry Silk" to command higher sales volume. Authentic momme-rated silk cannot be manufactured and shipped profitably under $120.',
    image: 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=1200&q=85',
    imageAlt: 'Bedding with smooth fabric sheets',
    quote: '"Microfiber polyester mimics silk shine in photographs but contains zero organic sericin or silk protein."',
    quoteSource: '— Textile Testing Laboratory Review',
    supporting: 0,
    contradicting: 10,
    lowCred: 1
  },
  'earbuds with 15k 5-star reviews have no fake reviews': {
    verdict: 'False',
    confidence: 93,
    color: '#c91e2a',
    bg: 'linear-gradient(135deg,#fff4f4,#fffafa)',
    border: '#f8e4e6',
    symbolColor: '#f14f57',
    symbolBorder: '#ffb4b8',
    symbolGlow: '#ffe4e5',
    barColor: '#ef4444',
    summary: 'Manipulated review farm detected: FakeSpot assigned this product an "F" grade. Over 78% of the 15,000 reviews were posted by review-broker networks and unverified accounts in exchange for gift cards.',
    type: 'Review Authenticity',
    domain: 'Review Fraud',
    topics: ['Fake Reviews', 'FakeSpot', 'Review Farm', 'Astroturfing', 'Consumer Deception'],
    sourcesCount: 13,
    analysisTime: '4.1 seconds',
    reasoning: [
      'Review velocity analysis detected 4,200 five-star ratings posted within a single 48-hour window with duplicate linguistic phrases.',
      'Over 65% of reviewer accounts have no prior purchase history and were created within 30 days of posting.',
      'Product packaging includes an illegal insert offering a $25 gift card in exchange for a five-star photo review.'
    ],
    takeaway: 'The 4.9-star rating is artificial. Adjusted for organic verified buyers, this product has an estimated true rating of 2.7 out of 5.',
    analysis: 'Incentivized review syndicates systematically inflate low-cost electronic accessories. Amazon and marketplace algorithms frequently purge these listings once review correlation thresholds trigger audit flags.',
    image: 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=1200&q=85',
    imageAlt: 'Wireless earbuds in open case',
    quote: '"Review clustering telemetry detected 78% synthesized feedback orchestrated via overseas review-broker groups."',
    quoteSource: '— FakeSpot E-Commerce Security Audit',
    supporting: 1,
    contradicting: 11,
    lowCred: 1
  },
  'seller offers free 30-day returns with no fees': {
    verdict: 'Misleading',
    confidence: 84,
    color: '#b45309',
    bg: 'linear-gradient(135deg,#fffbeb,#fefce8)',
    border: '#fde68a',
    symbolColor: '#d97706',
    symbolBorder: '#fcd34d',
    symbolGlow: '#fef3c7',
    barColor: '#f59e0b',
    summary: 'Hidden fee disclaimer: While promotional banners highlight "Free 30-Day Returns", the terms of service require buyers to ship items to an overseas address at their own cost plus a 25% restocking fee.',
    type: 'Seller Policy',
    domain: 'Consumer Rights',
    topics: ['Return Policy', 'Hidden Fees', 'Restocking Fee', 'Dispute Risk'],
    sourcesCount: 8,
    analysisTime: '3.0 seconds',
    reasoning: [
      'Fine print on checkout section 8.4 reveals buyer bears tracked international shipping costs ($35+) for returns.',
      'A mandatory 25% restocking surcharge is deducted from refund totals on open-box items.',
      'BBB consumer complaints cite refusal to provide prepaid return mailing labels despite promotional guarantees.'
    ],
    takeaway: 'Returns are not free. Returning an unwanted item will cost $35 to $50 out of pocket due to international return shipping rules and restocking fees.',
    analysis: 'Bait-and-switch return policies display a prominent "Hassle-Free Returns" trust badge on listing headers while burying punitive return requirements in multi-page nested terms.',
    image: 'https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?auto=format&fit=crop&w=1200&q=85',
    imageAlt: 'Shipping cardboard package and return label',
    quote: '"Prominent header guarantees often directly contradict restrictive return clauses buried in fine print disclosures."',
    quoteSource: '— Better Business Bureau Retail Review',
    supporting: 2,
    contradicting: 5,
    lowCred: 1
  }
}

export const HISTORY_ITEMS = [
  { id: 1, claim: 'AirPods Pro 2 for $29 are genuine Apple products.', verdict: 'False', confidence: 97, date: 'Oct 1, 2026', time: '02:34 PM', domain: 'Consumer Tech' },
  { id: 2, claim: 'Sony WH-1000XM5 has real 70% flash markdown.', verdict: 'Misleading', confidence: 89, date: 'Sep 29, 2026', time: '11:17 AM', domain: 'Price Tracking' },
  { id: 3, claim: '100% Mulberry Silk sheet set for $18.99 is authentic.', verdict: 'False', confidence: 96, date: 'Sep 27, 2026', time: '03:45 PM', domain: 'Home & Bedding' },
  { id: 4, claim: 'Wireless earbuds 15k 5-star reviews are genuine organic.', verdict: 'False', confidence: 93, date: 'Sep 25, 2026', time: '09:22 AM', domain: 'Review Fraud' },
  { id: 5, claim: 'Seller provides zero-fee free returns within 30 days.', verdict: 'Misleading', confidence: 84, date: 'Sep 22, 2026', time: '04:11 PM', domain: 'Seller Policy' },
  { id: 6, claim: 'Anker 65W GaN Charger sold by AnkerDirect is authentic.', verdict: 'Mostly True', confidence: 98, date: 'Sep 20, 2026', time: '10:05 AM', domain: 'Electronics' },
  { id: 7, claim: 'Nike Air Jordan 1 on DealMart is authorized stock.', verdict: 'False', confidence: 95, date: 'Sep 18, 2026', time: '01:30 PM', domain: 'Footwear & Apparel' },
  { id: 8, claim: 'Samsung 990 Pro 2TB SSD at $99 matches all-time low.', verdict: 'Mostly True', confidence: 92, date: 'Sep 15, 2026', time: '08:47 AM', domain: 'Computer Storage' },
]

export const SAVED_INVESTIGATIONS = [
  { id: 1, claim: 'AirPods Pro 2 for $29 are genuine Apple.', verdict: 'False', date: 'Oct 1, 2026', tags: ['Counterfeit', 'Electronics'] },
  { id: 2, claim: 'Sony WH-1000XM5 70% off flash deal.', verdict: 'Misleading', date: 'Sep 29, 2026', tags: ['Deals', 'Price History'] },
  { id: 3, claim: 'Anker 65W GaN Charger from AnkerDirect.', verdict: 'Mostly True', date: 'Sep 20, 2026', tags: ['Authorized Seller', 'Safety'] },
]

export const SOURCES_PAGE = [
  { name: 'FakeSpot Product Intel', url: 'fakespot.com', type: 'Review & Counterfeit AI', credibility: 96, articles: 42000, lastUpdated: 'Oct 2025', country: 'USA', color: '#2563eb', initials: 'FS', verified: true },
  { name: 'CamelCamelCamel Price Tracker', url: 'camelcamelcamel.com', type: 'Price History Engine', credibility: 98, articles: 85000, lastUpdated: 'Oct 2025', country: 'Global', color: '#f59e0b', initials: 'CCC', verified: true },
  { name: 'Trustpilot Merchant Platform', url: 'trustpilot.com', type: 'Consumer Review Registry', credibility: 91, articles: 120000, lastUpdated: 'Oct 2025', country: 'Global', color: '#10b981', initials: 'TP', verified: true },
  { name: 'Better Business Bureau (BBB)', url: 'bbb.org', type: 'Consumer Protection Bureau', credibility: 95, articles: 34000, lastUpdated: 'Oct 2025', country: 'USA', color: '#0284c7', initials: 'BBB', verified: true },
  { name: 'Consumer Product Safety Commission', url: 'cpsc.gov', type: 'Government Safety Agency', credibility: 99, articles: 9500, lastUpdated: 'Sep 2025', country: 'USA', color: '#dc2626', initials: 'CPSC', verified: true },
  { name: 'Brand Registry & Trademark Database', url: 'uspto.gov', type: 'Trademark Authority', credibility: 99, articles: 56000, lastUpdated: 'Oct 2025', country: 'USA', color: '#4f46e5', initials: 'TM', verified: true },
  { name: 'Consumer Reports Product Lab', url: 'consumerreports.org', type: 'Independent Testing Lab', credibility: 97, articles: 18000, lastUpdated: 'Oct 2025', country: 'USA', color: '#0891b2', initials: 'CR', verified: true },
  { name: 'ReviewMeta Audit Engine', url: 'reviewmeta.com', type: 'Review Algorithmic Auditor', credibility: 92, articles: 27000, lastUpdated: 'Oct 2025', country: 'Global', color: '#7c3aed', initials: 'RM', verified: true },
]

export const COLLECTIONS = [
  { id: 1, name: 'Counterfeit & Replica Alerts', description: 'Audits of knockoff electronics, cloned serials, and uncertified goods.', count: 28, color: '#ef4444', icon: '🛡️' },
  { id: 2, name: 'Fake Discount & Price History', description: 'Deceptive anchor MSRPs, artificial flash deals, and true price floors.', count: 19, color: '#f59e0b', icon: '🏷️' },
  { id: 3, name: 'Review Farm Detection', description: 'Incentivized review syndicates, bot ratings, and gift-card astroturfing.', count: 34, color: '#3b82f6', icon: '⭐' },
  { id: 4, name: 'Sneakers & Luxury Fashion', description: 'Authentication checks for sneakers, designer bags, and premium fabrics.', count: 22, color: '#8b5cf6', icon: '👟' },
  { id: 5, name: 'Seller Credibility & Return Scams', description: 'Restocking fee traps, ghost merchants, and warranty guarantee validity.', count: 15, color: '#10b981', icon: '📦' },
]

export const KNOWLEDGE_GRAPH_NODES = [
  { id: 'product', label: 'AirPods Pro 2', x: 50, y: 25, size: 22, color: '#ef4444' },
  { id: 'seller', label: 'SuperDeals Merchant', x: 25, y: 55, size: 16, color: '#f59e0b' },
  { id: 'fakespot', label: 'FakeSpot Intel', x: 75, y: 50, size: 18, color: '#2563eb' },
  { id: 'camel', label: 'CamelCamelCamel', x: 65, y: 75, size: 15, color: '#f59e0b' },
  { id: 'apple', label: 'Apple Registry', x: 20, y: 78, size: 13, color: '#0f172a' },
  { id: 'bbb', label: 'BBB Bureau', x: 82, y: 22, size: 14, color: '#0284c7' },
]

export const DOMAIN_INSIGHTS = [
  { domain: 'Consumer Electronics', total: 64, falseRate: 58, misleadingRate: 24, trueRate: 18, topClaim: 'Counterfeit audio & chargers', color: '#ef4444' },
  { domain: 'Price & Flash Sales', total: 42, falseRate: 35, misleadingRate: 48, trueRate: 17, topClaim: 'Inflated original MSRP', color: '#f59e0b' },
  { domain: 'Customer Reviews', total: 53, falseRate: 62, misleadingRate: 26, trueRate: 12, topClaim: 'Incentivized review syndicates', color: '#3b82f6' },
  { domain: 'Footwear & Fashion', total: 38, falseRate: 54, misleadingRate: 31, trueRate: 15, topClaim: 'Replica sneakers & fabrics', color: '#8b5cf6' },
  { domain: 'Seller & Return Terms', total: 29, falseRate: 28, misleadingRate: 52, trueRate: 20, topClaim: 'Hidden overseas return fee', color: '#10b981' },
]
