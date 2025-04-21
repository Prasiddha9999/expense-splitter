// Main JavaScript file for Group Expense Splitter

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Custom file input
    document.querySelectorAll('.custom-file-input').forEach(function(input) {
        input.addEventListener('change', function(e) {
            var fileName = this.files[0].name;
            var nextSibling = this.nextElementSibling;
            nextSibling.innerText = fileName;
        });
    });

    // Custom expense split functionality
    const splitTypeSelect = document.getElementById('split-type');
    const customSplitContainer = document.getElementById('custom-split-container');
    
    if (splitTypeSelect && customSplitContainer) {
        splitTypeSelect.addEventListener('change', function() {
            if (this.value === 'custom') {
                customSplitContainer.classList.remove('d-none');
            } else {
                customSplitContainer.classList.add('d-none');
            }
        });
    }

    // Currency conversion
    const currencySelect = document.getElementById('currency');
    const amountInput = document.getElementById('amount');
    const convertedAmountDisplay = document.getElementById('converted-amount');
    
    if (currencySelect && amountInput && convertedAmountDisplay) {
        const updateConvertedAmount = function() {
            const amount = parseFloat(amountInput.value) || 0;
            const currency = currencySelect.value;
            
            // This would be replaced with actual API call in production
            // For now, just a simple mock conversion
            let rate = 1;
            if (currency === 'EUR') rate = 0.85;
            if (currency === 'GBP') rate = 0.75;
            if (currency === 'JPY') rate = 110;
            
            const baseCurrency = 'USD'; // Assuming USD is base
            const convertedAmount = amount * rate;
            
            convertedAmountDisplay.textContent = `${convertedAmount.toFixed(2)} ${currency}`;
        };
        
        amountInput.addEventListener('input', updateConvertedAmount);
        currencySelect.addEventListener('change', updateConvertedAmount);
    }
});
