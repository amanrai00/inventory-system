/**
 * Client-side i18n for EN/JA language support.
 * Language stored in localStorage. Applied via data-i18n attributes.
 * data-i18n="key"            → sets textContent
 * data-i18n-placeholder="key" → sets placeholder
 * data-i18n-title="key"      → sets title/aria-label
 * data-i18n-html="key"       → sets innerHTML (use sparingly)
 */
(function () {
  var TRANSLATIONS = {
    en: {
      // Brand
      'brand.name': 'Inventory System',
      'brand.tagline': 'Management',

      // Nav
      'nav.menu': 'Menu',
      'nav.dashboard': 'Dashboard',
      'nav.products': 'Products',
      'nav.add_product': 'Add Product',
      'nav.record_sale': 'Record Sale',
      'nav.sales_history': 'Sales History',
      'nav.sign_out': 'Sign out',

      // Footer
      'footer.name': 'Inventory System',
      'footer.tagline': 'Stock control · Products · Sales',

      // Skip link
      'a11y.skip': 'Skip to main content',

      // Login page
      'login.title': 'Sign In - Inventory System',
      'login.heading': 'Sign in',
      'login.subheading': 'Enter your credentials to continue.',
      'login.email': 'Email',
      'login.email.placeholder': 'you@company.com',
      'login.password': 'Password',
      'login.password.placeholder': 'Enter password',
      'login.submit': 'Sign In',
      'login.footer': 'For access issues, contact your administrator.',
      'login.lang.label': 'Language',

      // Validation — login
      'login.error.email_required': 'Email is required.',
      'login.error.password_required': 'Password is required.',
      'login.error.invalid_credentials': 'Invalid email or password.',
      'login.message.success': 'Login successful!',
      'login.message.logged_out': 'You have been logged out.',

      // Dashboard
      'dashboard.title': 'Dashboard - Inventory System',
      'dashboard.eyebrow': 'Overview',
      'dashboard.page_title': 'Dashboard',
      'dashboard.btn.add_product': 'Add Product',
      'dashboard.btn.record_sale': 'Record Sale',
      'dashboard.metric.products': 'Products',
      'dashboard.metric.total_products': 'Total Products',
      'dashboard.metric.watch': 'Watch',
      'dashboard.metric.low_stock': 'Low Stock',
      'dashboard.metric.critical': 'Critical',
      'dashboard.metric.out_of_stock': 'Out of Stock',
      'dashboard.metric.sales': 'Sales',
      'dashboard.metric.total_sales': 'Total Sales',
      'dashboard.stock.eyebrow': 'Inventory',
      'dashboard.stock.heading': 'Stock breakdown',
      'dashboard.quick_actions.eyebrow': 'Quick Actions',
      'dashboard.quick_actions.view_inventory': 'View Inventory',
      'dashboard.critical.eyebrow': 'Needs Attention',
      'dashboard.critical.heading': 'Low & out of stock',
      'dashboard.critical.btn_all': 'All Products',
      'dashboard.critical.th_product': 'Product',
      'dashboard.critical.th_sku': 'SKU',
      'dashboard.critical.th_stock': 'Stock',
      'dashboard.critical.th_min': 'Min',
      'dashboard.critical.th_status': 'Status',
      'dashboard.critical.empty_heading': 'Everything looks good.',
      'dashboard.critical.empty_sub': 'No products below their minimum threshold.',
      'dashboard.recent.eyebrow': 'Recent',
      'dashboard.recent.heading': 'Latest sales',
      'dashboard.recent.btn_all': 'All Sales',
      'dashboard.recent.empty_heading': 'No sales yet.',
      'dashboard.recent.empty_sub': 'Record your first sale to see it here.',
      'dashboard.ai.eyebrow': 'Powered by Amazon Bedrock',
      'dashboard.ai.heading': 'AI Restock Recommendations',
      'dashboard.ai.empty_heading': 'No predictions yet.',
      'dashboard.ai.empty_sub': 'Run python3 scripts/predict.py to generate them.',
      'dashboard.alert.out_of_stock.btn': 'Review',
      'dashboard.alert.out_of_stock.sub': 'These need restocking before they can be sold.',
      'dashboard.alert.low_stock.btn': 'View',
      'dashboard.alert.healthy.heading': 'Stock levels are healthy',
      'dashboard.alert.healthy.sub': 'All products are above their minimum thresholds.',
      'dashboard.alert.healthy.btn': 'View Inventory',

      // Products list
      'products.title': 'Products - Inventory System',
      'products.eyebrow': 'Catalog',
      'products.page_title': 'Products',
      'products.btn.add': 'Add Product',
      'products.filter.eyebrow': 'All Products',
      'products.filter.search.label': 'Search',
      'products.filter.search.placeholder': 'Name or SKU',
      'products.filter.status.label': 'Status',
      'products.filter.status.all': 'All Statuses',
      'products.filter.status.normal': 'Normal',
      'products.filter.status.low_stock': 'Low Stock',
      'products.filter.status.out_of_stock': 'Out of Stock',
      'products.filter.btn.filter': 'Filter',
      'products.filter.btn.reset': 'Reset',
      'products.th.id': 'ID',
      'products.th.name': 'Name',
      'products.th.sku': 'SKU',
      'products.th.price': 'Price',
      'products.th.stock': 'Stock',
      'products.th.min': 'Min',
      'products.th.status': 'Status',
      'products.status.normal': 'Normal',
      'products.status.low_stock': 'Low Stock',
      'products.status.out_of_stock': 'Out of Stock',
      'products.btn.edit': 'Edit',
      'products.empty.heading': 'No products found.',
      'products.empty.sub': 'Try adjusting your search or status filter.',

      // Add product
      'add_product.title': 'Add Product - Inventory System',
      'add_product.eyebrow': 'Catalog',
      'add_product.page_title': 'Add Product',
      'add_product.section.eyebrow': 'New Product',
      'add_product.section.heading': 'Product details',
      'add_product.field.name': 'Product Name',
      'add_product.field.name.placeholder': 'e.g. Blue Widget',
      'add_product.field.sku': 'SKU',
      'add_product.field.sku.placeholder': 'e.g. SKU-001',
      'add_product.field.price': 'Price ($)',
      'add_product.field.price.placeholder': '0.00',
      'add_product.field.stock_qty': 'Stock Quantity',
      'add_product.field.stock_qty.placeholder': '0',
      'add_product.field.min_stock': 'Minimum Stock Level',
      'add_product.field.min_stock.placeholder': '0',
      'add_product.field.min_stock.hint': 'Dashboard alerts trigger when stock falls below this number.',
      'add_product.btn.submit': 'Add Product',
      'add_product.btn.cancel': 'Cancel',
      'add_product.tips.heading': 'Tips',
      'add_product.tips.sku': '— Keep it short, unique, and consistent with your labelling system.',
      'add_product.tips.price': '— Use the price customers pay, not cost price.',
      'add_product.tips.min_stock': '— Set this to the point where you\'d want to reorder, not zero.',

      // Edit product
      'edit_product.title': 'Edit Product - Inventory System',
      'edit_product.eyebrow': 'Catalog',
      'edit_product.page_title': 'Edit Product',
      'edit_product.section.eyebrow': 'Edit Product',
      'edit_product.field.name': 'Product Name',
      'edit_product.field.sku': 'SKU',
      'edit_product.field.price': 'Price ($)',
      'edit_product.field.stock_qty': 'Stock Quantity',
      'edit_product.field.min_stock': 'Minimum Stock Level',
      'edit_product.field.min_stock.hint': 'Stock alerts trigger when on-hand quantity falls below this.',
      'edit_product.btn.submit': 'Save Changes',
      'edit_product.btn.cancel': 'Cancel',
      'edit_product.tips.heading': 'Things to check',
      'edit_product.tips.stock_qty': '— Should match the actual count on your shelves.',
      'edit_product.tips.min_stock': '— Raise it if alerts are coming too late, lower it if they\'re too noisy.',
      'edit_product.tips.price': '— Update if the sale price has changed.',

      // Record sale
      'record_sale.title': 'Record Sale - Inventory System',
      'record_sale.eyebrow': 'Sales',
      'record_sale.page_title': 'Record Sale',
      'record_sale.section.eyebrow': 'New Sale',
      'record_sale.section.heading': 'Record a transaction',
      'record_sale.field.product': 'Product',
      'record_sale.field.product.placeholder': 'Search by name or SKU...',
      'record_sale.field.qty': 'Quantity Sold',
      'record_sale.field.qty.placeholder': '1',
      'record_sale.available': 'Available:',
      'record_sale.units': 'units',
      'record_sale.btn.change': 'Change',
      'record_sale.btn.submit': 'Record Sale',
      'record_sale.btn.cancel': 'Cancel',
      'record_sale.error.product': 'Please select a product.',
      'record_sale.no_results': 'No products found.',
      'record_sale.tips.heading': 'Before you submit',
      'record_sale.tips.product': '— Search by name or SKU. Stock level is shown in the dropdown.',
      'record_sale.tips.qty': '— Can\'t exceed available stock. Whole numbers only.',
      'record_sale.tips.duplicates': '— Submit once and wait for confirmation.',
      'record_sale.status.out_of_stock': 'Out of Stock',
      'record_sale.status.left': 'left',
      'record_sale.status.in_stock': 'in stock',

      // Sales history
      'sales_history.title': 'Sales History - Inventory System',
      'sales_history.eyebrow': 'Sales',
      'sales_history.page_title': 'Sales History',
      'sales_history.btn.record': 'Record Sale',
      'sales_history.filter.eyebrow': 'Transaction Log',
      'sales_history.filter.product.label': 'Product',
      'sales_history.filter.product.placeholder': 'Search product',
      'sales_history.filter.from.label': 'From',
      'sales_history.filter.to.label': 'To',
      'sales_history.filter.btn.filter': 'Filter',
      'sales_history.filter.btn.reset': 'Reset',
      'sales_history.th.id': 'Sale ID',
      'sales_history.th.product': 'Product',
      'sales_history.th.qty': 'Qty Sold',
      'sales_history.th.date': 'Date',
      'sales_history.empty.heading': 'No sales found.',
      'sales_history.empty.sub': 'Try a different product name or date range.',

      // Common status pills
      'status.out_of_stock': 'Out of Stock',
      'status.low_stock': 'Low Stock',
      'status.normal': 'Normal',
      'status.restock': 'Restock',
      'status.units': 'units',

      // Common actions
      'action.edit': 'Edit',
      'action.review': 'Review',
      'action.view': 'View',

      // Product validation errors
      'validation.product.name_required': '商品名を入力してください。',
      'validation.product.sku_required': 'SKUを入力してください。',
      'validation.product.price_positive': 'Price must be greater than 0.',
      'validation.product.price_invalid': 'Price must be a valid number.',
      'validation.product.stock_negative': 'Stock quantity cannot be negative.',
      'validation.product.stock_invalid': 'Stock quantity must be a whole number.',
      'validation.product.min_stock_negative': 'Minimum stock must be 0 or more.',
      'validation.product.min_stock_invalid': 'Minimum stock level must be a whole number.',
      'validation.product.sku_duplicate': 'SKU already exists. Use a unique SKU for each product.',
    },

    ja: {
      // Brand
      'brand.name': '在庫管理システム',
      'brand.tagline': '在庫管理',

      // Nav
      'nav.menu': 'メニュー',
      'nav.dashboard': 'ダッシュボード',
      'nav.products': '商品一覧',
      'nav.add_product': '商品追加',
      'nav.record_sale': '売上登録',
      'nav.sales_history': '売上履歴',
      'nav.sign_out': 'ログアウト',

      // Footer
      'footer.name': '在庫管理システム',
      'footer.tagline': '在庫管理 · 商品 · 売上',

      // Skip link
      'a11y.skip': 'メインコンテンツへスキップ',

      // Login page
      'login.title': 'ログイン - 在庫管理システム',
      'login.heading': 'ログイン',
      'login.subheading': 'メールアドレスとパスワードを入力してください。',
      'login.email': 'メールアドレス',
      'login.email.placeholder': 'you@example.com',
      'login.password': 'パスワード',
      'login.password.placeholder': '••••••••',
      'login.submit': 'ログイン',
      'login.footer': 'ログインできない場合は管理者にご連絡ください。',
      'login.lang.label': '言語',

      // Validation — login
      'login.error.email_required': '\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002',
      'login.error.password_required': '\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002',
      'login.error.invalid_credentials': '\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9\u307e\u305f\u306f\u30d1\u30b9\u30ef\u30fc\u30c9\u304c\u6b63\u3057\u304f\u3042\u308a\u307e\u305b\u3093\u3002',
      'login.message.success': '\u30ed\u30b0\u30a4\u30f3\u3057\u307e\u3057\u305f\u3002',
      'login.message.logged_out': '\u30ed\u30b0\u30a2\u30a6\u30c8\u3057\u307e\u3057\u305f\u3002',

      // Dashboard
      'dashboard.title': 'ダッシュボード - 在庫管理システム',
      'dashboard.eyebrow': '概要',
      'dashboard.page_title': 'ダッシュボード',
      'dashboard.btn.add_product': '商品追加',
      'dashboard.btn.record_sale': '売上登録',
      'dashboard.metric.products': '商品',
      'dashboard.metric.total_products': '総商品数',
      'dashboard.metric.watch': '注意',
      'dashboard.metric.low_stock': '在庫少',
      'dashboard.metric.critical': '緊急',
      'dashboard.metric.out_of_stock': '在庫切れ',
      'dashboard.metric.sales': '売上',
      'dashboard.metric.total_sales': '総売上数',
      'dashboard.stock.eyebrow': '在庫',
      'dashboard.stock.heading': '在庫内訳',
      'dashboard.quick_actions.eyebrow': 'クイックアクション',
      'dashboard.quick_actions.view_inventory': '商品一覧',
      'dashboard.critical.eyebrow': '要対応',
      'dashboard.critical.heading': '在庫少・在庫切れ',
      'dashboard.critical.btn_all': '全商品',
      'dashboard.critical.th_product': '商品名',
      'dashboard.critical.th_sku': 'SKU',
      'dashboard.critical.th_stock': '在庫',
      'dashboard.critical.th_min': '最低',
      'dashboard.critical.th_status': 'ステータス',
      'dashboard.critical.empty_heading': '問題ありません。',
      'dashboard.critical.empty_sub': '最低在庫を下回っている商品はありません。',
      'dashboard.recent.eyebrow': '最近',
      'dashboard.recent.heading': '最新の売上',
      'dashboard.recent.btn_all': '全売上',
      'dashboard.recent.empty_heading': '売上がありません。',
      'dashboard.recent.empty_sub': '最初の売上を登録するとここに表示されます。',
      'dashboard.ai.eyebrow': 'Amazon Bedrock による予測',
      'dashboard.ai.heading': 'AI 補充推奨',
      'dashboard.ai.empty_heading': '予測データがありません。',
      'dashboard.ai.empty_sub': 'python3 scripts/predict.py を実行して生成してください。',
      'dashboard.alert.out_of_stock.btn': '確認',
      'dashboard.alert.out_of_stock.sub': '販売前に在庫を補充してください。',
      'dashboard.alert.low_stock.btn': '表示',
      'dashboard.alert.healthy.heading': '在庫は良好です',
      'dashboard.alert.healthy.sub': 'すべての商品が最低在庫を上回っています。',
      'dashboard.alert.healthy.btn': '在庫一覧',

      // Products list
      'products.title': '商品一覧 - 在庫管理システム',
      'products.eyebrow': 'カタログ',
      'products.page_title': '商品一覧',
      'products.btn.add': '商品追加',
      'products.filter.eyebrow': '全商品',
      'products.filter.search.label': '検索',
      'products.filter.search.placeholder': '名前またはSKU',
      'products.filter.status.label': 'ステータス',
      'products.filter.status.all': '全ステータス',
      'products.filter.status.normal': '通常',
      'products.filter.status.low_stock': '在庫少',
      'products.filter.status.out_of_stock': '在庫切れ',
      'products.filter.btn.filter': '絞り込み',
      'products.filter.btn.reset': 'リセット',
      'products.th.id': 'ID',
      'products.th.name': '商品名',
      'products.th.sku': 'SKU',
      'products.th.price': '価格',
      'products.th.stock': '在庫',
      'products.th.min': '最低',
      'products.th.status': 'ステータス',
      'products.status.normal': '通常',
      'products.status.low_stock': '在庫少',
      'products.status.out_of_stock': '在庫切れ',
      'products.btn.edit': '編集',
      'products.empty.heading': '商品が見つかりません。',
      'products.empty.sub': '検索条件またはステータスフィルターを変更してください。',

      // Add product
      'add_product.title': '商品追加 - 在庫管理システム',
      'add_product.eyebrow': 'カタログ',
      'add_product.page_title': '商品追加',
      'add_product.section.eyebrow': '新規商品',
      'add_product.section.heading': '商品詳細',
      'add_product.field.name': '商品名',
      'add_product.field.name.placeholder': '例：ブルーウィジェット',
      'add_product.field.sku': 'SKU',
      'add_product.field.sku.placeholder': '例：SKU-001',
      'add_product.field.price': '価格（円）',
      'add_product.field.price.placeholder': '0.00',
      'add_product.field.stock_qty': '在庫数量',
      'add_product.field.stock_qty.placeholder': '0',
      'add_product.field.min_stock': '最低在庫数',
      'add_product.field.min_stock.placeholder': '0',
      'add_product.field.min_stock.hint': 'この数を下回るとダッシュボードにアラートが表示されます。',
      'add_product.btn.submit': '商品を追加',
      'add_product.btn.cancel': 'キャンセル',
      'add_product.tips.heading': 'ヒント',
      'add_product.tips.sku': '— 短く、ユニークで、ラベルシステムと一致させてください。',
      'add_product.tips.price': '— 仕入れ価格ではなく、販売価格を入力してください。',
      'add_product.tips.min_stock': '— 在庫がゼロになる前に補充したい数量を設定してください。',

      // Edit product
      'edit_product.title': '商品編集 - 在庫管理システム',
      'edit_product.eyebrow': 'カタログ',
      'edit_product.page_title': '商品編集',
      'edit_product.section.eyebrow': '商品編集',
      'edit_product.field.name': '商品名',
      'edit_product.field.sku': 'SKU',
      'edit_product.field.price': '価格（円）',
      'edit_product.field.stock_qty': '在庫数量',
      'edit_product.field.min_stock': '最低在庫数',
      'edit_product.field.min_stock.hint': '在庫がこの数を下回るとアラートが発生します。',
      'edit_product.btn.submit': '変更を保存',
      'edit_product.btn.cancel': 'キャンセル',
      'edit_product.tips.heading': '確認事項',
      'edit_product.tips.stock_qty': '— 実際の棚の在庫数と一致させてください。',
      'edit_product.tips.min_stock': '— アラートが遅い場合は上げ、多すぎる場合は下げてください。',
      'edit_product.tips.price': '— 販売価格が変わった場合は更新してください。',

      // Record sale
      'record_sale.title': '売上登録 - 在庫管理システム',
      'record_sale.eyebrow': '売上',
      'record_sale.page_title': '売上登録',
      'record_sale.section.eyebrow': '新規売上',
      'record_sale.section.heading': '取引を登録',
      'record_sale.field.product': '商品',
      'record_sale.field.product.placeholder': '名前またはSKUで検索...',
      'record_sale.field.qty': '販売数量',
      'record_sale.field.qty.placeholder': '1',
      'record_sale.available': '在庫：',
      'record_sale.units': '個',
      'record_sale.btn.change': '変更',
      'record_sale.btn.submit': '売上を登録',
      'record_sale.btn.cancel': 'キャンセル',
      'record_sale.error.product': '商品を選択してください。',
      'record_sale.no_results': '商品が見つかりません。',
      'record_sale.tips.heading': '送信前の確認',
      'record_sale.tips.product': '— 名前またはSKUで検索。ドロップダウンに在庫数が表示されます。',
      'record_sale.tips.qty': '— 在庫数を超えることはできません。整数のみ。',
      'record_sale.tips.duplicates': '— 送信は1回のみ。確認を待ってください。',
      'record_sale.status.out_of_stock': '在庫切れ',
      'record_sale.status.left': '残り',
      'record_sale.status.in_stock': '在庫あり',

      // Sales history
      'sales_history.title': '売上履歴 - 在庫管理システム',
      'sales_history.eyebrow': '売上',
      'sales_history.page_title': '売上履歴',
      'sales_history.btn.record': '売上登録',
      'sales_history.filter.eyebrow': '取引ログ',
      'sales_history.filter.product.label': '商品',
      'sales_history.filter.product.placeholder': '商品を検索',
      'sales_history.filter.from.label': '開始日',
      'sales_history.filter.to.label': '終了日',
      'sales_history.filter.btn.filter': '絞り込み',
      'sales_history.filter.btn.reset': 'リセット',
      'sales_history.th.id': '売上ID',
      'sales_history.th.product': '商品名',
      'sales_history.th.qty': '販売数',
      'sales_history.th.date': '日付',
      'sales_history.empty.heading': '売上が見つかりません。',
      'sales_history.empty.sub': '別の商品名または日付範囲を試してください。',

      // Common status pills
      'status.out_of_stock': '在庫切れ',
      'status.low_stock': '在庫少',
      'status.normal': '通常',
      'status.restock': '補充',
      'status.units': '個',

      // Common actions
      'action.edit': '編集',
      'action.review': '確認',
      'action.view': '表示',

      // Product validation errors
      'validation.product.name_required': '商品名を入力してください。',
      'validation.product.sku_required': 'SKUを入力してください。',
      'validation.product.price_positive': '価格は0より大きい値を入力してください。',
      'validation.product.price_invalid': '価格に有効な数値を入力してください。',
      'validation.product.stock_negative': '在庫数量は0以上で入力してください。',
      'validation.product.stock_invalid': '在庫数量は整数で入力してください。',
      'validation.product.min_stock_negative': '最低在庫数は0以上で入力してください。',
      'validation.product.min_stock_invalid': '最低在庫数は整数で入力してください。',
      'validation.product.sku_duplicate': 'このSKUはすでに使用されています。別のSKUを入力してください。',
    }
  };

  var DEFAULT_LANG = 'en';
  var STORAGE_KEY = 'inv_lang';
  var ROLE_TRANSLATIONS = {
    ja: {
      admin: '\u7ba1\u7406\u8005'
    }
  };

  function getLang() {
    try {
      return localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG;
    } catch (e) {
      return DEFAULT_LANG;
    }
  }

  function setLang(lang) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {}
  }

  function t(key) {
    var lang = getLang();
    var dict = TRANSLATIONS[lang] || TRANSLATIONS[DEFAULT_LANG];
    return dict[key] !== undefined ? dict[key] : (TRANSLATIONS[DEFAULT_LANG][key] || key);
  }

  function translateRoleLabel(role) {
    var lang = getLang();
    var normalizedRole = (role || '').trim().toLowerCase();
    var translatedRole = ROLE_TRANSLATIONS[lang] && ROLE_TRANSLATIONS[lang][normalizedRole];
    return translatedRole || role;
  }

  function translateDashboardStatusLabel(label) {
    var lang = getLang();
    if (lang !== 'ja') return label;

    if (label === 'Normal') return '通常';
    if (label === 'Low Stock') return '在庫少';
    if (label === 'Out of Stock') return '在庫切れ';
    return label;
  }

  function formatDashboardOutOfStockCount(count) {
    var lang = getLang();
    var numericCount = parseInt(count, 10);

    if (lang === 'ja') {
      return numericCount + ' 件';
    }

    return numericCount + ' item' + (numericCount !== 1 ? 's' : '') + ' out of stock';
  }

  function formatProductCount(count) {
    var lang = getLang();
    var numericCount = parseInt(count, 10);

    if (isNaN(numericCount) || numericCount <= 0) {
      return lang === 'ja' ? '結果なし' : 'No results';
    }

    if (lang === 'ja') {
      return numericCount + ' 件';
    }

    return numericCount + ' item' + (numericCount !== 1 ? 's' : '');
  }

  function applyTranslations() {
    var lang = getLang();

    // Update <html lang>
    document.documentElement.lang = lang;

    // Update <title> if data-i18n-title-key set on <title> tag
    var titleEl = document.querySelector('title[data-i18n]');
    if (titleEl) {
      titleEl.textContent = t(titleEl.getAttribute('data-i18n'));
    }

    // Text content
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      if (el.tagName === 'TITLE') return;
      el.textContent = t(el.getAttribute('data-i18n'));
    });

    // Placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
      el.placeholder = t(el.getAttribute('data-i18n-placeholder'));
    });

    // title / aria-label
    document.querySelectorAll('[data-i18n-aria]').forEach(function (el) {
      var val = t(el.getAttribute('data-i18n-aria'));
      el.setAttribute('title', val);
      el.setAttribute('aria-label', val);
    });

    // innerHTML (for mixed content)
    document.querySelectorAll('[data-i18n-html]').forEach(function (el) {
      el.innerHTML = t(el.getAttribute('data-i18n-html'));
    });

    // Dynamic role labels coming from the server session
    document.querySelectorAll('[data-role-label]').forEach(function (el) {
      el.textContent = translateRoleLabel(el.getAttribute('data-role-label'));
    });

    document.querySelectorAll('[data-dashboard-status-label]').forEach(function (el) {
      el.textContent = translateDashboardStatusLabel(el.getAttribute('data-dashboard-status-label'));
    });

    document.querySelectorAll('[data-dashboard-out-of-stock-count]').forEach(function (el) {
      el.textContent = formatDashboardOutOfStockCount(el.getAttribute('data-dashboard-out-of-stock-count'));
    });

    document.querySelectorAll('[data-product-count]').forEach(function (el) {
      el.textContent = formatProductCount(el.getAttribute('data-product-count'));
    });

    document.querySelectorAll('[data-prediction-en]').forEach(function (el) {
      el.textContent = lang === 'ja'
        ? (el.getAttribute('data-prediction-ja') || el.getAttribute('data-prediction-en'))
        : el.getAttribute('data-prediction-en');
    });

    // Update language switcher buttons active state
    document.querySelectorAll('[data-lang-btn]').forEach(function (btn) {
      var isActive = btn.getAttribute('data-lang-btn') === lang;
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
      btn.classList.toggle('lang-btn-active', isActive);
    });

    document.body.classList.add('page-ready');
  }

  function initSwitcher() {
    document.querySelectorAll('[data-lang-btn]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var lang = this.getAttribute('data-lang-btn');
        setLang(lang);
        applyTranslations();
        fetch('/set-lang/' + lang);
        document.cookie = 'lang=' + lang + '; path=/';
      });
    });
  }

  // Public API
  window.I18n = {
    t: t,
    getLang: getLang,
    setLang: setLang,
    apply: applyTranslations
  };

  // Auto-apply on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      applyTranslations();
      initSwitcher();
    });
  } else {
    applyTranslations();
    initSwitcher();
  }
})();
