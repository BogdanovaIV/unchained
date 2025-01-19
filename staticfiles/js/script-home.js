const quotes = [
    "Defeating human trafficking is a great moral calling of our time",
    "Modern slavery is closer than you think",
    "Together, we can fight against human trafficking",
    "Raise your voice, save a life",
    "Awareness is the first step to action"
];
let currentIndex = 0;

function updateQuote() {
    const quoteText = document.getElementById('quote-text');
    quoteText.textContent = quotes[currentIndex];
    currentIndex = (currentIndex + 1) % quotes.length;
}

setInterval(updateQuote, 5000);
