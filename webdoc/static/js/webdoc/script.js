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

    $("#main_video, #force_quality").fadeOut(400, function(){
        $('#main_video').remove();
        $('#active_focus').remove();
    });

    $('#player_preview, #chapter_selector').fadeIn();

    $('#player_closer').hide();
    if(video_quality != 'low'){
        $('#focus_list').show();
    }
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

function show_player(video, quality, play){
    if(typeof(play) == 'undefined'){
        play = true;
    }
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
    $('<video/>', {
        id:'main_video',
        width: width,
        height: height,
        class: "video_player",
        controls: true
    }).appendTo($("#content"));

    $('#main_video')[0].onended = function(e) {
        console.log("Video ended");
        hide_player();
        select_topic("next");
    };

    $('<div/>', {
        id:'active_focus'
    }).appendTo($("#content"));

    $('<div/>', {
        id:'open_focus'
    }).appendTo($("#content"));

    $("#main_video").hide();

    $("#main_video, #force_quality").fadeIn("slow",function(){
        if(play){
            $("#main_video")[0].play();
        }
    });
    $('#force_quality_'+video_quality).addClass('active');

    $('#player_preview, #chapter_selector').fadeOut();

    $('#player_closer').show();

    var videos_location = "";
    //videos_location = 'http://agripo.websailor.fr/';
    videos_location = 'http://videos.agripo.briceparent.info/videos-agripo/';

    $('<source/>', {
        src: videos_location+video+'_'+video_quality+".mp4",
        type: "video/mp4"
    }).appendTo($("#main_video"));

    $('<source/>', {
        src: videos_location+video+'_'+video_quality+".webm",
        type: "video/webm"
    }).appendTo($("#main_video"));

    $('<source/>', {
        src: videos_location+video+'_'+video_quality+".ogv",
        type: "video/ogg"
    }).appendTo($("#main_video"));

    $("#main_video").on("timeupdate", function (e) {
        var t = e.target.currentTime;

        for(var focus in focus_list[video]){
            if(focusShown == "" && t >= focus_list[video][focus][0] && t < focus_list[video][focus][1]){
                var thisVid = video+'_'+focus;
                showFocus(thisVid);
            }else if(focusShown == video+'_'+focus && t >= focus_list[video][focus][1]){
                hideFocus();
            }else if(focusShown == video+'_'+focus && t < focus_list[video][focus][0]){
                hideFocus();
            }
        }
    });
}

function showFocus(focus){
    focusShown = focus;
    console.debug("Showing focus #",focus);

    $('#active_focus').html($('#focus_'+focus).html());
    $('#active_focus').fadeIn('slow');
}

function hideFocus(){
    focusShown = 0;
    console.debug("Hiding active focus");
    $('#active_focus').fadeOut();
}
function focus_open_this_one(theme, focus){
    show_player('theme'+theme, "medium", false);

    $("#main_video")[0].addEventListener('loadedmetadata', function(){
        $("#main_video")[0].currentTime = focus_list['theme'+theme][focus][0];
    }, false);
}

function focus_open(){
    $("#main_video")[0].pause();
    $('#player_closer').fadeOut();

    $('#active_focus').addClass("full");
}
function focus_close(){
    $("#main_video")[0].play();
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
