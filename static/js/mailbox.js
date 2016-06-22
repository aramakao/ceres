$(document).ready(function(){
  //ajaxDjango();

  $("#b_mailbox").click(function(){
    $("#mbx_msg").html('');
  });
  $("#btn_mailbox").click(function(){
    ajaxDjango();
      var phone=$("#mbx_phone").val().trim();
      var user=$("#mbx_user").val().trim();
      var message=$("#mbx_message").val();
      var email=$("#mbx_email").val();
      if(message==''){
        $("#mbx_msg").html('Escriba una sugerencia!');
      }else{
        $.ajax({
          type: "POST",
          url: "/mailbox",
          data: {phone:phone,user:user,message:message,email:email},
           success: function(result){
             $("#mbx_msg").html('Sugerencia enviada con exito!');
             $("#mbx_phone").val('');
             $("#mbx_user").val('');
             $("#mbx_message").val('');
             $("#mbx_email").val('');
          },
          error:function(result){
            $("#mbx_msg").html('Tenemos un problema!');
          }
        });
      }
  });
});
