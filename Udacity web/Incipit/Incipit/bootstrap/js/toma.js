var playerEl = document.getElementById("Mplayer");
var track;
function renderTrack() {
    var title = document.getElementById("title").value;
    var artist = document.getElementById("artist").value;


    track = window.tomahkAPI.Track(title,artist, {
        width:150,
        height:150,
        disabledResolvers: [ ],
        handlers: {
            onloaded: function() {
                log(track.connection+":\n  api loaded");
            },
            onended: function() {
                log(track.connection+":\n  Song ended: "+track.artist+" - "+track.title);
            },
            onplayable: function() {
                log(track.connection+":\n  playable");
            },
            onresolved: function(resolver, result) {
                log(track.connection+":\n  Track found: <b>"+resolver+"</b> - "+ result.track + " by "+result.artist);
            },
            ontimeupdate: function(timeupdate) {
                var currentTime = timeupdate.currentTime;
                var duration = timeupdate.duration;
                currentTime = parseInt(currentTime);
                duration = parseInt(duration);

                log(track.connection+":\n  Time update: "+currentTime + " "+duration);
            }  
        }
    });
    playerEl.replaceChild(track.render(),playerEl.childNodes[0]);
}