// Make loading symbol appear when loading next page
document.getElementById("submit").onclick = function() {loadFunction()};

function loadFunction() {
    document.getElementById('load').style.display = 'inline-block';
}

// Copy Stream URL and Edit "Copy Text" Message
function myFunction() {
    var copyText = document.getElementById("answer");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
    
    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copied: " + copyText.value;
}

// Confirm Stream URL was copied
function outFunc() {
    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copy to clipboard";
}