/**
 * Archive functionality for bookmark management
 */
class ArchiveManager {
    /**
     * Initialize archive functionality on page load
     */
    static init() {
        document.querySelectorAll('.archive-link').forEach(link => {
            link.addEventListener('click', this.handleArchive.bind(this));
        });
    }
    
    /**
     * Handle archive link clicks with confirmation and error handling
     * @param {Event} e - Click event
     */
    static async handleArchive(e) {
        e.preventDefault();
        
        const link = e.target;
        const confirmMessage = 'Archive this bookmark?';
        
        if (!confirm(confirmMessage)) {
            return;
        }
        
        // Disable the link to prevent double-clicking
        link.style.opacity = '0.5';
        link.style.pointerEvents = 'none';
        
        try {
            const response = await fetch(link.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                // Success - reload the page to show updated list
                location.reload();
            } else {
                throw new Error(`Server responded with status: ${response.status}`);
            }
        } catch (error) {
            console.error('Archive operation failed:', error);
            alert('Failed to archive bookmark. Please try again.');
            
            // Re-enable the link
            link.style.opacity = '';
            link.style.pointerEvents = '';
        }
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    ArchiveManager.init();
});