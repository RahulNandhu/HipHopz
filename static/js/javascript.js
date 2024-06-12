document.addEventListener("DOMContentLoaded", function() {
    var rangeDiscountInput = document.getElementById('rangeDiscountInput');
    var numberDiscountInput = document.getElementById('numberDiscountInput');
    var numberPriceInput = document.getElementById('numberPriceInput');
    var rangePriceInput = document.getElementById('rangePriceInput');

    // Set initial value of number input to match range input
    numberDiscountInput.value = rangeDiscountInput.value;
    numberPriceInput.value=rangePriceInput.value;

    // Add event listener to range input
    rangeDiscountInput.addEventListener('input', function() {
        // Update value of number input when range input changes
        numberDiscountInput.value = rangeDiscountInput.value;
    });

    rangePriceInput.addEventListener('input',function(){
        numberPriceInput.value = rangePriceInput.value;
    });

    // Add event listener to number input
    numberDiscountInput.addEventListener('input', function() {
        // Update value of range input when number input changes
        rangeDiscountInput.value = numberDiscountInput.value;
    });

    numberPriceInput.addEventListener('input',function(){
        rangePriceInput.value = numberPriceInput.value;
    });



});

function Edit_Success() {
    var success = document.getElementById('success').textContent;
    if (success) {
        Swal.fire({
            title: 'Success!',
            text: success,
            icon: 'success',
            confirmButtonText: 'OK'
        });
    }
};



