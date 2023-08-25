// Get Stripe publishable key
fetch("/payment/config/")
    .then((result) => { return result.json(); })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);

        // Event handler
        document.querySelector("#paybtn").addEventListener("click", () => {
            // Get Checkout Session ID
            fetch("/payment/create-checkout-session/")
                .then((result) => { return result.json(); })
                .then((data) => {
                    console.log(data);
                    // Redirect to Stripe Checkout
                    return stripe.redirectToCheckout({ sessionId: data.sessionId })
                })
                .then((res) => {
                    console.log(res);
                });
        });
    });

// Event handler
// document.querySelectorAll(".single_price_plan").forEach((plan) => {
//     const priceId = plan.dataset.priceId;

//     console.log(priceId);
//     plan.addEventListener("click", () => {
//         fetch("/payment/create-subscription-session/", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/x-www-form-urlencoded",
//                 "X-CSRFToken": csrfToken, // You need to set csrfToken variable
//             },
//             body: new URLSearchParams({
//                 priceId: priceId, // Use the correct parameter name
//             }),
//         })
//             .then((result) => { return result.json(); })
//             .then((data) => {
//                 // Redirect to Stripe Checkout
//                 return stripe.redirectToCheckout({ sessionId: data.sessionId })
//                 .catch((error) => {
//                     console.error('Payment failed:', error);
//                     // Make an AJAX request to your Django server to handle the failure
//                     fetch("/payment/payment-failed/", {
//                         method: "POST",
//                         headers: {
//                             "Content-Type": "application/json",
//                             "X-CSRFToken": csrfToken, // You need to set csrfToken variable
//                         },
//                         body: JSON.stringify({ session_id: data.sessionId }),
//                     })
//                     .then((result) => { return result.json(); })
//                     .then((data) => {
//                         console.log(data);
//                     });
//                 });
//             })
//             .then((res) => {
//                 console.log(res);
//             });
//     });
// });
