document.getElementById('sidebarCollapse').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('active');
});


let totalQuantity = 0;
if (document.getElementById("wishlistcookie")){
    let cookiecartdata = JSON.parse(document.getElementById("cartcookie").textContent);
    for (const key in cookiecartdata) {
        totalQuantity += cookiecartdata[key].quantity;
    }
}
document.getElementById("cartitemscount").textContent = `${totalQuantity}`;


let totalWishlistItems
if (document.getElementById("wishlistcookie")){
    let cookiewishlistdata = document.getElementById("wishlistcookie").textContent;
    totalWishlistItems = cookiewishlistdata.split(',').length; // Count commas by splitting and subtracting 1
} else {
    totalWishlistItems = ""
}
document.getElementById("wishlistitemscount").textContent = `${totalWishlistItems}`;
