$(document).ready(function(){

    $("#id_VHost").change(function(){
        var vhostid = $(this).val();

        $("#Net_Panel").hide()
        var data = {
            "vhostid":  vhostid,
            "jq_req": "ds_type",
        }


        if (vhostid != 0){

             $.ajax({
                "url": "/ajax/dstore_update_query/",
                "type": "POST",
                "data": data,
                "dataType": 'json',
                "success":function(data){

                    

                    var vendor = data.vendor;


                    if (vendor == "ZN"){

                        var zpool = data.zpool_list;
                        

                        $("#Dpath_Panel").empty();
                        $("#Dpath_Panel").append('<select class="form-control"  id="id_dpath"></select>');
                        for (item in zpool){
                            $("#id_dpath").append('<option value="' + zpool[item] + '">' + zpool[item] + '</option>');
                        }
                        $("#ds_vendor").attr('value', 'ZN');

                    }else if (vendor == "VB"){
                         $("#Dpath_Panel").empty();
                         $("#Dpath_Panel").append('<input type="text" class="form-control"  id="id_dpath" value="">');
                         $("#ds_vendor").attr('value', 'VB');

                    }
                }

            });

        }


    });

    $("#btn_open_from").click(function(e){


        e.preventDefault();


        

        var data = { jq_req: "vhost"}

        $.ajax({
            "url": "/ajax/dstore_update_query/",
            "type": "POST",
            "data": data,
            "dataType": 'json',
            "success":function(data){
                var vhost = JSON.parse(data.vhosts)
                $("#id_VHost").append("<option value='0' selected>- Select -</option>");
                for (key in vhost){
                    $("#id_VHost").append("<option value='" + vhost[key].id + "'>" + vhost[key].name + "</option>");

                }
            }
        });
        $("#md_dstore_form").modal();
    });

    $("#btn_create_dstore").click(function(e){
        e.preventDefault();
        var ds_vendor = $('#ds_vendor').val();
        var data ={
            name: $("#id_name").val(),
            vhost: $("#id_VHost").val(),
        }

        if ( ds_vendor == "ZN"){
            data['dpath'] = $("#id_dpath option:selected").text();
        } else{
            data['dpath'] = $("#id_dpath").val();
        }

        $.ajax(
             {
                 "type": "POST",
                 "dataType": "json",
                 "url": "/vhost/datastore/new/",
                 "data": data,
                 "success": function(data) {
                    $("#info_msg").text(data.msg);
                    $("#md_dstore_form").modal('hide');
                 },
                 error: function(){
                     alert(data.message);
                 },
             }
         );


    });

    $('input[id^="btn_delete_dstore"]').click(function(e){
        e.preventDefault();

        var pdiv = $(this).parent().attr('id');
        var ds_name = $("#"+ pdiv + "> #dstore_name").val();
        var ds_id = $("#"+ pdiv + "> #dstore_id").val();
        var ds_path = $("#"+ pdiv + "> #dstore_path").val();
        $("#delete_msg").text("The Datastore " + ds_name +  " with the path " + ds_path + " will be deleted with  all the Virtual Machines and/or contained data. Please confirm action");
        $("#del_ds").attr("value",ds_id);
        $("#md_delete_dstore").modal();
    });

    $("#btn_delete_dstore_ok").click(function(e){
        e.preventDefault();

        var del_ds = $("#del_ds").val();
        

        var data = { ds_id: del_ds};

        $("#md_delete_dstore").modal("hide");

        $.ajax(
             {
                 "type": "POST",
                 "dataType": "json",
                 "url": "/ajax/deldstore/",
                 "data": data,
                 "success": function(data) {
                    $("#info_msg").text(data.msg);
                    $("#md_delete_dstore").modal('hide');
                 },
                 error: function(){
                     alert(data.message);
                 },
             }
         );



    });

    // When the user clicks on <span> (x), close the modal
    $(".close").click(function() {
        $("#md_delete_net").modal("hide");
    });

    $("#md_dstore_form").on('hidden.bs.modal', function () {
        $("#md_msg").modal();
    });

    $("#md_delete_dstore").on('hidden.bs.modal', function () {
        $("#md_msg").modal();
    });

    //Referesh
    $("#btn_update").on('click',function (e) {
        e.preventDefault();

        var data = {
            type: "datastore",
        }
        $.ajax(
            {
                "type": "POST",
                "dataType": "json",
                "url": "/ajax/updatedb/",
                "data": data,
                success: function(data) {
                    
                    $("#info_msg").text(data.msg);
                    $("#md_msg").modal();
                },
                error: function(){
                    alert("Error detected");
                },
            }
        );
    });

    // MSG



    $("#md_msg").on('hidden.bs.modal', function () {
        location.reload(true);
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
