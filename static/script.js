// DOM Elements
const navBar = document.getElementById('navBar');
const navCreateBtn = document.getElementById('navCreate');
const chartForm = document.getElementById('chartForm');
const generateBtn = document.getElementById('generateBtn');
const downloadBtn = document.getElementById('downloadBtn');
const chartImage = document.getElementById('chartImage');
const placeholder = document.getElementById('placeholder');
const assetSearch = document.getElementById('assetSearch');
const searchSuggestions = document.getElementById('searchSuggestions');
const tickerInput = document.getElementById('ticker');
const compareTickerInput = document.getElementById('compareTicker');
const categoryTabs = document.getElementById('categoryTabs');
const assetGrid = document.getElementById('assetGrid');

// Sections for scrolling
const sectionAsset = document.getElementById('section-asset');
const sectionTimeframe = document.getElementById('section-timeframe');
const sectionCustomize = document.getElementById('section-customize');
const sectionBackground = document.getElementById('section-background');
const sectionChart = document.getElementById('section-chart');
const leaderboardSection = document.getElementById('newsLeaderboardSection');

// Asset Data
const assetData = [
    // Crypto
    { ticker: 'BTC-USD', name: 'Bitcoin', icon: '₿', category: 'Crypto' },
    { ticker: 'ETH-USD', name: 'Ethereum', icon: 'Ξ', category: 'Crypto' },
    { ticker: 'SOL-USD', name: 'Solana', icon: '◎', category: 'Crypto' },
    { ticker: 'XRP-USD', name: 'XRP', icon: '✕', category: 'Crypto' },
    { ticker: 'ADA-USD', name: 'Cardano', icon: '₳', category: 'Crypto' },
    { ticker: 'DOGE-USD', name: 'Dogecoin', icon: 'Ð', category: 'Crypto' },
    { ticker: 'AVAX-USD', name: 'Avalanche', icon: '🔺', category: 'Crypto' },
    { ticker: 'DOT-USD', name: 'Polkadot', icon: '●', category: 'Crypto' },
    { ticker: 'MATIC-USD', name: 'Polygon', icon: 'Ⓜ', category: 'Crypto' },
    { ticker: 'LTC-USD', name: 'Litecoin', icon: 'Ł', category: 'Crypto' },
    { ticker: 'UNI-USD', name: 'Uniswap', icon: '🦄', category: 'Crypto' },
    { ticker: 'LINK-USD', name: 'Chainlink', icon: '🔗', category: 'Crypto' },
    { ticker: 'ATOM-USD', name: 'Cosmos', icon: '⚛', category: 'Crypto' },
    { ticker: 'XMR-USD', name: 'Monero', icon: 'ɱ', category: 'Crypto' },
    { ticker: 'BCH-USD', name: 'Bitcoin Cash', icon: 'Ƀ', category: 'Crypto' },
    { ticker: 'ALGO-USD', name: 'Algorand', icon: 'Ⱥ', category: 'Crypto' },

    // Stocks
    { ticker: 'AAPL', name: 'Apple', icon: '', category: 'Stocks' },
    { ticker: 'MSFT', name: 'Microsoft', icon: '⊞', category: 'Stocks' },
    { ticker: 'GOOGL', name: 'Google', icon: 'G', category: 'Stocks' },
    { ticker: 'AMZN', name: 'Amazon', icon: 'a', category: 'Stocks' },
    { ticker: 'TSLA', name: 'Tesla', icon: '⚡', category: 'Stocks' },
    { ticker: 'NVDA', name: 'NVIDIA', icon: '◆', category: 'Stocks' },
    { ticker: 'META', name: 'Meta', icon: '∞', category: 'Stocks' },
    { ticker: 'NFLX', name: 'Netflix', icon: 'N', category: 'Stocks' },
    { ticker: 'AMD', name: 'AMD', icon: '∰', category: 'Stocks' },
    { ticker: 'INTC', name: 'Intel', icon: 'i', category: 'Stocks' },
    { ticker: 'COIN', name: 'Coinbase', icon: 'C', category: 'Stocks' },
    { ticker: 'HOOD', name: 'Robinhood', icon: '🏹', category: 'Stocks' },
    { ticker: 'PLTR', name: 'Palantir', icon: 'P', category: 'Stocks' },
    { ticker: 'UBER', name: 'Uber', icon: 'U', category: 'Stocks' },
    { ticker: 'ABNB', name: 'Airbnb', icon: '🏠', category: 'Stocks' },
    { ticker: 'SQ', name: 'Block', icon: '□', category: 'Stocks' },

    // Indices
    { ticker: '^GSPC', name: 'S&P 500', icon: '🇺🇸', category: 'Indices' },
    { ticker: '^DJI', name: 'Dow Jones', icon: '🏭', category: 'Indices' },
    { ticker: '^IXIC', name: 'Nasdaq', icon: '💻', category: 'Indices' },
    { ticker: '^RUT', name: 'Russell 2000', icon: 'R', category: 'Indices' },
    { ticker: '^FTSE', name: 'FTSE 100', icon: '🇬🇧', category: 'Indices' },
    { ticker: '^N225', name: 'Nikkei 225', icon: '🇯🇵', category: 'Indices' },
    { ticker: '^GDAXI', name: 'DAX', icon: '🇩🇪', category: 'Indices' },
    { ticker: '^HSI', name: 'Hang Seng', icon: '🇭🇰', category: 'Indices' },

    // Forex
    { ticker: 'EURUSD=X', name: 'EUR/USD', icon: '🇪🇺', category: 'Forex' },
    { ticker: 'GBPUSD=X', name: 'GBP/USD', icon: '🇬🇧', category: 'Forex' },
    { ticker: 'JPY=X', name: 'USD/JPY', icon: '🇯🇵', category: 'Forex' },
    { ticker: 'CHF=X', name: 'USD/CHF', icon: '🇨🇭', category: 'Forex' },
    { ticker: 'AUDUSD=X', name: 'AUD/USD', icon: '🇦🇺', category: 'Forex' },
    { ticker: 'USDCAD=X', name: 'USD/CAD', icon: '🇨🇦', category: 'Forex' },

    // Commodities
    { ticker: 'GC=F', name: 'Gold Futures', icon: '🥇', category: 'Commodities' },
    { ticker: 'SI=F', name: 'Silver Futures', icon: '🥈', category: 'Commodities' },
    { ticker: 'CL=F', name: 'Crude Oil', icon: '🛢', category: 'Commodities' },
    { ticker: 'NG=F', name: 'Natural Gas', icon: '🔥', category: 'Commodities' },
    { ticker: 'HG=F', name: 'Copper', icon: '🥉', category: 'Commodities' },
    { ticker: 'ZC=F', name: 'Corn', icon: '🌽', category: 'Commodities' },

    // Economic Indicators (FRED)
    { ticker: 'fed_funds_rate', name: 'Fed Funds Rate', icon: '🏦', category: 'Economic' },
    { ticker: 'treasury_10y', name: '10Y Treasury Yield', icon: '📈', category: 'Economic' },
    { ticker: 'treasury_2y', name: '2Y Treasury Yield', icon: '📊', category: 'Economic' },
    { ticker: 'cpi_yoy', name: 'CPI YoY', icon: '💰', category: 'Economic' },
    { ticker: 'unemployment', name: 'Unemployment Rate', icon: '👥', category: 'Economic' },
    { ticker: 'dxy', name: 'Dollar Index (DXY)', icon: '💵', category: 'Economic' },
    { ticker: 'gdp', name: 'GDP Growth', icon: '📈', category: 'Economic' },
    { ticker: 'pmi', name: 'Manufacturing PMI', icon: '🏭', category: 'Economic' },
    { ticker: 'ism_services', name: 'ISM Services PMI', icon: '🏢', category: 'Economic' },

    // On-Chain Metrics
    { ticker: 'BTC.D', name: 'Bitcoin Dominance', icon: '👑', category: 'On-Chain' },
    { ticker: 'USDT.D', name: 'Tether Dominance', icon: '💎', category: 'On-Chain' },
    { ticker: 'ETH-BTC', name: 'ETH/BTC Ratio', icon: '⚖️', category: 'On-Chain' },
    { ticker: 'TOTAL2', name: 'Total2 Market Cap', icon: '📊', category: 'On-Chain' },
    { ticker: 'TOTAL3', name: 'Total3 Market Cap', icon: '📈', category: 'On-Chain' },
    { ticker: 'OTHERS.D', name: 'Others Dominance', icon: '🔄', category: 'On-Chain' },
    { ticker: 'USDC-USD', name: 'USDC (Stablecoin)', icon: '💰', category: 'On-Chain' },
    { ticker: 'USDT-USD', name: 'USDT (Stablecoin)', icon: '💵', category: 'On-Chain' },
    { ticker: 'BTC-USD', name: 'Bitcoin Price', icon: '₿', category: 'On-Chain' },
    { ticker: 'ETH-USD', name: 'Ethereum Price', icon: 'Ξ', category: 'On-Chain' }
];

// Allowed Candle Intervals per Period
const allowedIntervals = {
    '1d': ['1m', '5m', '15m', '1h'],
    '5d': ['5m', '15m', '1h', '1d'],
    '1mo': ['15m', '1h', '4h', '1d'],
    '3mo': ['1h', '4h', '1d'],
    '6mo': ['4h', '1d', '1w'],
    '1y': ['1d', '1w', '1mo'],
    '2y': ['1d', '1w', '1mo'],
    '5y': ['1d', '1w', '1mo'],
    '10y': ['1d', '1w', '1mo'],
    'max': ['1d', '1w', '1mo'],
    'ytd': ['1d', '1w', '1mo'],
    'custom': ['1d', '1w', '1mo']
};

// State
let selectedTickers = []; // Array to store selected tickers
let isMultiSelect = false;
let assetSettings = {}; // { ticker: { chartType, color, scale, priceAxis, timeAxis, candleInterval } }per-asset settings

// Default settings for an asset
function getDefaultSettings(ticker, isPrimary) {
    return {
        ticker: ticker,
        chartType: isPrimary ? 'candle' : 'line',
        color: isPrimary ? '#0066FF' : '#FF9500',
        upColor: '#10B981',   // Green for bullish candles
        downColor: '#EF4444', // Red for bearish candles
        scale: 'linear', // linear, log, percentage
        priceAxis: 'left',
        timeAxis: 'bottom',
        candleInterval: '1d' // For candle charts: 1m, 5m, 15m, 1h, 4h, 1d, 1w, 1mo
    };
}

function updateHiddenInputs() {
    if (selectedTickers.length > 0) {
        // First selected is primary
        tickerInput.value = selectedTickers[0];

        // Rest are comparisons
        if (selectedTickers.length > 1) {
            compareTickerInput.value = selectedTickers.slice(1).join(',');
        } else {
            compareTickerInput.value = '';
        }
    } else {
        tickerInput.value = '';
        compareTickerInput.value = '';
    }

    // Update customization sections and header
    renderCustomizationSections();
    updateCustomizationHeader();
    renderSelectedAssetsBar();
}

function removeTicker(ticker) {
    selectedTickers = selectedTickers.filter(t => t !== ticker);
    updateHiddenInputs();
    // Re-render asset grid to update active states
    const activeCategory = document.querySelector('.cat-tab.active') ? document.querySelector('.cat-tab.active').dataset.category : 'All';
    renderAssets(activeCategory);
}



