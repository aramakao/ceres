$(document).ready(function(){
    $("#searchBox" ).focusin(function() {
      var textSearch=$("#searchBox").val().trim();
      if(textSearch==""){
        $('#dpdSearch').hide();
      }
    });
    $("#searchBox" ).keyup(function() {
      var textSearch=$("#searchBox").val().trim();
      if(textSearch!=""){
        $('#dpdSearch').show();
        $.ajax({
          type: "GET",
          url: "/api/search/"+textSearch,
          success: function (data) {
            $("#dpdSearch").empty();
            if(data.length>0){
              jQuery.each(data,function(i,result) {
                $("#dpdSearch").append('<li><a href="'+result.url+'"><div class="media-left"><img class="media-object img-circle img-avatar" src="/media/'+result.image+'"></div><div class="media-body"><strong>'+result.text+'</strong><br><small>'+result.source+'</small></div></a></li>');
              });
              $("#dpdSearch").append('<li role="separator" class="divider"></li>');
              $("#dpdSearch").append('<li><a href="/buscar?query='+textSearch+'"><span class="tab">Ver todos los Resultados</span></a></li>');
            }else{
              $("#dpdSearch").append('<li><a><span class="tab">No hay Resultados</span></a></li>');
            }
          }
        });
      }else {
        $('#dpdSearch').hide();
      }
    });
});
