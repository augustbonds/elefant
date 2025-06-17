// Tag input with pills and autocomplete functionality
class TagInput {
    constructor(hiddenInputId, containerSelector) {
        this.hiddenTagsInput = document.getElementById(hiddenInputId);
        this.tagInputField = document.querySelector(`${containerSelector} .tag-input-field`);
        this.tagPillsContainer = document.querySelector(`${containerSelector} .tag-pills-container`);
        this.suggestionsDiv = document.querySelector(`${containerSelector} .tag-suggestions`);
        this.allTags = [];
        this.currentTags = [];
        this.selectedSuggestionIndex = -1;
        
        this.init();
    }
    
    async init() {
        // Fetch all available tags
        try {
            const response = await fetch('/api/tags');
            this.allTags = await response.json();
        } catch (error) {
            console.error('Failed to fetch tags:', error);
        }
        
        // Initialize with existing tags if any
        const existingTags = this.hiddenTagsInput.value;
        if (existingTags) {
            this.currentTags = existingTags.split(',').map(tag => tag.trim()).filter(tag => tag);
            this.renderTags();
        }
        
        this.bindEvents();
    }
    
    bindEvents() {
        // Handle input events for autocomplete
        this.tagInputField.addEventListener('input', (e) => {
            const currentValue = e.target.value.trim();
            
            if (currentValue.length >= 1) {
                // Filter matching tags
                const matches = this.allTags.filter(tag => 
                    tag.toLowerCase().includes(currentValue.toLowerCase()) &&
                    !this.currentTags.includes(tag)
                ).slice(0, 5); // Show max 5 suggestions
                
                this.showSuggestions(matches);
            } else {
                this.hideSuggestions();
            }
        });
        
        // Handle key events
        this.tagInputField.addEventListener('keydown', (e) => {
            const suggestions = this.suggestionsDiv.querySelectorAll('.tag-suggestion');
            const isDropdownVisible = this.suggestionsDiv.style.display === 'block';
            
            if (e.key === 'ArrowDown' && isDropdownVisible) {
                e.preventDefault();
                this.selectedSuggestionIndex = Math.min(this.selectedSuggestionIndex + 1, suggestions.length - 1);
                this.updateSelectedSuggestion();
            } else if (e.key === 'ArrowUp' && isDropdownVisible) {
                e.preventDefault();
                this.selectedSuggestionIndex = Math.max(this.selectedSuggestionIndex - 1, -1);
                this.updateSelectedSuggestion();
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (isDropdownVisible && this.selectedSuggestionIndex >= 0) {
                    const selectedTag = suggestions[this.selectedSuggestionIndex].dataset.tag;
                    this.selectTag(selectedTag);
                } else {
                    this.addCurrentTag();
                }
            } else if (e.key === 'Escape' && isDropdownVisible) {
                e.preventDefault();
                this.hideSuggestions();
            } else if (e.key === ',') {
                e.preventDefault();
                this.addCurrentTag();
            } else if (e.key === 'Backspace' && e.target.value === '' && this.currentTags.length > 0) {
                // Remove last tag if input is empty
                this.removeTag(this.currentTags.length - 1);
            } else {
                // Reset selection when typing
                this.selectedSuggestionIndex = -1;
            }
        });
        
        // Focus the input when clicking on the container
        this.tagPillsContainer.addEventListener('click', (e) => {
            if (e.target === this.tagPillsContainer || e.target.classList.contains('tag-input-field')) {
                this.tagInputField.focus();
            }
        });
        
        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.tagPillsContainer.contains(e.target) && !this.suggestionsDiv.contains(e.target)) {
                this.hideSuggestions();
            }
        });
    }
    
    addCurrentTag() {
        const tagValue = this.tagInputField.value.trim();
        if (tagValue && !this.currentTags.includes(tagValue)) {
            this.currentTags.push(tagValue);
            this.tagInputField.value = '';
            this.renderTags();
            this.updateHiddenInput();
            this.hideSuggestions();
        }
    }
    
    removeTag(index) {
        this.currentTags.splice(index, 1);
        this.renderTags();
        this.updateHiddenInput();
        this.tagInputField.focus();
    }
    
    renderTags() {
        // Clear existing pills (but keep the input field)
        const pills = this.tagPillsContainer.querySelectorAll('.tag-pill');
        pills.forEach(pill => pill.remove());
        
        // Add tag pills before the input field
        this.currentTags.forEach((tag, index) => {
            const pill = document.createElement('div');
            pill.className = 'tag-pill';
            pill.innerHTML = `${tag}<span class="tag-pill-remove" data-index="${index}">×</span>`;
            
            // Add click handler for remove button
            pill.querySelector('.tag-pill-remove').addEventListener('click', () => {
                this.removeTag(parseInt(pill.querySelector('.tag-pill-remove').dataset.index));
            });
            
            this.tagPillsContainer.insertBefore(pill, this.tagInputField);
        });
    }
    
    updateHiddenInput() {
        this.hiddenTagsInput.value = this.currentTags.join(',');
    }
    
    updateSelectedSuggestion() {
        const suggestions = this.suggestionsDiv.querySelectorAll('.tag-suggestion');
        suggestions.forEach((suggestion, index) => {
            suggestion.classList.toggle('selected', index === this.selectedSuggestionIndex);
        });
    }
    
    showSuggestions(matches) {
        if (matches.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        this.selectedSuggestionIndex = -1; // Reset selection
        
        this.suggestionsDiv.innerHTML = matches.map(tag => 
            `<div class="tag-suggestion" data-tag="${tag}">${tag}</div>`
        ).join('');
        
        this.suggestionsDiv.style.display = 'block';
        
        // Add click handlers
        this.suggestionsDiv.querySelectorAll('.tag-suggestion').forEach(suggestion => {
            suggestion.addEventListener('click', () => {
                this.selectTag(suggestion.dataset.tag);
            });
        });
    }
    
    hideSuggestions() {
        this.suggestionsDiv.style.display = 'none';
        this.selectedSuggestionIndex = -1;
    }
    
    selectTag(selectedTag) {
        if (!this.currentTags.includes(selectedTag)) {
            this.currentTags.push(selectedTag);
            this.tagInputField.value = '';
            this.renderTags();
            this.updateHiddenInput();
            this.hideSuggestions();
            this.tagInputField.focus();
        }
    }
}