function renderSelectedAssetsBar() {
    const bar = document.getElementById('selectedAssetsBar');
    if (selectedTickers.length === 0) {
        bar.classList.add('hidden');
        return;
    }

    bar.classList.remove('hidden');
    bar.innerHTML = selectedTickers.map(ticker => {
        const asset = assetData.find(a => a.ticker === ticker);
        const name = asset ? asset.name : ticker;
        const icon = asset ? asset.icon : '📊';

        return `
            <div class="asset-chip">
                <span class="asset-chip-icon">${icon}</span>
                <span class="asset-chip-name">${name}</span>
                <button type="button" class="asset-chip-remove" data-ticker="${ticker}" title="Remove">✕</button>
            </div>
        `;
    }).join('');

    // Attach listeners
    bar.querySelectorAll('.asset-chip-remove').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            removeTicker(btn.dataset.ticker);
        });
    });
}

function updateCustomizationHeader() {
    const headerElement = document.getElementById('customizingAssets');

    if (selectedTickers.length === 0) {
        headerElement.textContent = 'Select an asset to begin';
        return;
    }

    // Build display string with asset names and icons
    const assetNames = selectedTickers.map(ticker => {
        const asset = assetData.find(a => a.ticker === ticker);
        if (asset) {
            // For short display, use icon + short name
            const shortName = asset.ticker.split('-')[0];
            return `${asset.icon} ${shortName}`;
        }
        return ticker;
    });

    if (assetNames.length === 1) {
        headerElement.textContent = assetNames[0];
    } else {
        headerElement.textContent = assetNames.join(' + ');
    }
}

