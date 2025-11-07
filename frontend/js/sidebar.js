// Sidebar JavaScript - Loads sidebar component and handles functionality
async function loadSidebar() {
    let sidebarContainer = document.getElementById('sidebar-container');
    
    if (!sidebarContainer) {
        // Try to find or create a container
        const body = document.body;
        const existingSidebar = document.querySelector('.sidebar, .vertical-nav, .navbar');
        if (existingSidebar) {
            existingSidebar.remove();
        }
        
        // Create container if it doesn't exist
        sidebarContainer = document.createElement('div');
        sidebarContainer.id = 'sidebar-container';
        body.insertBefore(sidebarContainer, body.firstChild);
    }
    
    // Check if sidebar is already loaded
    if (sidebarContainer.querySelector('.sidebar')) {
        console.log('Sidebar already loaded');
        initializeSidebar();
        return;
    }
    
    try {
        const response = await fetch('../components/sidebar.html');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const sidebarHTML = await response.text();
        if (!sidebarHTML || sidebarHTML.trim().length === 0) {
            throw new Error('Sidebar HTML is empty');
        }
        sidebarContainer.innerHTML = sidebarHTML;
        initializeSidebar();
        console.log('Sidebar loaded successfully');
    } catch (error) {
        console.error('Error loading sidebar:', error);
        // Fallback: create sidebar directly if fetch fails
        sidebarContainer.innerHTML = `
            <div class="sidebar">
                <div class="logo">
                    <i class="fas fa-shield-alt"></i>
                    <h1>Aegis<span>.</span></h1>
                </div>
                <ul class="nav-menu">
                    <li class="nav-item">
                        <a href="userdashboard.html" class="nav-link">
                            <i class="fas fa-home"></i><span>Dashboard</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="aichatbot.html" class="nav-link">
                            <i class="fas fa-robot"></i><span>AI Chatbot</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="community_list.html" class="nav-link">
                            <i class="fas fa-users"></i><span>Community</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="profile.html" class="nav-link">
                            <i class="fas fa-user"></i><span>Profile</span>
                        </a>
                    </li>
                </ul>
                <div class="logout-section">
                    <div class="user-avatar">
                        <i class="fas fa-sign-out-alt"></i>
                    </div>
                    <div class="user-info">
                        <h4>Logout</h4>
                        <p>Sign out safely</p>
                    </div>
                </div>
            </div>
        `;
        initializeSidebar();
    }
}

function initializeSidebar() {
    // Add active state to current page nav item
    const currentPath = window.location.pathname;
    const currentPage = currentPath.split('/').pop() || 'userdashboard.html';
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        const link = item.querySelector('.nav-link');
        if (link) {
            const linkHref = link.getAttribute('href');
            if (currentPage === linkHref || currentPath.includes(linkHref)) {
                item.classList.add('active');
            }
        }
    });

    // Logout functionality
    const logoutSection = document.querySelector('.logout-section');
    if (logoutSection) {
        // Remove any existing listeners to prevent duplicates
        const newLogoutSection = logoutSection.cloneNode(true);
        logoutSection.parentNode.replaceChild(newLogoutSection, logoutSection);
        
        newLogoutSection.addEventListener('click', async () => {
            try {
                const { auth } = await import('../js/firebase.js');
                const { signOut } = await import('https://www.gstatic.com/firebasejs/11.0.0/firebase-auth.js');
                await signOut(auth);
                window.location.href = 'login.html';
            } catch (err) {
                console.error('Logout error:', err.message);
                alert('Logout failed: ' + err.message);
            }
        });
    }
}

// Auto-load sidebar when DOM is ready
function initSidebarLoader() {
    // Wait a bit to ensure DOM is fully ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(loadSidebar, 100);
        });
    } else {
        // DOM already loaded, but wait a bit to ensure container exists
        setTimeout(loadSidebar, 100);
    }
}

// Initialize sidebar loader
initSidebarLoader();
