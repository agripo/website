/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
forced_quality = null;
function force_quality(quality, button){
    forced_quality = quality;

    $('#force_quality button').removeClass('active');
    $(button).addClass('active');

    // We update the player's dimensions
    if(forced_quality == "low"){
        var width = 600;
        var height = 337;
    }else if(forced_quality == "medium"){
        var width = 800;
        var height = 450;
    }else{
        forced_quality = "high";
        var width = 1280;
        var height = 720;
    }
    var vid = $('#main_video')[0];
    vid.width = width;
    vid.height = height;


    // We update the url to the video that are already shown
    $('#main_video source').each(function(id, el){
        el.src = el.src.replace(/low|medium|high/i,forced_quality);
        console.log("New source :", el);
    });

    var timestamp = vid.currentTime;
    vid.load();
    vid.addEventListener('loadedmetadata', function(){
        vid.currentTime = timestamp;
        vid.play();
    }, false);
}

function hide_player(){
    console.log("Hiding the player");
    stopActiveVideo();
    there_is_a_player = false;

    $('#main_video').remove();
    console.log("Before", $('#active_focus'));
    $('#active_focus').remove();
    console.log("After", $('#active_focus'));

    $('#player_preview, #chapter_selector').fadeIn();

    $('#player_closer').hide();
    if(video_quality != 'low'){
        $('#focus_list').show();
    }
    $('#youtube_player').replaceWith('<div id="youtube_player"></div>');
}
var video_quality = null;
var focusShown = "";
var focus_list = {
    theme1:{
        1:[77,87],
        2:[145,155]
    },
    theme2:{
        1:[157,167],
        2:[307,317],
        3:[358,368],
        4:[387,397]
    },
    theme3:{
        1:[7,17],
        2:[148,158],
        3:[210,220]
    }
};

var youtube_api_ready = false;
var YTPlayer;
var there_is_a_player = false;

function show_player(video, quality, play, start_time){
    if(!youtube_api_ready){
        console.log("Youtube API is not ready. We wait a little...");
        setTimeout(function(){
            show_player(video, quality, play);
        }, 200);
        return
    }
    if(typeof(play) == 'undefined'){
        play = true;
    }
    if(typeof(start_time) == 'undefined'){
        start_time = 0;
    }
    var theme_name = "theme"+video;
    console.log("Showing the player");
    $('#focus_list').hide();

    // We reset the focus window
    hideFocus();

    if(forced_quality === null){
        video_quality = quality;
    }else{
        video_quality = forced_quality;
    }
    if(quality == "low"){
        var width = 600;
        var height = 337;
    }else if(quality == "medium"){
        var width = 800;
        var height = 450;
    }else{
        quality = "high";
        var width = 1280;
        var height = 720;
    }

    var player_is_ready = false;
    function onPlayerReady(event){
        console.log("Youtube player is ready");
        player_is_ready = true;

        if(play){
            playActiveVideo(start_time);
        }
    }

    function onPlayerStateChange(event) {
        if(event.data == YT.PlayerState.PLAYING){
            var check_time = function(){
                var time = event.target.getCurrentTime();

                for(var focus in focus_list[theme_name]){
                    var the_focus = focus_list[theme_name][focus];
                    var the_focus_id = theme_name+'_'+focus;
                    if(focusShown == "" && time >= the_focus[0] && time < the_focus[1]){
                        showFocus(video, focus);
                    }else if(focusShown == the_focus_id && (time < the_focus[0] || time >= the_focus[1])){
                        hideFocus();
                    }
                }
                if(there_is_a_player && YTPlayer.getPlayerState() == YT.PlayerState.PLAYING){
                    window.setTimeout(check_time, 250);
                }
            }
            check_time();
        }else if(event.data == YT.PlayerState.ENDED){
            console.log("Video ended");
            hide_player();
            select_topic("next");
        }
    }
    var videos_ids = ['oyYKDGxIviw', 'bKCPB_usTm4', 'zH4bQP4JnoI'];
    var video_id = videos_ids[parseInt(video) - 1];
    console.log("The video id is", video_id, parseInt(video), parseInt(video) - 1);
    YTPlayer = new YT.Player('youtube_player', {
        width: width,
        height: height,
        videoId: video_id,
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
    there_is_a_player = true;

    $('<div/>', {
        id:'active_focus'
    }).appendTo($("#content"));

    $('#player_preview, #chapter_selector').fadeOut();

    $('#player_closer').show();
}

function showFocus(video, focus){
    focusShown = focus;
    console.debug("Showing focus #",video+"_"+focus);

    $('#active_focus').html($('#focus_theme'+video+"_"+focus).html());
    $('#active_focus').fadeIn('slow');

    $('#active_focus .content').load("/webdoc/focus/theme"+video+"_focus"+focus+"/");
}

function hideFocus(){
    focusShown = 0;
    console.debug("Hiding active focus");
    $('#active_focus').fadeOut();
}
function focus_open_this_one(theme, focus){
    show_player(theme, "medium", true, focus_list['theme'+theme][focus][0]);
}

function focus_open(){
    pauseActiveVideo();
    $('#player_closer').fadeOut();

    $('#active_focus').addClass("full");
}
function focus_close(){
    playActiveVideo();
    $('#player_closer').fadeIn();

    $('#active_focus').removeClass("full");
}

var previous_shown_chapter = 1;
function select_topic(element){
    if(element == "next"){
        if(previous_shown_chapter < 3){
            chapter = previous_shown_chapter + 1;
        }else{
            chapter = 'none';
        }
    }else{
        var chapter = $(element).data("select");
    }
    console.log("We switch to chapter",chapter);
    if(chapter != "none"){
        $('#chapter'+previous_shown_chapter).fadeOut(
            400,
            function(){
                $('#chapter'+chapter).fadeIn();
            }
        );
        $('#preview'+previous_shown_chapter).fadeOut(
            400,
            function(){
                $('#preview'+chapter).fadeIn();
            }
        );
        $('#chapter'+previous_shown_chapter+'_focus').fadeOut(
            400,
            function(){
                $('#chapter'+chapter+'_focus').fadeIn();
            }
        );
        previous_shown_chapter = chapter;

        if(chapter > 1){
            $('#previous_topic_button').data("select", chapter - 1);
            $('#previous_topic_button').parent().removeClass('disabled_arrow');
        }else{
            $('#previous_topic_button').data("select", "none");
            $('#previous_topic_button').parent().addClass('disabled_arrow');
        }
        if(chapter < 3){
            $('#next_topic_button').data("select", chapter + 1);
            $('#next_topic_button').parent().removeClass('disabled_arrow');
        }else{
            $('#next_topic_button').data("select", "none");
            $('#next_topic_button').parent().addClass('disabled_arrow');
        }
    }
}


// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
    youtube_api_ready = true;
}

function pauseActiveVideo(){
    console.log("PAUSE");
    YTPlayer.pauseVideo();
}

function playActiveVideo(start_time){
    console.log("PLAY");
    YTPlayer.playVideo();
    if(typeof(start_time) != 'undefined'){
        YTPlayer.seekTo(start_time, true);
    }
}
function stopActiveVideo() {
    YTPlayer.stopVideo();
}
