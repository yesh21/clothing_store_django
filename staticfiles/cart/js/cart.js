function addQuantity() {
    const prevSpan = event.target.previousElementSibling;
    if (prevSpan.innerHTML < 10 && prevSpan.id === 'quanitySelected') {
        prevSpan.innerHTML++;
    }
}

function dropQuantity() {
    const nextSpan = event.target.nextElementSibling;
    if (nextSpan.innerHTML > 0 && nextSpan.id === 'quanitySelected') {
        nextSpan.innerHTML--;
    }
}