$(function () {
    var index = 0
    const maxIndex = 5
    const delay = 6000
    const shuffeledIndices = []

    for(let i=0; i<=maxIndex; i++){
        shuffeledIndices.push(i)
    }

    // Shuffle by Fisher-Yates algorithm
    for(let i=maxIndex; i>= 0; i--) {
        const j = Math.floor(Math.random() * (i+1))
        const tmp = shuffeledIndices[j]
        shuffeledIndices[j] = shuffeledIndices[i]
        shuffeledIndices[i] = tmp
    }

    function showImage(idxidx) {
        const idx = shuffeledIndices[idxidx]
        const imgs = $('#header .slider .slider-img')
        imgs.eq(idx).removeClass('hidden')
        imgs.filter((i, e) => {return i != idx}).addClass('hidden')
        const dots = $('#header .slider .dots .dot')
        dots.removeClass('active')
        dots.eq(idxidx).addClass('active')
        index = idxidx
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

    showImage(0)

    // Start the animaions delayed to allow for showing the first image directly
    setTimeout(() => {
        $('#header .slider .slider-img').addClass('animated')
    }, 150)

    setTimeout(nextImage, delay)
    $('#header .slider .dots .dot').click(function (evt) {
        // console.log(evt)
        const newIdx = $(evt.target).data('index')
        showImage(newIdx)
    })
})