function renderCustomizationSections() {
    const container = document.getElementById('perAssetCustomization');

    if (selectedTickers.length === 0) {
        container.innerHTML = '';
        return;
    }

    // Ensure settings exist for all selected tickers
    selectedTickers.forEach((ticker, index) => {
        if (!assetSettings[ticker]) {
            assetSettings[ticker] = getDefaultSettings(ticker, index === 0);
        }
    });

    // Remove settings for unselected tickers
    Object.keys(assetSettings).forEach(ticker => {
        if (!selectedTickers.includes(ticker)) {
            delete assetSettings[ticker];
        }
    });

    // Render sections for each asset
    container.innerHTML = selectedTickers.map((ticker, index) => {
        const asset = assetData.find(a => a.ticker === ticker);
        const settings = assetSettings[ticker];
        const isPrimary = index === 0;

        const assetName = asset ? asset.name : ticker;
        const assetIcon = asset ? asset.icon : '📊';

        return `
            <div class="asset-customization-section" data-ticker="${ticker}">
                <div class="asset-section-header">
                    <div class="header-left">
                        <span class="asset-section-icon">${assetIcon}</span>
                        <span class="asset-section-name">${assetName}</span>
                        ${isPrimary ? '<span class="asset-section-badge">Primary</span>' : '<span class="asset-section-badge" style="background: #FF9500;">Overlay</span>'}
                    </div>
                    <button type="button" class="remove-asset-btn" data-ticker="${ticker}" title="Remove Asset">✕</button>
                </div>
                
                <div class="customization-grid">
                    <!-- Chart Type -->
                    <div class="control-card">
                        <label>Chart Type</label>
                        <div class="segmented-control asset-chart-type" data-ticker="${ticker}">
                            <button type="button" class="segment ${settings.chartType === 'candle' ? 'active' : ''}" data-value="candle">Candle</button>
                            <button type="button" class="segment ${settings.chartType === 'line' ? 'active' : ''}" data-value="line">Line</button>
                            <button type="button" class="segment ${settings.chartType === 'ohlc' ? 'active' : ''}" data-value="ohlc">OHLC</button>
                            <button type="button" class="segment ${settings.chartType === 'area' ? 'active' : ''}" data-value="area">Area</button>
                            <button type="button" class="segment ${settings.chartType === 'hollow_and_filled' ? 'active' : ''}" data-value="hollow_and_filled">Hollow</button>
                            <button type="button" class="segment ${settings.chartType === 'renko' ? 'active' : ''}" data-value="renko">Renko</button>
                            <button type="button" class="segment ${settings.chartType === 'pnf' ? 'active' : ''}" data-value="pnf">PnF</button>
                        </div>
                    </div>
                    
                    <!-- Candle Interval (shown only for candle charts) -->
                    ${settings.chartType === 'candle' || settings.chartType === 'ohlc' || settings.chartType === 'hollow_and_filled' ? (() => {
                const currentPeriod = document.getElementById('period').value || '1y';
                const validIntervals = allowedIntervals[currentPeriod] || allowedIntervals['1y'];
                const intervals = ['1m', '5m', '15m', '1h', '4h', '1d', '1w', '1mo'];

                return `
                        <div class="control-card candle-interval-card" data-ticker="${ticker}">
                            <label>Candle Timeframe</label>
                            <div class="segmented-control asset-candle-interval" data-ticker="${ticker}">
                                ${intervals.map(int => `
                                    <button type="button" class="segment ${settings.candleInterval === int ? 'active' : ''}" 
                                            data-value="${int}" 
                                            ${!validIntervals.includes(int) ? 'disabled style="opacity:0.3; pointer-events:none;"' : ''}>
                                        ${int}
                                    </button>
                                `).join('')}
                            </div>
                        </div>
                        `;
            })() : ''}
                    
                    <!-- Color -->
                    <!-- Color (Hidden for Candle/OHLC) -->
                    ${settings.chartType !== 'candle' && settings.chartType !== 'ohlc' && settings.chartType !== 'hollow_and_filled' ? `
                    <div class="control-card">
                        <label>Color</label>
                        <div class="color-picker-wrapper">
                            <input type="color" class="asset-color-picker" data-ticker="${ticker}" value="${settings.color}">
                        </div>
                    </div>
                    ` : ''}
                    
                    <!-- Candlestick Colors (shown only for candle charts) -->
                    ${settings.chartType === 'candle' || settings.chartType === 'ohlc' || settings.chartType === 'hollow_and_filled' ? `
                    <div class="control-card candle-colors-card" data-ticker="${ticker}">
                        <label>Candle Colors</label>
                        <div class="candle-color-grid">
                            <div class="candle-color-item">
                                <label class="candle-color-label">🟢 Up (Bullish)</label>
                                <input type="color" class="asset-up-color-picker" data-ticker="${ticker}" value="${settings.upColor || '#10B981'}">
                            </div>
                            <div class="candle-color-item">
                                <label class="candle-color-label">🔴 Down (Bearish)</label>
                                <input type="color" class="asset-down-color-picker" data-ticker="${ticker}" value="${settings.downColor || '#EF4444'}">
                            </div>
                        </div>
                    </div>
                    ` : ''}
                    
                    <!-- Scale -->
                    <div class="control-card">
                        <label>Scale</label>
                        <div class="segmented-control asset-scale" data-ticker="${ticker}">
                            <button type="button" class="segment ${settings.scale === 'linear' ? 'active' : ''}" data-value="linear">Linear</button>
                            <button type="button" class="segment ${settings.scale === 'log' ? 'active' : ''}" data-value="log">Log</button>
                            <button type="button" class="segment ${settings.scale === 'percentage' ? 'active' : ''}" data-value="percentage">%</button>
                        </div>
                    </div>
                    
                    <!-- Price Axis -->
                    <div class="control-card">
                        <label>Price Axis</label>
                        <div class="segmented-control asset-price-axis" data-ticker="${ticker}">
                            <button type="button" class="segment ${settings.priceAxis === 'left' ? 'active' : ''}" data-value="left">Left</button>
                            <button type="button" class="segment ${settings.priceAxis === 'right' ? 'active' : ''}" data-value="right">Right</button>
                        </div>
                    </div>
                    
                    <!-- Time Axis -->
                    <div class="control-card">
                        <label>Time Axis</label>
                        <div class="segmented-control asset-time-axis" data-ticker="${ticker}">
                            <button type="button" class="segment ${settings.timeAxis === 'bottom' ? 'active' : ''}" data-value="bottom">Bottom</button>
                            <button type="button" class="segment ${settings.timeAxis === 'top' ? 'active' : ''}" data-value="top">Top</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    }).join('');

    // Attach event listeners
    attachCustomizationListeners();

    // Update hidden input with serialized settings
    updatePerAssetSettingsInput();
}

function attachCustomizationListeners() {
    // Remove Asset Listeners
    document.querySelectorAll('.remove-asset-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const ticker = btn.dataset.ticker;
            removeTicker(ticker);
        });
    });

    // Chart type listeners
    document.querySelectorAll('.asset-chart-type').forEach(control => {
        const ticker = control.dataset.ticker;
        control.addEventListener('click', (e) => {
            if (e.target.classList.contains('segment')) {
                control.querySelectorAll('.segment').forEach(s => s.classList.remove('active'));
                e.target.classList.add('active');
                assetSettings[ticker].chartType = e.target.dataset.value;
                updatePerAssetSettingsInput();
                // Re-render to show/hide candle interval selector
                renderCustomizationSections();
            }
        });
    });

    // Candle interval listeners
    document.querySelectorAll('.asset-candle-interval').forEach(control => {
        const ticker = control.dataset.ticker;
        control.addEventListener('click', (e) => {
            if (e.target.classList.contains('segment')) {
                control.querySelectorAll('.segment').forEach(s => s.classList.remove('active'));
                e.target.classList.add('active');
                assetSettings[ticker].candleInterval = e.target.dataset.value;
                updatePerAssetSettingsInput();
            }
        });
    });

    // Color picker listeners
    document.querySelectorAll('.asset-color-picker').forEach(picker => {
        const ticker = picker.dataset.ticker;
        picker.addEventListener('input', (e) => {
            assetSettings[ticker].color = e.target.value;
            updatePerAssetSettingsInput();
        });
    });

    // Up color picker listeners
    document.querySelectorAll('.asset-up-color-picker').forEach(picker => {
        const ticker = picker.dataset.ticker;
        picker.addEventListener('input', (e) => {
            assetSettings[ticker].upColor = e.target.value;
            updatePerAssetSettingsInput();
        });
    });

    // Down color picker listeners
    document.querySelectorAll('.asset-down-color-picker').forEach(picker => {
        const ticker = picker.dataset.ticker;
        picker.addEventListener('input', (e) => {
            assetSettings[ticker].downColor = e.target.value;
            updatePerAssetSettingsInput();
        });
    });

    // Scale listeners
    document.querySelectorAll('.asset-scale').forEach(control => {
        const ticker = control.dataset.ticker;
        control.addEventListener('click', (e) => {
            if (e.target.classList.contains('segment')) {
                control.querySelectorAll('.segment').forEach(s => s.classList.remove('active'));
                e.target.classList.add('active');
                assetSettings[ticker].scale = e.target.dataset.value;
                updatePerAssetSettingsInput();
            }
        });
    });

    // Price axis listeners
    document.querySelectorAll('.asset-price-axis').forEach(control => {
        const ticker = control.dataset.ticker;
        control.addEventListener('click', (e) => {
            if (e.target.classList.contains('segment')) {
                control.querySelectorAll('.segment').forEach(s => s.classList.remove('active'));
                e.target.classList.add('active');
                assetSettings[ticker].priceAxis = e.target.dataset.value;
                updatePerAssetSettingsInput();
            }
        });
    });

    // Time axis listeners
    document.querySelectorAll('.asset-time-axis').forEach(control => {
        const ticker = control.dataset.ticker;
        control.addEventListener('click', (e) => {
            if (e.target.classList.contains('segment')) {
                control.querySelectorAll('.segment').forEach(s => s.classList.remove('active'));
                e.target.classList.add('active');
                assetSettings[ticker].timeAxis = e.target.dataset.value;
                updatePerAssetSettingsInput();
            }
        });
    });
}

function updatePerAssetSettingsInput() {
    const input = document.getElementById('perAssetSettings');
    input.value = JSON.stringify(assetSettings);
}

function renderAssets(category) {
    // Filter assets based on category, or show all if 'All' is selected
    const assets = category === 'All'
        ? assetData
        : assetData.filter(a => a.category === category);

    assetGrid.innerHTML = assets.map(asset => {
        // For economic indicators, show a clean version of the ticker
        let displayTicker = asset.ticker;
        if (asset.category === 'Economic') {
            displayTicker = asset.name.split(' ').slice(0, 2).join(' ');
        } else {
            displayTicker = asset.ticker.split('-')[0];
        }

        const isActive = selectedTickers.includes(asset.ticker) ? 'active' : '';

        return `
        <div class="asset-card ${isActive}" 
             data-ticker="${asset.ticker}" 
             data-name="${asset.name}">
            <div class="asset-icon">${asset.icon}</div>
            <div class="asset-ticker">${displayTicker}</div>
            <div class="asset-name">${asset.name}</div>
        </div>
    `;
    }).join('');

    // Add click handlers
    document.querySelectorAll('.asset-card').forEach(card => {
        card.addEventListener('click', () => {
            const ticker = card.dataset.ticker;
            const isMultiSelect = document.getElementById('multiSelectToggle').checked;

            if (isMultiSelect) {
                // Multi-Select Mode: Toggle selection
                if (selectedTickers.includes(ticker)) {
                    selectedTickers = selectedTickers.filter(t => t !== ticker);
                    card.classList.remove('active');
                } else {
                    selectedTickers.push(ticker);
                    card.classList.add('active');
                }
            } else {
                // Single Select Mode: Replace selection
                selectedTickers = [ticker];
                // Update visual state for all cards
                document.querySelectorAll('.asset-card').forEach(c => c.classList.remove('active'));
                card.classList.add('active');
            }

            updateHiddenInputs();

            // Scroll to next section only on first selection (if single select or first of multi)
            if (selectedTickers.length === 1 && !isMultiSelect) {
                sectionTimeframe.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });
}

// Category Switching
categoryTabs.addEventListener('click', (e) => {
    if (e.target.classList.contains('cat-tab')) {
        document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
        e.target.classList.add('active');
        renderAssets(e.target.dataset.category);
    }
});

// Initialize with 'All'
// Sync selectedTickers with input values
if (tickerInput.value) {
    selectedTickers = [tickerInput.value];
    if (compareTickerInput.value) {
        const compares = compareTickerInput.value.split(',');
        selectedTickers = selectedTickers.concat(compares);
    }
} else {
    // Default fallback
    selectedTickers = ['AAPL'];
    updateHiddenInputs();
}
renderAssets('All');

// Search Logic
assetSearch.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    if (query.length < 2) {
        searchSuggestions.classList.remove('active');
        return;
    }

    const matches = assetData.filter(asset =>
        asset.ticker.toLowerCase().includes(query) ||
        asset.name.toLowerCase().includes(query)
    );

    if (matches.length > 0) {
        searchSuggestions.innerHTML = matches.map(asset => `
            <div class="suggestion-item" data-ticker="${asset.ticker}">
                <span class="suggestion-name">${asset.name}</span>
                <span class="suggestion-ticker">${asset.ticker}</span>
            </div>
        `).join('');
        searchSuggestions.classList.add('active');
    } else {
        searchSuggestions.classList.remove('active');
    }
});

searchSuggestions.addEventListener('click', (e) => {
    const item = e.target.closest('.suggestion-item');
    if (item) {
        const ticker = item.dataset.ticker;
        const isMultiSelect = document.getElementById('multiSelectToggle').checked;

        if (isMultiSelect) {
            if (!selectedTickers.includes(ticker)) {
                selectedTickers.push(ticker);
            }
        } else {
            selectedTickers = [ticker];
        }
        updateHiddenInputs();

        assetSearch.value = '';
        searchSuggestions.classList.remove('active');

        // Re-render to show active state if visible
        // Or find card and activate
        const card = document.querySelector(`.asset-card[data-ticker="${ticker}"]`);
        if (card) {
            if (!isMultiSelect) {
                document.querySelectorAll('.asset-card').forEach(c => c.classList.remove('active'));
            }
            card.classList.add('active');
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            // If not in current view, maybe switch category? 
            // For simplicity, just re-render 'All' to show it.
            document.querySelector('.cat-tab[data-category="All"]').click();
            setTimeout(() => {
                const newCard = document.querySelector(`.asset-card[data-ticker="${ticker}"]`);
                if (newCard) {
                    if (!isMultiSelect) {
                        document.querySelectorAll('.asset-card').forEach(c => c.classList.remove('active'));
                    }
                    newCard.classList.add('active');
                    newCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }, 100);
        }

        if (selectedTickers.length === 1 && !isMultiSelect) {
            sectionTimeframe.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
});

// --- Timeframe Logic ---
const periodToggle = document.getElementById('periodToggle');
const periodInput = document.getElementById('period');
const customDateContainer = document.getElementById('customDateContainer');

periodToggle.addEventListener('click', (e) => {
    if (e.target.classList.contains('toggle-btn')) {
        // Update UI
        periodToggle.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
        e.target.classList.add('active');

        const value = e.target.dataset.value;
        periodInput.value = value;

        // Handle Custom Date
        if (value === 'custom') {
            customDateContainer.classList.remove('hidden');
        } else {
            customDateContainer.classList.add('hidden');
        }

        // Update allowed intervals in customization
        renderCustomizationSections();
        attachCustomizationListeners();
    }
});

// --- Customization Logic ---

// Helper for segmented controls
function setupSegmentedControl(controlId, inputId) {
    const control = document.getElementById(controlId);
    const input = document.getElementById(inputId);

    if (control && input) {
        control.addEventListener('click', (e) => {
            if (e.target.classList.contains('segment')) {
                control.querySelectorAll('.segment').forEach(s => s.classList.remove('active'));
                e.target.classList.add('active');
                input.value = e.target.dataset.value;
            }
        });
    }
}

setupSegmentedControl('primaryTypeControl', 'primaryType');

// Theme Control
const themeControl = document.getElementById('themeControl');
const styleInput = document.getElementById('style');
if (themeControl && styleInput) {
    themeControl.addEventListener('click', (e) => {
        const option = e.target.closest('.theme-option');
        if (option) {
            themeControl.querySelectorAll('.theme-option').forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
            styleInput.value = option.dataset.value;
        }
    });
}

// Background Color
const bgColorButtons = document.querySelectorAll('.bg-option');
const bgColorInput = document.getElementById('bgColor');

bgColorButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        bgColorButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        bgColorInput.value = btn.dataset.bg;
    });
});

// Output Format Control
const formatControl = document.getElementById('formatControl');
const outputFormatInput = document.getElementById('outputFormat');
if (formatControl && outputFormatInput) {
    formatControl.addEventListener('click', (e) => {
        if (e.target.classList.contains('segment')) {
            formatControl.querySelectorAll('.segment').forEach(s => s.classList.remove('active'));
            e.target.classList.add('active');
            outputFormatInput.value = e.target.dataset.value;
        }
    });
}

// --- Comparison Search Logic ---
// Removed old comparison search logic as multi-selection handles it.

// Close suggestions on click outside
// --- Templates & History Logic ---

function collectCurrentConfig() {
    // Derive primary chart type from first asset
    let primaryChartType = 'candle';
    if (selectedTickers.length > 0 && assetSettings[selectedTickers[0]]) {
        primaryChartType = assetSettings[selectedTickers[0]].chartType;
    }

    return {
        ticker: tickerInput.value,
        compare_ticker: compareTickerInput.value,
        period: periodInput.value,
        chart_type: primaryChartType,
        style: document.getElementById('style').value,
        bg_color: document.getElementById('bgColor').value,
        selected_tickers: selectedTickers,
        asset_settings: assetSettings
    };
}

function applyConfig(config) {
    // Restore State
    selectedTickers = config.selected_tickers || [];
    assetSettings = config.asset_settings || {};

    // Restore Inputs
    tickerInput.value = config.ticker || '';
    compareTickerInput.value = config.compare_ticker || '';
    periodInput.value = config.period || '1y';
    document.getElementById('style').value = config.style || 'standard';
    document.getElementById('bgColor').value = config.bg_color || 'transparent';

    // Update UI
    // Period
    document.querySelectorAll('#periodToggle .toggle-btn').forEach(btn => {
        if (btn.dataset.value === periodInput.value) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Theme
    document.querySelectorAll('#themeControl .theme-option').forEach(opt => {
        if (opt.dataset.value === document.getElementById('style').value) {
            opt.classList.add('active');
        } else {
            opt.classList.remove('active');
        }
    });

    // Background
    document.querySelectorAll('.bg-option').forEach(opt => {
        if (opt.dataset.bg === document.getElementById('bgColor').value) {
            opt.classList.add('active');
        } else {
            opt.classList.remove('active');
        }
    });

    // Assets
    updateHiddenInputs(); // Updates header and customization sections
    const activeCategory = document.querySelector('.cat-tab.active') ? document.querySelector('.cat-tab.active').dataset.category : 'All';
    renderAssets(activeCategory);

    // Scroll to top or chart?
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// API Calls
async function loadTemplates() {
    try {
        const res = await fetch('/api/templates');
        const templates = await res.json();
        renderTemplates(templates);
    } catch (e) {
        console.error("Error loading templates:", e);
    }
}

async function saveTemplate(name) {
    console.log("Saving template:", name);
    const config = collectCurrentConfig();
    console.log("Config to save:", config);
    try {
        const res = await fetch('/api/templates', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, config })
        });
        console.log("Save response status:", res.status);
        if (!res.ok) {
            const err = await res.json();
            console.error("Save error details:", err);
        }
        loadTemplates();
    } catch (e) {
        console.error("Error saving template:", e);
    }
}

async function deleteTemplate(name) {
    // Removed confirm() dialog - execute immediately for better UX
    try {
        await fetch(`/api/templates/${encodeURIComponent(name)}`, { method: 'DELETE' });
        loadTemplates();
    } catch (e) {
        console.error("Error deleting template:", e);
    }
}

async function loadHistory() {
    try {
        const res = await fetch('/api/history');
        const history = await res.json();
        renderHistory(history);
    } catch (e) {
        console.error("Error loading history:", e);
    }
}

async function addToHistory() {
    const config = collectCurrentConfig();
    try {
        await fetch('/api/history', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });
        loadHistory();
    } catch (e) {
        console.error("Error adding to history:", e);
    }
}

// Rendering
function renderTemplates(templates) {
    const container = document.getElementById('templatesList');
    if (Object.keys(templates).length === 0) {
        container.innerHTML = '<div class="empty-state">No templates saved yet</div>';
        return;
    }

    container.innerHTML = Object.entries(templates).map(([name, config]) => `
        <div class="template-card" onclick="applyTemplate('${name}')">
            <span class="template-name">${name}</span>
            <button class="template-delete" onclick="event.stopPropagation(); deleteTemplate('${name}')" title="Delete">✕</button>
        </div>
    `).join('');

    // Store templates globally for access
    window.currentTemplates = templates;
}

window.applyTemplate = (name) => {
    if (window.currentTemplates && window.currentTemplates[name]) {
        applyConfig(window.currentTemplates[name]);
        // Visual feedback
        alert(`Template "${name}" applied!`);
    }
};

function renderHistory(history) {
    const container = document.getElementById('historyList');
    if (history.length === 0) {
        container.innerHTML = '<div class="empty-state">No history yet</div>';
        return;
    }

    // Add Clear All button
    const clearAllBtn = `
        <div class="history-header">
            <button class="btn-clear-history" data-action="clear-all">🗑️ Clear All History</button>
        </div>
    `;

    const historyItems = history.map((item, index) => {
        const date = new Date(item.timestamp).toLocaleString();
        const ticker = item.ticker || 'Unknown';
        const period = item.period || '1y';

        return `
        <div class="history-item">
            <div class="history-info">
                <span class="history-title">${ticker}</span>
                <span class="history-meta">${period} • ${item.chart_type}</span>
                <span class="history-time">${date}</span>
            </div>
            <div class="history-actions">
                <button class="btn-history-action btn-apply" data-action="apply" data-index="${index}">Apply</button>
                <button class="btn-history-action btn-generate" data-action="generate" data-index="${index}">Generate</button>
                <button class="btn-history-action btn-delete" data-action="delete" data-index="${index}" title="Delete">✕</button>
            </div>
        </div>
        `;
    }).join('');

    container.innerHTML = clearAllBtn + historyItems;
    window.currentHistory = history;

    // Add event delegation for all history actions
    container.querySelectorAll('[data-action]').forEach(btn => {
        btn.addEventListener('click', handleHistoryAction);
    });
}

function handleHistoryAction(e) {
    const action = e.target.dataset.action;
    const index = parseInt(e.target.dataset.index);

    if (action === 'apply' && window.currentHistory && window.currentHistory[index]) {
        applyConfig(window.currentHistory[index].config);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (action === 'generate' && window.currentHistory && window.currentHistory[index]) {
        applyConfig(window.currentHistory[index].config);
        setTimeout(() => {
            document.getElementById('generateBtn').click();
        }, 100);
    } else if (action === 'delete') {
        deleteHistoryItem(index);
    } else if (action === 'clear-all') {
        clearAllHistory();
    }
}

async function deleteHistoryItem(index) {
    if (!window.currentHistory || !window.currentHistory[index]) return;

    // Removed confirm() dialog - execute immediately for better UX
    try {
        const res = await fetch(`/api/history/${index}`, { method: 'DELETE' });
        if (res.ok) {
            loadHistory();
        }
    } catch (e) {
        console.error("Error deleting history:", e);
    }
}

async function clearAllHistory() {
    // Removed confirm() dialog - execute immediately for better UX
    try {
        const res = await fetch('/api/history/clear', { method: 'DELETE' });
        if (res.ok) {
            loadHistory();
        }
    } catch (e) {
        console.error("Error clearing history:", e);
    }
}

// Event Listeners
document.getElementById('saveTemplateBtn').addEventListener('click', () => {
    // Use prompt for naming
    const name = prompt("Enter a name for this template:");
    if (name && name.trim()) {
        saveTemplate(name.trim());
    }
});

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    loadTemplates();
    loadHistory();
});

// Hook into form submission to save history
const originalHandleSubmit = chartForm.onsubmit; // Wait, chartForm uses addEventListener
// We need to find where chartForm is submitted and call addToHistory() on success.
// It's in the 'submit' event listener. I'll modify it separately.
document.addEventListener('click', (e) => {
    if (!assetSearch.contains(e.target) && !searchSuggestions.contains(e.target)) {
        searchSuggestions.classList.remove('active');
    }
});

// --- Chart Generation ---
chartForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // UI Loading State
    const btnText = generateBtn.querySelector('.btn-text');
    const btnLoading = generateBtn.querySelector('.btn-loading');

    generateBtn.disabled = true;
    btnText.classList.add('hidden');
    btnLoading.classList.remove('hidden');

    const formData = new FormData(chartForm);

    // Add custom dates if selected
    if (periodInput.value === 'custom') {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        if (startDate) formData.append('start', startDate);
        if (endDate) formData.append('end', endDate);
    }

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error || 'Failed');

        // Success - Handle both PNG and SVG formats
        const format = data.format || 'png';

        if (format === 'svg') {
            // Decode SVG from base64 and embed as inline SVG
            const svgContent = atob(data.image);
            chartImage.style.display = 'none';
            placeholder.innerHTML = svgContent;
            placeholder.classList.remove('hidden');
            // Style the SVG for better display
            const svgElement = placeholder.querySelector('svg');
            if (svgElement) {
                svgElement.style.width = '100%';
                svgElement.style.height = 'auto';
                svgElement.style.maxWidth = '100%';
            }
        } else {
            // PNG - display as image
            chartImage.src = `data:image/png;base64,${data.image}`;
            chartImage.classList.remove('hidden');
            chartImage.style.display = 'block';
            placeholder.classList.add('hidden');
        }

        // Show download button by revealing the chartActions wrapper
        const chartActions = document.getElementById('chartActions');
        if (chartActions) {
            chartActions.classList.remove('hidden');
        }

        // Scroll to chart
        sectionChart.scrollIntoView({ behavior: 'smooth', block: 'start' });

        // Add to History
        addToHistory();

        // Setup Download
        downloadBtn.onclick = async () => {
            try {
                const fileExt = (data.format === 'svg') ? 'svg' : 'png';
                const res = await fetch('/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image: data.image,
                        ticker: formData.get('ticker'),
                        format: data.format || 'png'
                    })
                });

                if (res.ok) {
                    const blob = await res.blob();
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${formData.get('ticker')}_chart.${fileExt}`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    setTimeout(() => URL.revokeObjectURL(url), 100);
                }
            } catch (err) {
                alert('Download failed: ' + err.message);
            }
        };

    } catch (err) {
        alert('Error generating chart: ' + err.message);
    } finally {
        generateBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoading.classList.add('hidden');
    }
});

