$(document).ready(function(){

    $("#id_VHost").change(function(){
        var vhostid = $(this).val();

        $("#Net_Panel").hide()
        var data = {
            "vhostid":  vhostid,
            "jq_req": "vsw_type"
        }


        if (vhostid != 0){

             $.ajax({
                "url": "/ajax/net_update_query/",
                "type": "POST",
                "data": data,
                "dataType": 'json',
                "success":function(data){

                    var vendor = data.vendor;


                    if (vendor == "VW"){

                        var type = JSON.parse(data.vswlist);

                        $("#np_title").text("VmWare Network Data");
                        $("#id_NType").empty();
                        for (key in type){
                            $("#id_NType").append("<option value='" + type[key].vswitch + "'>" + type[key].vswitch + "</option>");
                        }
                        $("#Net_Panel").show()
                    }else if (vendor == "VW"){
                         $("#id_NType").empty();
                         $("#id_NType").append("<option value='0'>intnet</option>");
                    }else if (vendor == "ZN"){
                         $("#id_NType").empty();
                         $("#id_NType").append("<option value='0'>portgroup</option>");
                    }
                }

            });

        }


    });

    $('input[id^="btn_open_from"]').click(function(e){

        e.preventDefault();

        var data = { jq_req: "vhost"}

        $.ajax({
            "url": "/ajax/net_update_query/",
            "type": "POST",
            "data": data,
            "dataType": 'json',
            "success":function(data){
                var vhost = JSON.parse(data.vhosts)
                for (key in vhost){
                    $("#id_VHost").append("<option value='" + vhost[key].id + "'>" + vhost[key].name + "</option>");
                }
            }
        });
        $("#md_net_form").modal();
    });

    $("#btn_create_net").click(function(e){
        e.preventDefault();
        var data ={
            name: $("#id_name").val(),
            vhost: $("#id_VHost").val(),
            ntype: $("#id_NType option:selected").text(),
        }

        $.ajax(
             {
                 "type": "POST",
                 "dataType": "json",
                 "url": "/vhost/network/new/",
                 "data": data,
                 "success": function(data) {
                    $("#info_msg").text(data.msg);
                    $("#md_net_form").modal('hide');
                 },
                 error: function(){
                     alert(data.message);
                 },
             }
         );


    });

    $('input[id^="btn_delete_network"]').click(function(e){
        e.preventDefault();


        var pdiv = $(this).parent().attr('id');
        var vsw_name = $("#"+ pdiv + "> #vsw_name").val();
        var vsw_id = $("#"+ pdiv + "> #vsw_id").val();
        console.log("id VSWITHC " + vsw_id)
        $("#delete_msg").text("The Virtual Network " + vsw_name +  "is going to be deleted");
        $("#del_vsw").attr("value",vsw_id);
        $("#md_delete_net").modal();
    });

    $("#btn_delete_network_ok").click(function(e){
        e.preventDefault();

        var vsw_id = $("#del_vsw").val();
        console.log("id VSWITHC " + vsw_id);

        var data = { vsw_id: vsw_id};

        $("#md_delete_net").modal("hide");

        $.ajax(
             {
                 "type": "POST",
                 "dataType": "json",
                 "url": "/ajax/delnet/",
                 "data": data,
                 "success": function(data) {
                    $("#info_msg").text(data.msg);
                    $("#md_delete_net").modal('hide');

                 },
                 error: function(){
                     alert(data.message);
                 },
             }
         );



    });

    $("#md_net_form").on('hidden.bs.modal', function () {
        $("#md_msg").modal();
    });

    $("#md_delete_net").on('hidden.bs.modal', function () {
        $("#md_msg").modal();
    });


    $("#md_msg").on('hidden.bs.modal', function () {
        location.reload(true);
    });


    // When the user clicks on <span> (x), close the modal
    $(".close").click(function() {
        $("#md_delete_net").modal("hide");
    });

    // CSRF code

    function getCookie(name) {
            var cookieValue = null;
            var i = 0;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (i; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup(
        {
            crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        }
    );


});


