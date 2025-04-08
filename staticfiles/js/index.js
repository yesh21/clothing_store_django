$(document).ready(function() {
    $('.carousel').slick({
        dots: true,
        infinite: true,
        speed: 1000,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        arrows: true,
        nextArrow: '<button type="button" class="slick-next w-20">⫸</button>',
        prevArrow: '<button type="button" class="slick-prev w-20">⫷</button>',
    });
});

function wishlistHeart() {
    if (event.target.classList.contains("fas", "fas-heart")) {
        event.target.classList.remove("fas", "fas-heart");
    } else {
        event.target.classList.add("fas", "fas-heart");
    }
}
gsap.registerPlugin(ScrollTrigger);
var sections = gsap.utils.toArray('#yourDiv');
sections.forEach((section) => {
    gsap.to(section, {
        duration: 1.5,
        y: '-30%',
        opacity: 1,
        ease: 'power2.inOut',
        scrollTrigger: {
            trigger: section,
            start: "center bottom",
            //end: "center top",
            //toggleClass: "active",
            //markers: true
        }
    });
})