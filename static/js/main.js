/**
 * 清徽半导体材料 - 全局 JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // 导航栏活动状态
    highlightActiveNav();

    // 滚动时导航栏效果
    handleNavbarScroll();

    // 平滑滚动
    initSmoothScroll();

    // 图片懒加载
    initLazyLoading();
});

function highlightActiveNav() {
    const path = window.location.pathname;
    document.querySelectorAll('.navbar .nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href && path.startsWith(href) && href !== '/') {
            link.classList.add('active');
        } else if (href === '/' && path === '/') {
            link.classList.add('active');
        }
    });
}

function handleNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
        } else {
            navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.05)';
        }
    });
}

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

function initLazyLoading() {
    if ('loading' in HTMLImageElement.prototype) {
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            img.src = img.dataset.src || img.src;
        });
    }
}

/**
 * 通用API请求
 */
async function apiFetch(url, options = {}) {
    try {
        const resp = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        return await resp.json();
    } catch (e) {
        console.error('API请求失败:', e);
        throw e;
    }
}
