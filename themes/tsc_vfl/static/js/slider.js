$(function () {
    var index = 0
    const maxIndex = 5
    const delay = 7000
    function showImage(idx) {
        // console.log("switching to index", idx)
        const imgs = $('#header .slider .slider-img')
        imgs.eq(idx).removeClass('hidden')
        imgs.filter((i, e) => {return i != idx}).addClass('hidden')
        const dots = $('#header .slider .dots .dot')
        dots.removeClass('active')
        dots.eq(idx).addClass('active')
        index = idx
    }
    function getNextIndex() {
        const ret = index + 1
        if (ret > maxIndex) {
            return 0
        } else {
            return ret
        }
    }
    function nextImage() {
        const newIdx = getNextIndex()
        showImage(newIdx)
        setTimeout(nextImage, delay)
    }
    // setTimeout(nextImage, delay)
    $('#header .slider .dots .dot').click(function (evt) {
        // console.log(evt)
        const newIdx = $(evt.target).data('index')
        showImage(newIdx)
    })
})
