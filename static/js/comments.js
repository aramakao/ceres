$(document).ready(function(){
  ajaxDjango();
  load_comments();
  function load_comments(argument) {
    var id=$("#id_comment_bx").val();
    var object=$("#object_comment_bx").val();
    var label=$("#label_comment_bx").val();
    $.ajax({
      type: "GET",
      url: "/comentarios/getComments",
      data: {id:id,object:object,label:label},
       success: function(data){
        jQuery.each(data,function(i,comment) {
          insert_comment(comment);
        });
      },
      error:function(data){
        console.log(data);
      }
    });
  }

  function insert_comment(comment) {
    $("#comments_list").append("<div class='media'><div class='media-left'><a href='/usuario/"+comment.slug+"'><img class='media-object img-circle img-avatar' src='"+comment.avatar+"'></a></div><div class='media-body'><a href='/usuario/"+comment.slug+"'><h4 class='media-heading'>"+comment.fullName+"</h4></a>"+comment.message+"</div><br><small>Hace "+comment.date+"</small></div><hr>");
  }
  $("#lbl_comment_bx").hide();
  $("#btn_comment_bx").click(function(){
    var comment=$("#comment_bx").val().trim();
    if(comment==""){
      $("#lbl_comment_bx").html('Escribe un comentario!');
      $("#lbl_comment_bx").show();
    }
      else{
        var id=$("#id_comment_bx").val();
        var object=$("#object_comment_bx").val();
        var label=$("#label_comment_bx").val();
        $.ajax({
          type: "POST",
          url: "/comentarios/",
          data: {comment:comment,id:id,object:object,label:label},
           success: function(data){
             $("#comment_bx").val("");
             $("#lbl_comment_bx").show();
             $("#lbl_comment_bx").html("Comentario publicado!");
             $("#comments_list").html("");
            jQuery.each(data,function(i,comment) {
              insert_comment(comment);
            });
          },
          error:function(data){
            $("#lbl_comment_bx").html('Tenemos un problema!');
            $("#lbl_comment_bx").show();
          }
        });
      }
  });
});
