$('document').ready(function(){

  update_songs();
  // var songs = new Array();
  // $('.songPlay').each(function(){
  //   $(this).parents('.collection-item');
  //   songs.push($(this));
  // });

var song = new Audio();

  $('.songPlay').on("click",function(){
    $('.collection-item[status=playing]').attr('status','stopped')
    var _this = $(this);
    console.log(this);
    parent = _this.parents('.collection-item');
    parent.attr('status','playing');

    $('.collection-item').not(parent).css({
      "background-color":'#fff',
      'color':'#000',
    })
    parent.css({
      'background-color':'#008275',
      'color':'#fff',
    })

    if(_this.attr('state') == 'stop' || typeof _this.attr('state') === 'undefined' ){

    $('#duration').val(0);

    $('.songPlay[state=playing]').text('play_arrow');
    $('.songPlay[state=playing]').attr('state','stop');

    _this.attr({'state':'playing'})
    _this.text("pause");

    var src = _this.attr('data-link');
    $('#cover').css('background-image','url('+_this.attr('cover')+')');

    $("#play").text('pause_circle_outline');

    song.src = src ;
    song.volume =1 ;
    song.play();


    song.addEventListener('loadedmetadata',function(){

      var title = _this.attr('data-name');
      $('.title').text(title);

      $('#duration').attr('max',song.duration);

      var duration = song.duration;
      $('.duration').text(formatSecondsAsTime(duration));

      });

    }
    else if(_this.attr('state') == 'playing' )
    {
      $("#play").text('play_circle_outline');
      _this.text('play_arrow');
      song.pause();
      _this.attr({'state':'stop'});
    }

  });

  song.addEventListener('timeupdate',function (){
    $(".current").text(formatSecondsAsTime(song.currentTime))
      curtime = parseInt(song.currentTime, 10);
          $("#duration").val(curtime);
      });

  $('#play').on('click',function(){
    var _this = $(this);
    if(_this.text() == 'play_circle_outline')
    {
      song.play();
      _this.text('pause_circle_outline');
    }
    else if(_this.text() == 'pause_circle_outline')
    {
      song.pause();
      _this.text('play_circle_outline');

    }
  });
  var shuffle=0;
  $('#shuffle').on('click',function(){
    if(shuffle==0){
      $(this).css({
        'color':'#ef5350',
      });
      shuffle=1;
    }
    else if(shuffle==1){
      $(this).css({
        'color':'#fff',
      });
      shuffle=0;
    }
  });
  var repeat=0;
  $("#repeat").on('click',function(){
    if(repeat==0){
      $(this).text('repeat_one');
      repeat=1;
    }
    else if(repeat==1)
    {
      $(this).text('repeat');
      repeat=0;
    }
  });
  $("#next").on('click',function(){
    var _this = $(this);
    if(shuffle==1){
      var random = songs[Math.floor(songs.length * Math.random())];
      random.trigger('click');
    }
    else if(shuffle==0){
      var item = $('.collection-item[status="playing"]').next('.collection-item');
      item.find('.songPlay').trigger('click');

    }
  });
  $("#prev").on('click',function(){
    var _this = $(this);
    if(shuffle==1){
      var random = songs[Math.floor(songs.length * Math.random())];
      random.trigger('click');
    }
    else if(shuffle==0){
      var item = $('.collection-item[status="playing"]').prev('.collection-item');
      item.find('.songPlay').trigger('click');

    }
  });
  song.addEventListener("ended", function(){
    if(repeat==1){
      song.currentTime=0;
      song.play();
    }
    else if(repeat==0)
    {
      $('#next').trigger('click');
    }
  });
  var volume=1;
  $('#volume').on('click',function(){
    if(volume == 1){
      $(this).text('volume_off');
      song.volume=0;
      volume = 0 ;
    }
    else if(volume==0){
      $(this).text('volume_up');
      song.volume = 1;
      volume = 1;
    }
  });
  $("#duration").on("change", function() {
        song.currentTime = $(this).val();
        $("#duration").attr("max", song.duration);
    });


/////// Our Code
// TODO: clone hidden collection item so you can add to playlist more than once
$(".add_song").click(function() {
        $(this).find( 'li.collection-item' ).show();
        // track = $(this).find( 'li.collection-item' ).clone();
        $(this).find( 'li.collection-item' ).appendTo( "#playlist" );
        // $(this).find( 'li.collection-item' ).hide();
        // update_songs();
});

function update_songs(){
  var songs = new Array();
  $('.songPlay').each(function(){
    $(this).parents('.collection-item');
    songs.push($(this));
  });
  console.log(songs);
}

// Saves songs in playlist
$(function() {
  $('#savePlaylist').click(function(){

    // Check if playlist name
    if ($('#playlist').find('li.collection-header').text() === ""){
        var message = "please give this playlist a name"
        result = window.prompt(message, "default");
        $('#playlist').find('li.collection-header').text(result)
        var playlist_name = result
    } else {
        var playlist_name = $('#playlist').find('li.collection-header').text()
    };

    // Variables to send by AJAX
    var playlist_name = $('#playlist').find('li.collection-header').text()
    var playlist_id = parseInt($('#playlist').find('li.collection-id').text())
    var song_id_list = []

    // iterate through song elements currently in playlist and get ids
    $('#playlist').find( '.songPlay' ).each(function(){
      var _this = $(this);
      song_id_list.push(_this.attr('song-id'));
    });

    // Create JSON object to send to server
    var obj = { 'playlist_name' : playlist_name, 'playlist_id' : playlist_id, 'song_id_list' : song_id_list};
    var myJSON = JSON.stringify(obj);
    $.ajax({
        url: '/save_playlist',
        type: 'POST',
        data: myJSON,
        contentType: 'application/json',
        // dataType: 'json',
        success: function(response) {
            console.log(response);
            $('#playlist').find('li.collection-id').text(response)
        },
        error: function(error) {
            console.log(error);
        }
    });
});
});

$(function() {
  $('#loadPlaylist').click(function(){
    // var playlist_id = $('#playlists_select option:selected').text()
    console.log("load-clicked")
    var playlist_id = $('#select option:selected').val();
    var playlist = []
    var obj = { 'playlist_id' : playlist_id }
    var myJSON = JSON.stringify(obj);
    $.ajax({
        url: '/load_playlist',
        type: 'POST',
        data: myJSON,
        contentType: 'application/json',
        success: callback,
        error: function(error) {
            console.log(error);
        }
    });

    // var $i = $('<i />').addClass("material-icons songPlay")
    // $i.attr({
    //   "song-id=" : item[0],
    //   "data-link": item[2],
    //   "data-name": item[1],
    //   "cover"    : item[3]
    // });

  });
});

function callback(data) {
  var playlist = JSON.parse(data);

  playlist.forEach(function(item){
      $(" #playlist ")
        .append($("<li></li>").addClass("collection-item")
          .append($("<div></div").text(item[1])
            .append($('<a></a>').addClass("seconday-content").attr("href", "#playsection")
              .append($('<i></i>').addClass("material-icons songPlay")
                .text("play_arrow")
                .attr({
                  "song-id"  : item[0],
                  "data-link": item[2],
                  "data-name": item[1],
                  "cover"    : item[3]
                })))))})}


 // callback
      // $('<li/>', { "class": "collection-record", text:(item[1]) })

      //     $('<div/>', { text:(item[1]) }.append(
      //       $('<a/>', { "href": "#" , "class": "secondary-content"} ).append(
      //         $('<i/>',
      //           { "class": "material-icons songPlay",
      //             "song-id=" : item[0],
      //             "data-link": item[2],
      //             "data-name": item[1],
      //             "cover"    : item[3]
      //           })
      //       )
      //     )
      // );




//////End our code

function formatSecondsAsTime(secs) {
  var hr  = Math.floor(secs / 3600);
  var min = Math.floor((secs - (hr * 3600))/60);
  var sec = Math.floor(secs - (hr * 3600) -  (min * 60));

  if (min < 10){
    min = "0" + min;
  }
  if (sec < 10){
    sec  = "0" + sec;
  }

  return min + ':' + sec;
}

$('#fav').on('click',function(){
  var path = "static/images/air-horn-club-sample.mp3"
  var snd = new Audio(path);
  snd.play();
  color1 = Math.floor((Math.random() * 255) + 1);
  color2 = Math.floor((Math.random() * 255) + 1);
  color3 = Math.floor((Math.random() * 255) + 1);

  color = 'rgb('+color1+','+color2+','+color3+')';

  $('#fav').queue(function(next){
    $('#fav').css({
      "transform":"rotate(180deg)",
    });
    next();
  });
  $('#fav').queue(function(next){
    $('#fav').css('color', color);
    $('#fav').css({
      "transform":" rotate(360deg)",
    });
    next();
  });
  $("#fav").delay(400).queue(function(next){
    $("#fav").css({
      'transform':'rotate(0deg)',
    });
    next();
  });

});

});
