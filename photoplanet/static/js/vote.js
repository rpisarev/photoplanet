$(document).ready(function(){
    $('.js-vote').click(function(){
        var photo_id = $(this).attr('data-id');
        var vote = $(this).attr('data-vote');
        alert(vote);
        $.ajax({
            url: window.PHOTO.vote_url,
            data: {'photo': photo_id, 'vote': vote},
            type: 'POST',
            success: function(data){
                console.log(data);
		alert(data);
                $('.js-vote-' + photo_id).text(data.votes);
            }

        });
        return false;
    })
})
