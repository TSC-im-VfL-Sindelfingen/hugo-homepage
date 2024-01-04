$(function() {
    $(".tsc-gallery-img a").click(function(ev){
        // console.debug(ev)
        const url = ev.currentTarget.dataset.url
        console.debug(url)
        $('#overlay').removeClass('hidden')
        $('#overlay  .img img').attr('src', url)
    })
    $('#overlay .background, #overlay .spacer').click(function(ev) {
        $('#overlay').addClass('hidden')
        $('#overlay .img img').attr('src', '')
    })
    // $('#overlay').on('keydown', function(ev){
    //     if(ev.keyCode === 27) {
    //         console.log('closing')
    //     }
    // })
})