// --- Economic Data (Horizontal Ticker) ---
async function fetchEconomicData() {
    try {
        const response = await fetch('/economic-data');
        const data = await response.json();
        renderEconomicTicker(data);
    } catch (error) {
        console.error('Failed to fetch economic data:', error);
    }
}

function renderEconomicTicker(data) {
    const tickerContainer = document.getElementById('economicTicker');
    if (!tickerContainer) return;

    tickerContainer.innerHTML = '';

    // Define indicators to show
    const indicators = [
        data.interest_rate,
        data.treasury_10y,
        data.cpi,
        data.unemployment,
        data.dxy,
        data.pmi,
        data.ism_services
    ];

    indicators.forEach((indicator, index) => {
        if (!indicator) return;

        const card = document.createElement('div');
        card.className = 'economic-card';

        // Determine change class
        let changeClass = 'eco-change';
        let changeIcon = '';
        if (indicator.change_pct > 0) {
            changeClass += ' positive';
            changeIcon = '↑';
        } else if (indicator.change_pct < 0) {
            changeClass += ' negative';
            changeIcon = '↓';
        }

        card.innerHTML = `
            <div class="eco-label">${indicator.label}</div>
            <div class="eco-value">${indicator.value}${indicator.unit}</div>
            <div class="${changeClass}">
                ${changeIcon} ${Math.abs(indicator.change_pct).toFixed(1)}%
            </div>
        `;

        // Add click listener for expansion
        if (indicator.ticker) {
            card.style.cursor = 'pointer';
            card.onclick = () => expandEconomicCard(indicator);
        }

        tickerContainer.appendChild(card);
    });
}

async function expandEconomicCard(indicator) {
    // Check if already expanded
    const existingOverlay = document.getElementById('ecoOverlay');
    if (existingOverlay) existingOverlay.remove();

    // Create Overlay
    const overlay = document.createElement('div');
    overlay.id = 'ecoOverlay';
    overlay.className = 'eco-overlay';

    // Create Expanded Card
    const card = document.createElement('div');
    card.className = 'eco-expanded-card';

    card.innerHTML = `
        <button class="eco-close-btn">✕</button>
        <div class="eco-expanded-content">
            <div class="eco-chart-container">
                <div class="eco-loading">Loading Chart...</div>
                <img id="ecoChartImage" class="hidden" alt="${indicator.label} Chart">
            </div>
            <div class="eco-details">
                <h3>${indicator.label}</h3>
                <div class="eco-stat-row">
                    <span class="eco-stat-value">${indicator.value}${indicator.unit}</span>
                    <span class="eco-stat-change ${indicator.change_pct >= 0 ? 'positive' : 'negative'}">
                        ${indicator.change_pct >= 0 ? '↑' : '↓'} ${Math.abs(indicator.change_pct).toFixed(1)}%
                    </span>
                </div>
                <p class="eco-description">${indicator.description || 'No description available.'}</p>
                <div class="eco-impact-box">
                    <strong>Market Impact:</strong>
                    <p>${indicator.impact || 'No impact analysis available.'}</p>
                </div>
            </div>
        </div>
    `;

    overlay.appendChild(card);
    console.log("Appending overlay to body");
    document.body.appendChild(overlay);
    console.log("Overlay appended. Visible?", overlay.offsetParent !== null);

    // Close Logic
    const closeBtn = card.querySelector('.eco-close-btn');
    const close = () => {
        overlay.classList.add('fade-out');
        setTimeout(() => overlay.remove(), 300);
    };
    closeBtn.onclick = close;
    overlay.onclick = (e) => {
        if (e.target === overlay) close();
    };

    // Fetch Chart - Use SVG format for infinite zoom quality
    try {
        const formData = new FormData();
        formData.append('ticker', indicator.ticker);
        formData.append('period', '5y'); // Default to 5y context
        formData.append('interval', '1d');
        formData.append('style', 'default');
        formData.append('output_format', 'svg'); // Use SVG for infinite zoom quality

        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.image) {
            const imgContainer = card.querySelector('.eco-chart-container');
            const loader = card.querySelector('.eco-loading');
            loader.classList.add('hidden');

            // Handle SVG format
            if (data.format === 'svg') {
                const svgContent = atob(data.image);
                imgContainer.innerHTML = svgContent;
                const svgElement = imgContainer.querySelector('svg');
                if (svgElement) {
                    svgElement.style.width = '100%';
                    svgElement.style.height = 'auto';
                    svgElement.style.cursor = 'zoom-in';
                    svgElement.onclick = (e) => {
                        e.stopPropagation();
                        openFullscreenChartSVG(svgContent, indicator.label, data.image);
                    };
                }
            } else {
                // PNG fallback
                const img = document.createElement('img');
                img.id = 'ecoChartImage';
                img.src = `data:image/png;base64,${data.image}`;
                img.style.cursor = 'zoom-in';
                img.onclick = (e) => {
                    e.stopPropagation();
                    openFullscreenChart(`data:image/png;base64,${data.image}`, indicator.label);
                };
                imgContainer.appendChild(img);
            }
        }
    } catch (e) {
        console.error("Error fetching economic chart:", e);
        card.querySelector('.eco-loading').textContent = "Failed to load chart";
    }
}

