$(function () {
    var index = 0
    const maxIndex = 5
    const delay = 7000
    function showImage(idx) {
        const imgs = $('#header .slider img')
        imgs.eq(idx).removeClass('hidden')
        imgs.filter((i, e) => {return i != idx}).addClass('hidden')
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
        console.log("switching to index", newIdx)
        showImage(newIdx)
        index = newIdx
        setTimeout(nextImage, delay)
    }
    setTimeout(nextImage, delay)
})