function openFullscreenChart(imgSrc, label) {
    // Create fullscreen modal
    const modal = document.createElement('div');
    modal.className = 'chart-fullscreen-modal';
    modal.innerHTML = `
        <div class="chart-fullscreen-content">
            <div class="chart-fullscreen-header">
                <h3>${label} - Historical Data</h3>
                <button class="chart-fullscreen-close">✕</button>
            </div>
            <div class="chart-fullscreen-image-container">
                <img src="${imgSrc}" alt="${label} Chart" class="chart-fullscreen-image">
            </div>
            <div class="chart-fullscreen-controls">
                <button class="chart-zoom-btn" data-action="zoom-in">🔍 Zoom In</button>
                <button class="chart-zoom-btn" data-action="zoom-out">🔍 Zoom Out</button>
                <button class="chart-zoom-btn" data-action="reset">↺ Reset</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Close handlers
    const closeBtn = modal.querySelector('.chart-fullscreen-close');
    closeBtn.onclick = () => {
        modal.classList.add('fade-out');
        setTimeout(() => modal.remove(), 300);
    };

    modal.onclick = (e) => {
        if (e.target === modal) {
        }
    };

    // Zoom controls and pan functionality
    const img = modal.querySelector('.chart-fullscreen-image');
    const imageContainer = modal.querySelector('.chart-fullscreen-image-container');
    let scale = 1;
    let translateX = 0;
    let translateY = 0;
    let isPanning = false;
    let startX = 0;
    let startY = 0;

    // Create zoom indicator
    const zoomIndicator = document.createElement('div');
    zoomIndicator.className = 'zoom-indicator';
    zoomIndicator.textContent = '100%';
    imageContainer.appendChild(zoomIndicator);

    function updateTransform() {
        img.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
        zoomIndicator.textContent = `${Math.round(scale * 100)}%`;
    }

    // Button controls
    modal.querySelectorAll('.chart-zoom-btn').forEach(btn => {
        btn.onclick = () => {
            const action = btn.dataset.action;
            if (action === 'zoom-in') {
                scale = Math.min(scale + 0.25, 3);
            } else if (action === 'zoom-out') {
                scale = Math.max(scale - 0.25, 0.5);
            } else if (action === 'reset') {
                scale = 1;
                translateX = 0;
                translateY = 0;
            }
            updateTransform();
        };
    });

    // Mousewheel / Touchpad zoom
    imageContainer.addEventListener('wheel', (e) => {
        e.preventDefault();

        const delta = e.deltaY > 0 ? -0.1 : 0.1;
        const oldScale = scale;
        const newScale = Math.max(0.5, Math.min(3, scale + delta));

        if (oldScale !== newScale) {
            // Get cursor position relative to the container
            const rect = imageContainer.getBoundingClientRect();
            const offsetX = e.clientX - rect.left - rect.width / 2;
            const offsetY = e.clientY - rect.top - rect.height / 2;

            // Calculate the point in the image that's under the cursor
            const imageX = (offsetX - translateX) / oldScale;
            const imageY = (offsetY - translateY) / oldScale;

            // Update scale
            scale = newScale;

            // Adjust translation to keep the same point under the cursor
            translateX = offsetX - imageX * scale;
            translateY = offsetY - imageY * scale;

            updateTransform();
        }
    }, { passive: false });

    // Double-click to zoom in/out
    img.addEventListener('dblclick', (e) => {
        e.preventDefault();
        if (scale === 1) {
            scale = 2;
        } else {
            scale = 1;
            translateX = 0;
            translateY = 0;
        }
        updateTransform();
    });

    // Pan with mouse drag
    img.addEventListener('mousedown', (e) => {
        if (scale > 1) {
            isPanning = true;
            startX = e.clientX - translateX;
            startY = e.clientY - translateY;
            img.style.cursor = 'grabbing';
            e.preventDefault();
        }
    });

    document.addEventListener('mousemove', (e) => {
        if (isPanning) {
            translateX = e.clientX - startX;
            translateY = e.clientY - startY;
            updateTransform();
        }
    });

    document.addEventListener('mouseup', () => {
        if (isPanning) {
            isPanning = false;
            img.style.cursor = scale > 1 ? 'grab' : 'zoom-in';
        }
    });

    // Touch support for pan
    let touchStartX = 0;
    let touchStartY = 0;

    img.addEventListener('touchstart', (e) => {
        if (scale > 1 && e.touches.length === 1) {
            touchStartX = e.touches[0].clientX - translateX;
            touchStartY = e.touches[0].clientY - translateY;
            e.preventDefault();
        }
    }, { passive: false });

    img.addEventListener('touchmove', (e) => {
        if (scale > 1 && e.touches.length === 1) {
            const touch = e.touches[0];
            translateX = touch.clientX - touchStartX;
            translateY = touch.clientY - touchStartY;
            updateTransform();
        }
    });

    img.addEventListener('touchend', () => {
        img.style.cursor = scale > 1 ? 'grab' : 'zoom-in';
    });

    // Update cursor based on zoom
    img.style.cursor = scale > 1 ? 'grab' : 'zoom-in';

    // Keyboard controls
    const keyHandler = (e) => {
        if (e.key === 'Escape') {
            modal.classList.add('fade-out');
            setTimeout(() => modal.remove(), 300);
            document.removeEventListener('keydown', keyHandler);
        } else if (e.key === '+' || e.key === '=') {
            scale = Math.min(scale + 0.25, 3);
            updateTransform();
        } else if (e.key === '-') {
            scale = Math.max(scale - 0.25, 0.5);
            updateTransform();
        } else if (e.key === '0') {
            scale = 1;
            translateX = 0;
            translateY = 0;
            updateTransform();
        } else if (e.key === 'ArrowUp') {
            translateY += 50;
            updateTransform();
        } else if (e.key === 'ArrowDown') {
            translateY -= 50;
            updateTransform();
        } else if (e.key === 'ArrowLeft') {
            translateX += 50;
            updateTransform();
        } else if (e.key === 'ArrowRight') {
            translateX -= 50;
            updateTransform();
        }
    };

    document.addEventListener('keydown', keyHandler);
}

// SVG Fullscreen Chart Viewer - Uses browser-native zoom for infinite quality
function openFullscreenChartSVG(svgContent, label, base64Image) {
    const modal = document.createElement('div');
    modal.className = 'chart-fullscreen-modal';
    modal.innerHTML = `
        <div class="chart-fullscreen-content">
            <div class="chart-fullscreen-header">
                <h3>${label} - Historical Data (SVG)</h3>
                <button class="chart-fullscreen-close">✕</button>
            </div>
            <div class="chart-fullscreen-image-container" style="overflow: auto;">
                ${svgContent}
            </div>
            <div class="chart-fullscreen-controls">
                <p style="color: #aaa; font-size: 13px; margin: 0;">
                    💡 Use browser zoom (Cmd/Ctrl +/-) for infinite quality zoom
                </p>
                <button class="chart-zoom-btn" data-action="download">💾 Download SVG</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Close handlers
    const closeBtn = modal.querySelector('.chart-fullscreen-close');
    closeBtn.onclick = () => {
        modal.classList.add('fade-out');
        setTimeout(() => modal.remove(), 300);
    };

    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.classList.add('fade-out');
            setTimeout(() => modal.remove(), 300);
        }
    };

    // Style the embedded SVG
    const svgElement = modal.querySelector('svg');
    if (svgElement) {
        svgElement.style.width = '100%';
        svgElement.style.height = 'auto';
        svgElement.style.maxWidth = '100%';
    }

    // Download button
    const downloadBtn = modal.querySelector('[data-action="download"]');
    downloadBtn.onclick = async () => {
        try {
            const blob = new Blob([atob(base64Image)], { type: 'image/svg+xml' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${label.replace(/\s+/g, '_')}_chart.svg`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            setTimeout(() => URL.revokeObjectURL(url), 100);
        } catch (err) {
            console.error('Download failed:', err);
        }
    };

    // Keyboard close  
    const keyHandler = (e) => {
        if (e.key === 'Escape') {
            modal.classList.add('fade-out');
            setTimeout(() => modal.remove(), 300);
            document.removeEventListener('keydown', keyHandler);
        }
    };

    document.addEventListener('keydown', keyHandler);
}

// Initial Fetch
fetchEconomicData();
setInterval(fetchEconomicData, 60000); // Refresh every minute

// --- News Tab Logic ---
const mainTabs = document.querySelectorAll('.main-tab');
const viewGenerator = document.getElementById('view-generator');
const viewNews = document.getElementById('view-news');
const countryPills = document.querySelectorAll('.country-pill');
const newsBlocksContainer = document.getElementById('newsBlocks');
const refreshNewsBtn = document.getElementById('refreshNewsBtn');
const filterChips = document.querySelectorAll('.filter-chip');
const sortSelect = document.getElementById('newsSortSelect');
const summarySection = document.getElementById('countrySummarySection');

let currentCountry = 'US';
let currentFilter = 'All';
let currentSort = 'date';
let allNewsData = [];
let summaryData = null;
let hexagonData = null;

// Main Tab Switching
mainTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        mainTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const view = tab.dataset.view;
        if (view === 'generator') {
            viewGenerator.classList.remove('hidden');
            viewNews.classList.add('hidden');
        } else {
            viewGenerator.classList.add('hidden');
            viewNews.classList.remove('hidden');
            if (allNewsData.length === 0) {
                fetchNews(currentCountry);
            }
        }
    });
});

// Country Switching
countryPills.forEach(pill => {
    pill.addEventListener('click', () => {
        countryPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        currentCountry = pill.dataset.country;
        fetchNews(currentCountry);
    });
});

// Filter Switching
filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
        filterChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        currentFilter = chip.dataset.filter;
        renderNews();
    });
});

// Sort Switching
sortSelect.addEventListener('change', (e) => {
    currentSort = e.target.value;
    renderNews();
});

refreshNewsBtn.addEventListener('click', () => fetchNews(currentCountry));

async function fetchNews(country) {
    // Hide old data immediately
    newsBlocksContainer.innerHTML = '';
    leaderboardSection.classList.add('hidden');
    summarySection.classList.add('hidden');

    // Show aesthetic candlestick loading animation
    newsBlocksContainer.innerHTML = `
        <div class="news-loading-overlay">
            <div class="loading-animation">
                <div class="candlestick-chart">
                    <div class="candle candle-tall" style="animation-delay: 0s;">
                        <div class="wick"></div>
                        <div class="body bullish"></div>
                    </div>
                    <div class="candle candle-short" style="animation-delay: 0.15s;">
                        <div class="wick"></div>
                        <div class="body bearish"></div>
                    </div>
                    <div class="candle candle-medium" style="animation-delay: 0.3s;">
                        <div class="wick"></div>
                        <div class="body bullish"></div>
                    </div>
                    <div class="candle candle-tall" style="animation-delay: 0.45s;">
                        <div class="wick"></div>
                        <div class="body bearish"></div>
                    </div>
                    <div class="candle candle-medium" style="animation-delay: 0.6s;">
                        <div class="wick"></div>
                        <div class="body bullish"></div>
                    </div>
                    <div class="candle candle-short" style="animation-delay: 0.75s;">
                        <div class="wick"></div>
                        <div class="body bullish"></div>
                    </div>
                </div>
                <p class="loading-text">Fetching global market intelligence...</p>
                <div class="loading-progress-bar">
                    <div class="loading-progress-fill"></div>
                </div>
            </div>
        </div>`;

    try {
        const response = await fetch(`/api/news/${country}`);
        const data = await response.json();

        if (data.error) throw new Error(data.error);

        allNewsData = data.news || [];
        summaryData = data.summary || null;
        hexagonData = data.hexagon || null;

        renderNews();
        renderSummary(summaryData, hexagonData);
    } catch (e) {
        newsBlocksContainer.innerHTML = `<div class="error-state">Error loading news: ${e.message}</div>`;
    }
}

function createNewsCard(item) {
    const sentimentClass = item.sentiment.toLowerCase();
    const impactDots = Array(5).fill(0).map((_, i) =>
        `<div class="dot ${i < Math.ceil(item.impact / 2) ? 'active' : ''}"></div>`
    ).join('');

    // We store the item data in a data attribute to retrieve it on click
    // But for cleaner code, let's just use an onclick handler that calls a function with the index
    // Or better, we create the element and attach the listener directly.

    // Since we are returning a string here, we can't attach a listener directly to the object.
    // We will change renderNews to create elements instead of using innerHTML for the grid.
    // But to keep it simple with the current structure, we'll use a global function or event delegation.
    // Let's use event delegation on the grid or just encode the data.
    // Actually, let's rewrite renderNews to create elements.
    return ''; // Not used, see renderNews update
}

function renderNews() {
    newsBlocksContainer.innerHTML = '';

    if (allNewsData.length === 0) {
        newsBlocksContainer.innerHTML = '<div class="empty-state">No news found.</div>';
        return;
    }

    // Filter
    let filteredNews = allNewsData;
    if (currentFilter !== 'All') {
        filteredNews = allNewsData.filter(item => item.category === currentFilter);
    }

    // Sort
    filteredNews.sort((a, b) => {
        if (currentSort === 'date') return b.timestamp - a.timestamp;
        if (currentSort === 'impact') return b.impact - a.impact;
        if (currentSort === 'sentiment') {
            const score = s => s === 'Positive' ? 1 : (s === 'Negative' ? -1 : 0);
            return score(b.sentiment) - score(a.sentiment);
        }
        return 0;
    });

    // Grouping Logic
    const categories = currentFilter === 'All'
        ? ['Economy', 'Finance', 'Politics', 'Technology', 'Energy', 'General']
        : [currentFilter];

    let hasContent = false;

    categories.forEach(category => {
        const categoryNews = filteredNews.filter(item => item.category === category);
        if (categoryNews.length === 0 && currentFilter === 'All') return;
        if (categoryNews.length === 0 && currentFilter !== 'All') return;

        hasContent = true;

        const block = document.createElement('div');
        block.className = 'news-category-block';

        const header = document.createElement('div');
        header.className = 'category-header';
        header.innerHTML = `<h3>${category}</h3><span class="category-badge">${categoryNews.length} items</span>`;
        block.appendChild(header);

        const grid = document.createElement('div');
        grid.className = 'news-grid-row';

        categoryNews.forEach(item => {
            const card = document.createElement('div');
            card.className = 'news-card';

            const sentimentClass = item.sentiment.toLowerCase();
            const impactDots = Array(5).fill(0).map((_, i) =>
                `<div class="dot ${i < Math.ceil(item.impact / 2) ? 'active' : ''}"></div>`
            ).join('');

            card.innerHTML = `
                <div class="news-meta">
                    <div class="news-source">
                        ${item.source_type === 'RSS' ? '📡' : '📰'} ${item.publisher}
                    </div>
                    <span class="news-time">${item.time}</span>
                </div>
                <div class="news-title">${item.title}</div>
                <div class="news-footer">
                    <span class="sentiment-badge ${sentimentClass}">${item.sentiment}</span>
                    <div class="impact-indicator" title="Impact Score: ${item.impact}/10">
                        Impact ${impactDots}
                    </div>
                </div>
            `;

            // Click Handler for Detail View
            card.addEventListener('click', () => showNewsDetail(item));

            grid.appendChild(card);
        });

        block.appendChild(grid);
        newsBlocksContainer.appendChild(block);
    });

    if (!hasContent) {
        newsBlocksContainer.innerHTML = '<div class="empty-state">No news found for this category.</div>';
    }

    // Render Leaderboard (with safety check)
    if (allNewsData) { // Assuming allNewsData is the equivalent of newsData.news
        renderLeaderboard(allNewsData);
    }
}

function renderLeaderboard(newsItems) {
    if (!newsItems || newsItems.length === 0) {
        leaderboardSection.classList.add('hidden');
        return;
    }

    // Sort by impact score descending
    const topItems = [...newsItems]
        .sort((a, b) => b.impact - a.impact)
        .slice(0, 5);

    const leaderboardHTML = `
        <div class="leaderboard-header">
            <h3 class="leaderboard-title">📊 Most Impactful News</h3>
            <button class="leaderboard-toggle" onclick="this.closest('.news-leaderboard').querySelector('.leaderboard-list').classList.toggle('collapsed'); this.textContent = this.textContent === '▼' ? '▲' : '▼';" style="background: none; border: none; font-size: 18px; cursor: pointer; color: #8E8E93; transition: all 0.2s;">▼</button>
        </div>
        <div class="leaderboard-list">
            ${topItems.map((item, index) => {
        const rankColors = ['#FFD60A', '#C0C0C0', '#CD7F32', '#8E8E93', '#8E8E93'];
        const rankColor = rankColors[index] || '#8E8E93';

        return `
                    <div class="leaderboard-item" data-news-id="${index}">
                        <div class="rank-badge" style="background: ${rankColor};">${index + 1}</div>
                        <div class="leaderboard-content">
                            <div class="leaderboard-headline">${item.title}</div>
                            <div class="leaderboard-meta">
                                <span>${item.category}</span>
                                <span class="impact-score">Impact: ${item.impact}/10</span>
                                <span>${item.publisher}</span>
                            </div>
                        </div>
                    </div>
                `;
    }).join('')}
        </div>
    `;

    leaderboardSection.innerHTML = leaderboardHTML;
    leaderboardSection.classList.remove('hidden');

    // Add click listeners
    topItems.forEach((item, index) => {
        const itemEl = leaderboardSection.querySelector(`[data-news-id="${index}"]`);
        if (itemEl) {
            itemEl.style.cursor = 'pointer';
            itemEl.addEventListener('click', () => showNewsDetail(item));
        }
    });
}

function showNewsDetail(item) {
    const modal = document.createElement('div');
    modal.className = 'news-detail-modal';

    // Analysis fallback
    const analysis = item.analysis || {
        market_impact: "Analysis not available.",
        investor_sentiment: "Sentiment data not available.",
        chain_reaction: [],
        historical_lookback: null,
        affected_assets: [],
        social_sentiment: { bullish: 33, bearish: 33, neutral: 34 }
    };

    // Generate Chain Reaction HTML
    let chainHTML = '';
    if (analysis.chain_reaction && analysis.chain_reaction.length > 0) {
        const steps = analysis.chain_reaction.map((step, index) => `
            <div class="chain-step">
                <div class="step-dot">${index + 1}</div>
                <div class="step-label">${step.step}</div>
                <div class="step-detail">${step.detail}</div>
            </div>
        `).join('');

        chainHTML = `
            <div class="chain-reaction-container">
                <div class="chain-title">Market Chain Reaction</div>
                <div class="chain-steps">
                    ${steps}
                </div>
            </div>
        `;
    }

    // Generate Affected Assets HTML
    let assetsHTML = '';
    if (analysis.affected_assets && analysis.affected_assets.length > 0) {
        const assetCards = analysis.affected_assets.map(ticker => `
            <div class="asset-mini-card">
                <span class="asset-ticker">${ticker}</span>
                <span class="asset-name">Asset</span>
            </div>
        `).join('');

        assetsHTML = `
            <div class="analysis-box">
                <h4>Affected Assets</h4>
                <div class="affected-assets-grid">
                    ${assetCards}
                </div>
            </div>
        `;
    }

    // Generate Social Sentiment HTML
    const social = analysis.social_sentiment || { bullish: 33, bearish: 33, neutral: 34 };
    const sentimentHTML = `
        <div class="social-sentiment-container">
            <h4>Live Social Sentiment (Simulated)</h4>
            <div class="sentiment-bar-wrapper">
                <div class="sentiment-segment segment-bullish" style="width: ${social.bullish}%">${social.bullish}%</div>
                <div class="sentiment-segment segment-neutral" style="width: ${social.neutral}%">${social.neutral}%</div>
                <div class="sentiment-segment segment-bearish" style="width: ${social.bearish}%">${social.bearish}%</div>
            </div>
            <div class="sentiment-legend">
                <span>Bullish</span>
                <span>Neutral</span>
                <span>Bearish</span>
            </div>
        </div>
    `;

    modal.innerHTML = `
        <div class="news-detail-content">
            <button class="news-detail-close">✕</button>
            
            <div class="detail-header">
                <span class="detail-category">${item.category}</span>
                <span class="detail-time">${item.time} • ${item.publisher}</span>
            </div>
            
            <h2 class="detail-title">${item.title}</h2>
            
            <div class="detail-summary">
                ${item.summary || item.title}
            </div>
            
            ${chainHTML}
            
            <div class="detail-analysis-grid">
                <div class="analysis-box">
                    <h4>Market Impact</h4>
                    <p>${analysis.market_impact}</p>
                </div>
                <div class="analysis-box">
                    <h4>Investor Sentiment</h4>
                    <p>${analysis.investor_sentiment}</p>
                </div>
                ${assetsHTML}
            </div>

            ${sentimentHTML}

            <div class="historical-chart-section" style="margin-top: 24px;">
                <h4>Historical Market Reaction Pattern</h4>
                <p class="historical-chart-description">
                    This chart shows simulated market behavior following similar news events over the past 5 trading days.
                    The pattern is based on ${analysis.historical_lookback ? analysis.historical_lookback.asset : 'market index'} performance and directional sentiment analysis.
                </p>
                <div class="historical-chart-container">
                    <canvas id="historicalChart"></canvas>
                </div>
            </div>
            
            <div class="detail-actions">
                <a href="${item.link}" target="_blank" class="btn-read-original">
                    Read Original Article 
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                </a>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Render Historical Chart
    if (analysis.historical_lookback) {
        const ctx = document.getElementById('historicalChart').getContext('2d');
        const data = analysis.historical_lookback.data;
        const isPositive = data[data.length - 1] > 0;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: analysis.historical_lookback.labels,
                datasets: [{
                    label: `${analysis.historical_lookback.asset} % Change`,
                    data: data,
                    borderColor: isPositive ? '#34C759' : '#FF3B30',
                    backgroundColor: isPositive ? 'rgba(52, 199, 89, 0.1)' : 'rgba(255, 59, 48, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: isPositive ? '#34C759' : '#FF3B30',
                    pointBorderColor: '#FFFFFF',
                    pointBorderWidth: 2,
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: { size: 12, weight: '600' },
                            color: '#1C1C1E',
                            padding: 12
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: { size: 13, weight: '700' },
                        bodyFont: { size: 12 },
                        callbacks: {
                            label: function (context) {
                                return `Change: ${context.parsed.y > 0 ? '+' : ''}${context.parsed.y.toFixed(1)}%`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: true,
                            color: 'rgba(0, 0, 0, 0.05)',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#8E8E93',
                            font: { size: 11, weight: '600' }
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.08)',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#8E8E93',
                            font: { size: 11, weight: '600' },
                            callback: function (value) {
                                return value > 0 ? `+${value}%` : `${value}%`;
                            }
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Render Macro Sparklines
    if (data.macro_data) {
        setTimeout(() => {
            data.macro_data.forEach((item, idx) => {
                const ctx = document.getElementById(`macroSpark_${idx}`);
                if (ctx && item.trend) {
                    // Handle object or array trend
                    const trendValues = Array.isArray(item.trend) ? item.trend : (item.trend.values || []);

                    // Use only last 7 points for sparkline
                    const sparkData = trendValues.slice(-7);

                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: sparkData.map((_, i) => i),
                            datasets: [{
                                data: sparkData,
                                borderColor: item.change > 0 ? (item.inverse ? '#FF3B30' : '#34C759') : (item.inverse ? '#34C759' : '#FF3B30'),
                                borderWidth: 2,
                                pointRadius: 0,
                                fill: false,
                                tension: 0.4
                            }]
                        },
                        options: {
                            responsive: false,
                            maintainAspectRatio: false,
                            plugins: { legend: { display: false }, tooltip: { enabled: false } },
                            scales: { x: { display: false }, y: { display: false } },
                            animation: { duration: 1000 }
                        }
                    });
                }
            });
        }, 100);
    }

    // Animation
    requestAnimationFrame(() => modal.classList.add('visible'));

    // Close Handlers
    const closeBtn = modal.querySelector('.news-detail-close');
    const close = () => {
        modal.classList.remove('visible');
        setTimeout(() => modal.remove(), 300);
    };

    closeBtn.onclick = close;
    modal.onclick = (e) => {
        if (e.target === modal) close();
    };

    // Esc key
    const escHandler = (e) => {
        if (e.key === 'Escape') {
            close();
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
}

let summaryChart = null;

function renderSummary(data, hexagonalData) {
    if (!data) return;

    summarySection.classList.remove('hidden');

    // Calculate normalized values (0-100) for the chart
    // Scores are -10 to 10. Map to 0-100. 0 is 50.
    const ecoVal = (data.eco_score + 10) * 5;
    const polVal = (data.pol_score + 10) * 5;
    const sentVal = (data.sentiment_score + 10) * 5;

    const getColor = (score) => score > 2 ? '#34C759' : (score < -2 ? '#FF3B30' : '#8E8E93');

    // Get country flag
    const countryFlags = {
        'US': '🇺🇸',
        'DE': '🇩🇪',
        'UK': '🇬🇧',
        'CN': '🇨🇳',
        'JP': '🇯🇵',
        'Global': '🌍'
    };
    const flag = countryFlags[currentCountry] || '🌍';

    summarySection.innerHTML = `
        <div class="summary-header">
            <h2 class="summary-title">
                <span class="country-flag">${flag}</span>
                Country Outlook
            </h2>
            <div class="summary-header-actions">
                <div class="summary-badges">
                    <span class="sentiment-badge" style="font-size: 1rem; background: ${getColor(data.sentiment_score)}20; color: ${getColor(data.sentiment_score)}; padding: 8px 16px; border-radius: 8px; font-weight: 700;">
                        ${data.market_sentiment}
                    </span>
                    <span class="category-badge" style="background: #F2F2F7; color: #8E8E93; padding: 8px 16px; border-radius: 8px; font-weight: 600;">
                        ${data.article_count} Sources
                    </span>
                </div>
                <button class="outlook-toggle" onclick="this.closest('.country-summary-section').querySelector('.summary-content').classList.toggle('collapsed'); this.textContent = this.textContent === '▼' ? '▲' : '▼';" style="background: none; border: none; font-size: 18px; cursor: pointer; color: #8E8E93; transition: all 0.2s; margin-left: 16px;">▼</button>
            </div>
        </div>
        <div class="summary-content">
            <div class="summary-grid">
                <!-- Left Column: Hexagon + Verdict -->
                <div class="summary-left-col">
                    <div class="hexagon-dashboard-container" style="position: relative; min-height: 350px; width: 100%; display: flex; justify-content: center; background: linear-gradient(135deg, rgba(52, 199, 89, 0.03), rgba(10, 132, 255, 0.03)); border-radius: 16px; padding: 20px;">
                        <div id="hexagonDashboard"></div>
                    </div>
                    
                    <div class="verdict-box" style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.8), rgba(249, 249, 249, 0.8)); padding: 20px; border-radius: 16px; margin-top: 20px; border: 1px solid rgba(0,0,0,0.05);">
                        <h4 style="font-size: 14px; font-weight: 700; color: #1C1C1E; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 16px;">📝</span> Market Analysis
                        </h4>
                        <p class="verdict-text" style="line-height: 1.6; color: #1C1C1E;">${data.verdict}</p>
                    </div>
                </div>

                <!-- Right Column: Macro Data + News -->
                <div class="summary-right-col">
                    <!-- Macro Grid -->
                    <div class="macro-grid">
                        ${data.macro_data ? data.macro_data.map((item, idx) => `
                            <div class="macro-card clickable" onclick="showMacroDetail('${item.label}', ${idx})">
                                <div class="macro-header">
                                    <span class="macro-label">${item.label}</span>
                                    <span class="macro-trend ${item.change > 0 ? (item.inverse ? 'negative' : 'positive') : (item.inverse ? 'positive' : 'negative')}">
                                        ${item.change > 0 ? '↗' : '↘'} ${item.change_label}
                                    </span>
                                </div>
                                <div class="macro-value">${item.value}</div>
                                <div class="macro-chart-container">
                                    <canvas id="macroSpark_${idx}" width="120" height="40"></canvas>
                                </div>
                                <div class="macro-hint">Click for details</div>
                            </div>
                        `).join('') : '<div class="no-data">Loading Macro Data...</div>'}
                    </div>

                    <!-- Top News Feed -->
                    <div class="news-feed-section">
                        <h4 style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Top Headlines</h4>
                        <div class="news-feed-list">
                            ${data.top_news ? data.top_news.map(news => `
                                <a href="${news.link || '#'}" target="_blank" class="news-feed-item">
                                    <div class="news-feed-content">
                                        <div class="news-feed-title">${news.title}</div>
                                        <div class="news-feed-meta">
                                            <span class="news-source">${news.publisher}</span>
                                            <span class="news-time">${news.time}</span>
                                        </div>
                                    </div>
                                    <div class="news-sentiment ${news.sentiment.toLowerCase()}">
                                        ${news.sentiment === 'Positive' ? 'Bullish' : news.sentiment === 'Negative' ? 'Bearish' : 'Neutral'}
                                    </div>
                                </a>
                            `).join('') : ''}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Render Hexagon Dashboard
    if (hexagonalData) {
        renderHexagonDashboard(hexagonalData);
    }

    // Store macro data globally for modal access
    window.currentMacroData = data.macro_data;
}

function showMacroDetail(label, idx) {
    const data = window.currentMacroData[idx];
    if (!data) return;

    const modal = document.createElement('div');
    modal.className = 'news-detail-modal visible';
    document.body.appendChild(modal);

    const details = data.details || {};
    const drivers = details.key_drivers || [];
    const news = details.related_news || [];

    modal.innerHTML = `
        <div class="news-detail-content" style="max-width: 800px;">
            <button class="news-detail-close">✕</button>
            
            <div class="macro-detail-header">
                <div class="macro-detail-title-section">
                    <h2 class="macro-detail-title">${data.label}</h2>
                    <div class="macro-detail-value-group">
                        <span class="macro-detail-value">${data.value}</span>
                        <span class="macro-detail-change ${data.change > 0 ? (data.inverse ? 'negative' : 'positive') : (data.inverse ? 'positive' : 'negative')}">
                            ${data.change > 0 ? '↗' : '↘'} ${data.change_label}
                        </span>
                    </div>
                </div>
                <div class="macro-detail-desc">${details.description || 'Detailed analysis of this macroeconomic indicator.'}</div>
            </div>

            <div class="macro-chart-section">
                <div class="chart-controls">
                    <div class="timeframe-group">
                        <button class="chart-btn" data-range="1M">1M</button>
                        <button class="chart-btn" data-range="3M">3M</button>
                        <button class="chart-btn active" data-range="1Y">1Y</button>
                        <button class="chart-btn" data-range="5Y">5Y</button>
                        <button class="chart-btn" data-range="MAX">MAX</button>
                    </div>
                    <button class="chart-btn fullscreen-btn" title="Toggle Fullscreen">⛶</button>
                </div>
                <div class="main-chart-container" id="macroChartContainer" style="height: 300px; position: relative;">
                    <canvas id="macroDetailChart"></canvas>
                </div>
            </div>

            <div class="macro-insights-grid">
                <div class="insight-card">
                    <h4>📊 Structural Analysis</h4>
                    <p>${details.structural_analysis || details.historical_context || 'Data shows significant volatility in recent periods.'}</p>
                </div>
                
                <div class="insight-card">
                    <h4>🌍 Larger Trend</h4>
                    <p>${details.larger_trend || 'Trend analysis unavailable.'}</p>
                </div>

                <div class="insight-card">
                    <h4>🎓 Why It Matters</h4>
                    <p>${details.relevance || 'Relevance data unavailable.'}</p>
                </div>

                ${drivers.length > 0 ? `
                <div class="insight-card">
                    <h4>🎯 Key Drivers</h4>
                    <ul class="drivers-list">
                        ${drivers.map(d => `<li>${d}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
            </div>

            ${news.length > 0 ? `
            <div class="macro-news-section">
                <h4>📰 Related News</h4>
                <div class="news-feed-list">
                    ${news.map(n => `
                        <a href="${n.link || '#'}" target="_blank" class="news-feed-item">
                            <div class="news-feed-content">
                                <div class="news-feed-title">${n.title}</div>
                                <div class="news-feed-meta">
                                    <span class="news-source">${n.publisher}</span>
                                    <span class="news-time">${n.time}</span>
                                </div>
                            </div>
                        </a>
                    `).join('')}
                </div>
            </div>
            ` : ''}
        </div>
    `;

    // Chart Logic
    let chartInstance = null;

    // Handle new data structure {dates: [], values: []} or fallback to old array
    const trendObj = data.trend || {};
    const fullValues = Array.isArray(trendObj) ? trendObj : (trendObj.values || []);
    const fullDates = Array.isArray(trendObj) ? trendObj.map((_, i) => `Day ${i}`) : (trendObj.dates || []);

    const updateChart = (range) => {
        const ctx = document.getElementById('macroDetailChart');
        if (!ctx) return;

        if (chartInstance) chartInstance.destroy();

        let slicePoints = fullValues.length;
        const freq = data.frequency || 'daily';

        // Calculate points based on frequency
        // Daily: ~252/yr, Monthly: 12/yr, Quarterly: 4/yr
        let pointsPerYear = 252;
        if (freq === 'monthly') pointsPerYear = 12;
        if (freq === 'quarterly') pointsPerYear = 4;

        if (range === '1M') slicePoints = Math.max(2, Math.round(pointsPerYear / 12));
        if (range === '3M') slicePoints = Math.max(2, Math.round(pointsPerYear / 4));
        if (range === '1Y') slicePoints = pointsPerYear;
        if (range === '5Y') slicePoints = pointsPerYear * 5;
        if (range === 'MAX') slicePoints = fullValues.length;

        // Ensure we don't slice more than we have
        if (slicePoints > fullValues.length) slicePoints = fullValues.length;

        const chartData = fullValues.slice(-slicePoints);
        const chartLabels = fullDates.slice(-slicePoints);

        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartLabels,
                datasets: [{
                    label: data.label,
                    data: chartData,
                    borderColor: '#007AFF',
                    backgroundColor: 'rgba(0, 122, 255, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointHitRadius: 20
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    zoom: {
                        zoom: {
                            wheel: { enabled: true },
                            pinch: { enabled: true },
                            mode: 'x',
                        },
                        pan: {
                            enabled: true,
                            mode: 'x',
                        },
                        limits: {
                            x: { min: 'original', max: 'original' },
                            y: { min: 'original', max: 'original' }
                        }
                    },
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(28, 28, 30, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false,
                        callbacks: {
                            label: function (context) {
                                return `${context.parsed.y.toFixed(2)}`;
                            },
                            title: function (context) {
                                return context[0].label; // Show full date
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: {
                            maxTicksLimit: 8,
                            display: true, // Show dates
                            maxRotation: 0,
                            autoSkip: true
                        }
                    },
                    y: {
                        grid: { color: 'rgba(0,0,0,0.05)' },
                        beginAtZero: false
                    }
                }
            }
        });
    };

    // Initialize Chart
    setTimeout(() => updateChart('1Y'), 100);

    // Timeframe Buttons
    const timeButtons = modal.querySelectorAll('.timeframe-group .chart-btn');
    timeButtons.forEach(btn => {
        btn.onclick = () => {
            timeButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            updateChart(btn.dataset.range);
        };
    });

    // Fullscreen Toggle
    const fsBtn = modal.querySelector('.fullscreen-btn');
    const chartSection = modal.querySelector('.macro-chart-section');
    fsBtn.onclick = () => {
        chartSection.classList.toggle('fullscreen');
        fsBtn.classList.toggle('active');
        fsBtn.textContent = chartSection.classList.contains('fullscreen') ? '✕' : '⛶';
        // Resize and Reset Zoom
        if (chartInstance) {
            chartInstance.resize();
            chartInstance.resetZoom();
        }
    };

    // Close Handlers
    const closeBtn = modal.querySelector('.news-detail-close');
    const close = () => {
        modal.classList.remove('visible');
        setTimeout(() => modal.remove(), 300);
    };

    closeBtn.onclick = close;
    modal.onclick = (e) => {
        if (e.target === modal) close();
    };

    // Esc key
    const escHandler = (e) => {
        if (e.key === 'Escape') {
            close();
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
}

function renderHexagonDashboard(hexData) {
    const container = document.getElementById('hexagonDashboard');
    if (!container || !hexData) return;

    // Helper: Get color based on score (0-100)
    const getCardColor = (score) => {
        if (score < 35) return { bg: 'linear-gradient(135deg, #FF3B30, #FF453A)', text: '#FFFFFF' };
        if (score < 50) return { bg: 'linear-gradient(135deg, #FF9500, #FF9F0A)', text: '#FFFFFF' };
        if (score < 65) return { bg: 'linear-gradient(135deg, #FFD60A, #FFD426)', text: '#1C1C1E' };
        if (score < 80) return { bg: 'linear-gradient(135deg, #34C759, #30D158)', text: '#FFFFFF' };
        return { bg: 'linear-gradient(135deg, #00C7BE, #00D4FF)', text: '#FFFFFF' };
    };

    // Helper: Get trend indicator
    const getTrendIcon = (score) => {
        if (score >= 60) return '↗';
        if (score <= 40) return '↘';
        return '→';
    };

    // Build cards HTML
    const createCard = (data, isMaster = false) => {
        const colors = getCardColor(data.score);
        const trend = getTrendIcon(data.score);
        const cardClass = isMaster ? 'metric-card master-card' : 'metric-card';

        return `
            <div class="${cardClass}" 
                 data-score="${data.score}" 
                 data-label="${data.label}" 
                 data-detail="${data.detail || ''}"
                 onclick="showMetricDetail('${data.label}', ${data.score}, '${data.detail || ''}', ${isMaster})">
                <div class="metric-card-content" style="background: ${colors.bg}; color: ${colors.text};">
                    <div class="metric-header">
                        <h4 class="metric-label">${data.label}</h4>
                        <span class="metric-trend">${trend}</span>
                    </div>
                    <div class="metric-score">
                        <span class="score-value">${Math.round(data.score)}</span>
                        <span class="score-unit">/ 100</span>
                    </div>
                    ${isMaster ? `<div class="metric-regime">${hexData.center.regime}</div>` : ''}
                </div>
            </div>
        `;
    };

    // Arrange cards: master in center, others around
    const topCards = hexData.hexagons.slice(0, 3);
    const bottomCards = hexData.hexagons.slice(3, 6);

    container.innerHTML = `
        <div class="metrics-dashboard">
            <div class="metrics-row metrics-row-top">
                ${topCards.map(card => createCard(card, false)).join('')}
            </div>
            <div class="metrics-row metrics-row-center">
                ${createCard(hexData.center, true)}
            </div>
            <div class="metrics-row metrics-row-bottom">
                ${bottomCards.map(card => createCard(card, false)).join('')}
            </div>
        </div>
    `;

    // Store hexData globally for modal access
    window.currentHexData = hexData;
}

function showMetricDetail(label, score, detail, isMaster) {
    const hexData = window.currentHexData;
    if (!hexData) return;

    // Find the data item
    let dataItem;
    if (isMaster) {
        dataItem = hexData.center;
    } else {
        dataItem = hexData.hexagons.find(h => h.label === label);
    }

    showHexagonDetail(label, score, detail, dataItem);
}

function showHexagonDetail(label, score, detail, hexDataItem) {
    const modal = document.getElementById('hexagonDetailModal');
    if (!modal) return;

    const breakdown = hexDataItem?.breakdown || {};
    const description = breakdown.description || 'Detailed analysis of this metric.';
    const implications = breakdown.market_implications || 'Market context not available.';
    const dataPoints = breakdown.data_points || [];
    const components = breakdown.components || [];
    const scoreDrivers = breakdown.score_drivers || [];
    const topSources = breakdown.top_sources || [];

    // Color based on score
    const getScoreColor = (s) => {
        if (s < 35) return '#FF3B30';
        if (s < 50) return '#FF9500';
        if (s < 65) return '#FFD60A';
        if (s < 80) return '#34C759';
        return '#00C7BE';
    };

    const scoreColor = getScoreColor(score);
    const interpretation =
        score >= 75 ? '🟢 <strong>Strong</strong>: Highly favorable conditions' :
            score >= 60 ? '🟡 <strong>Positive</strong>: Generally supportive environment' :
                score >= 45 ? '🟠 <strong>Neutral</strong>: Mixed signals, selective approach needed' :
                    score >= 30 ? '🟠 <strong>Cautious</strong>: Headwinds present, defensive positioning' :
                        '🔴 <strong>Weak</strong>: Significant challenges, risk-off stance';

    // Generate 7-day trend data (simulated from score with variance)
    const trendData = generateTrendData(score, 7);

    // Build comprehensive content with chart
    let content = `
        <div class="hexagon-detail-header">
            <div class="hexagon-detail-score" style="color: ${scoreColor};">${Math.round(score)}</div>
            <h3>${label}</h3>
            <div class="hexagon-score-bar-header">
                <div class="hexagon-score-fill" style="width: ${score}%; background: ${scoreColor};"></div>
            </div>
        </div>
        
        <div class="hexagon-detail-body">
            <!-- Overview -->
            <div class="detail-section">
                <h4>📊 Overview</h4>
                <p>${description}</p>
            </div>
            
            <!-- Score Interpretation -->
            <div class="detail-section">
                <div class="interpretation-box" style="border-left: 3px solid ${scoreColor};">
                    ${interpretation}
                </div>
            </div>
            
            <!-- 7-Day Trend Chart -->
            <div class="detail-section">
                <h4>📈 7-Day Trend</h4>
                <div class="chart-container">
                    <canvas id="metricTrendChart"></canvas>
                </div>
            </div>
            
            <!-- Market Implications -->
            <div class="detail-section">
                <h4>💹 Market Implications</h4>
                <div class="market-implications">
                    ${Array.isArray(implications)
            ? `<ul class="implications-list">${implications.map(imp => `<li>${imp.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</li>`).join('')}</ul>`
            : `<p>${implications.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</p>`
        }
                </div>
            </div>
            
            <!-- WHY: Score Drivers -->
            ${scoreDrivers.length > 0 ? `
            <div class="detail-section">
                <h4>🎯 Why This Score?</h4>
                <div class="score-drivers">
                    <ul class="drivers-list">
                        ${scoreDrivers.map(driver => {
            // Support markdown bold
            const formatted = driver.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            return `<li>${formatted}</li>`;
        }).join('')}
                    </ul>
                </div>
            </div>
            ` : ''}
            
            <!-- Key Data Points as Visual Table -->
            ${dataPoints.length > 0 ? `
            <div class="detail-section">
                <h4>📊 Key Indicators</h4>
                <div class="data-table">
                    ${dataPoints.map((point, idx) => {
            const [label, ...rest] = point.split(':');
            let value = rest.join(':').trim();

            // Support markdown bold (**text**)
            value = value.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

            return `
                            <div class="data-row ${idx % 2 === 0 ? 'even' : 'odd'}">
                                <div class="data-label">${label}</div>
                                <div class="data-value">${value || '—'}</div>
                            </div>
                        `;
        }).join('')}
                </div>
            </div>
            ` : ''}
            
            <!-- Score Components (for master score) -->
            ${components.length > 0 ? `
            <div class="detail-section">
                <h4>🔧 Score Components</h4>
                <div class="components-grid">
                    ${components.map(comp => `<div class="component-chip">${comp}</div>`).join('')}
                </div>
            </div>
            ` : ''}
            
            <!-- Key Sources for Further Investigation -->
            ${topSources.length > 0 ? `
            <div class="detail-section">
                <h4>📚 Key Sources</h4>
                <div class="sources-list">
                    ${topSources.map((source, idx) => `
                        <div class="source-item">
                            <div class="source-number">${idx + 1}</div>
                            <div class="source-content">
                                <a href="${source.url}" target="_blank" class="source-title">${source.title}</a>
                                <div class="source-publisher">${source.publisher}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
        </div>
    `;

    modal.querySelector('.hexagon-detail-content').innerHTML = `
        <button class="hexagon-detail-close" onclick="closeHexagonDetail()">✕</button>
        ${content}
    `;

    modal.classList.add('visible');

    // Show loading state for chart
    const chartContainer = modal.querySelector('.chart-container');
    if (chartContainer) {
        chartContainer.innerHTML = '<canvas id="metricTrendChart"></canvas><div class="chart-loading">Generating trend...</div>';
    }

    // Render chart after DOM update
    setTimeout(() => {
        const loadingEl = modal.querySelector('.chart-loading');
        if (loadingEl) loadingEl.remove();
        renderTrendChart(trendData, scoreColor);
    }, 150);
}

function generateTrendData(currentScore, days) {
    // Generate realistic trend data around current score
    const data = [];
    let score = currentScore - (Math.random() * 10 - 5);

    for (let i = 0; i < days; i++) {
        score += (Math.random() * 6 - 3);
        score = Math.max(0, Math.min(100, score));
        data.push(Math.round(score));
    }

    // Ensure last point is close to current score
    data[days - 1] = currentScore;

    return data;
}

function renderTrendChart(data, color) {
    const canvas = document.getElementById('metricTrendChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // Destroy existing chart if any
    if (window.metricChart) {
        window.metricChart.destroy();
    }

    window.metricChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['6d ago', '5d ago', '4d ago', '3d ago', '2d ago', '1d ago', 'Today'],
            datasets: [{
                label: 'Score',
                data: data,
                borderColor: color,
                backgroundColor: color + '20',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: color,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 13, weight: '600' },
                    bodyFont: { size: 12 },
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: Math.max(0, Math.min(...data) - 10),
                    max: Math.min(100, Math.max(...data) + 10),
                    ticks: {
                        font: { size: 11 },
                        callback: (value) => value + '%'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: { size: 10 }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function closeHexagonDetail() {
    const modal = document.getElementById('hexagonDetailModal');
    if (modal) {
        modal.classList.remove('visible');
    }
}

// --- Navigation ---
navCreateBtn.addEventListener('click', () => {
    sectionAsset.scrollIntoView({ behavior: 'smooth' });
});

// Show nav on scroll
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        navBar.classList.add('visible');
    } else {
        navBar.classList.remove('visible');
    }
});
