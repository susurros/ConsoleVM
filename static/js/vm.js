$(document).ready(function(){

    //Create VM

    $("#id_VHost").change(function(){
        var vhostid = $(this).val();

        var data = {vhostid:  vhostid}

        if (vhostid != 0){
             $.ajax({
                "url": "/ajax/vm_update_query/",
                "type": "POST",
                "data": data,
                "dataType": 'json',
                "success":function(data){

                    var dslist = JSON.parse(data.dslist);
                    var vswlist = JSON.parse(data.vswlist);
                    var oslist = JSON.parse(data.oslist);
                    var drivers = data.drivers;
                    var vendor = data.vendor;
                    var isos = JSON.parse(data.isolist);

                    console.log (vendor);

                    if (vendor == "ZN"){
                        $("#Net_Body").empty();
                        $("#Net_Body").append(
                            '<div class="row"><div class="form-group">'+
                                    '<div class="col-md-2"><label for="id_vswitch">Networks</label></div>'+
                                    '<div class="col-md-4"><select class="form-control" id="id_vswitch"><option value="0">- Select -</option></select></div>'+
                            '</div><!-- .form-group --></div><!-- .row -->'
                        );
                        $("#id_vswitch").empty();
                        for (key in vswlist){
                            $("#id_vswitch").append("<option value='"+vswlist[key].id+"'>"+vswlist[key].vsw +"</option>");
                        }
                        $("#Medium").empty();
                        $("#Remote_body").empty();
                        $("#Remote_body").append(
                            '<div class="row"><div class="form-group">'+
                                '<div class="col-md-2"><label class="control-label" for="rdp_port">Port</label></div>' +
                                '<div class="col-md-4"><input class="form-control" type="text"  id="rdp_port" value=""></div>'+
                            '</div><!-- ./form group --></div>'
                        );
                    }
                    else {
                        $("#Net_Body").empty();
                        $("#Net_Body").append(
                            '<div class="row"><div class="form-group">'+
                                    '<div class="col-md-2"><label for="id_vswitch">Networks</label></div>'+
                                    '<div class="col-md-4"><select class="form-control" id="id_vswitch"><option value="0" selected>- Select -</option></select></div>'+
                                    '<div class="col-md-2"><label for="id_driver">Driver</label></div>'+
                                    '<div class="col-md-4"><select class="form-control" id="id_driver"><option value="0" selected>- Select -</option></select></div>'+
                            '</div><!-- .form-group --></div><!-- .row -->'
                        );
                        $("#id_vswitch").empty();
                        for (key in vswlist){
                            $("#id_vswitch").append("<option value='"+vswlist[key].id+"'>"+vswlist[key].vsw +"</option>");
                        }
                        $("#id_driver").empty();
                        for (key in drivers){
                            $("#id_driver").append("<option value='"+drivers[key]+"'>"+drivers[key] +"</option>");
                        }

                        $("#Medium").empty();
                        $("#Medium").append(
                            '<div class="panel box box-primary"><div class="box-header with-border"><h4 class="box-title">Medium Data</h4></div>'+
                                '<div class="box-body"><div class="row"><div class="form-group">' +
                                    '<div class="col-md-2"><label for="image">Image:</label></div>'+
                                    '<div class="col-md-4"><select class="form-control" type="text" id="image"></select></div>' +
                                '</div><!-- ./form group --></div><!-- .row --></div><!-- .box-body -->'+
                            '</div><!-- Medium Data -->'
                        );
                        for (key in isos){
                            $("#image").append("<option value='"+isos[key].id+"'>"+isos[key].name +"</option>");
                        }

                        if (vendor== "VW"){
                            $("#Remote_body").empty();
                            $("#Remote_body").append(
                                '<div class="row"><div class="form-group">'+
                                    '<div class="col-md-2"><label class="control-label" for="rdp_pass">Password:</label></div>' +
                                    '<div class="col-md-4"><input class="form-control" type="text"  id="rdp_pass" value=""></div>'+
                                    '<div class="col-md-2"><label class="control-label" for="rdp_port">Port</label></div>' +
                                    '<div class="col-md-4"><input class="form-control" type="text"  id="rdp_port" value=""></div>'+
                                '</div><!-- ./form group --></div>'
                            );
                        }
                        else {
                            $("#Remote_body").empty();
                            $("#Remote_body").append(
                                '<div class="row"><div class="form-group">'+
                                    '<div class="col-md-2"><label for="rdp_user">User:</label></div>'+
                                    '<div class="col-md-4"><input class="form-control" type="text" id="rdp_user" maxlength="30" value="" ></div>'+
                                    '<div class="col-md-2"><label class="control-label" for="rdp_pass">Password:</label></div>'+
                                    '<div class="col-md-4"><input class="form-control" type="text"  id="rdp_pass" value=""></div>'+
                                '</div><!-- ./form group --></div>'+
                                '<div class="row"><div class="form-group">'+
                                    '<div class="col-md-2"><label class="control-label" for="rdp_port">Port</label></div>'+
                                    '<div class="col-md-4"><input class="form-control" type="text"  id="rdp_port" value="" ></div>' +
                                '</div><!-- ./form group --></div>'
                            )
                        }

                    }

                    $("#id_ostype").empty();
                    for (key in oslist){
                        $("#id_ostype").append("<option value='"+oslist[key].id+"'>"+oslist[key].os +"</option>");
                    }
                    $("#id_datastore").empty();
                    for (key in dslist){
                        $("#id_datastore").append("<option value='"+dslist[key].id+"'>"+dslist[key].ds +"</option>");
                    }

                    if (vendor == "VW"){
                        $("#Remote_Body").empty();
                        $("#Remote_Body").append(
                            '<div class="row"><div class="form-group">' +
                                '<div class="col-md-2"><label class="control-label" for="rdp_pass">Password:</label></div>'+
                                '<div class="col-md-4"><input class="form-control" type="text"  id="rdp_pass" value="'+ data.rdppass+'"></div>' +
                                '<div class="col-md-2"><label class="control-label" for="rdp_port">Port</label></div>'+
                                '<div class="col-md-4"><input class="form-control" type="text"  id="rdp_port" value="' + data.rdpport + '" ></div>'+
                            '</div><!-- ./form group --></div>'
                        )
                    }
                    else {
                        $("#Remote_Body").empty();
                        $("#Remote_Body").append(
                            '<div class="row"><div class="form-group">' +
                                '<div class="col-md-2"><label for="rdp_user">User:</label></div>' +
                                '<div class="col-md-4"><input class="form-control" type="text" id="rdp_user" maxlength="30" value="' + data.rdpuser + '" ></div>'+
                                '<div class="col-md-2"><label class="control-label" for="rdp_pass">Password:</label></div>'+
                                '<div class="col-md-4"><input class="form-control" type="text"  id="rdp_pass" value="'+ data.rdppass+'"></div>' +
                            '</div><!-- ./form group --></div>'+
                            '<div class="row"><div class="form-group">'+
                                '<div class="col-md-2"><label class="control-label" for="rdp_port">Port</label></div>'+
                                '<div class="col-md-4"><input class="form-control" type="text"  id="rdp_port" value="' + data.rdpport + '" ></div>'+
                            '</div><!-- ./form group --></div>'
                        );
                    }
                }
            });

        }
    });

    $("#btn_create_vm").click(function(e){
        e.preventDefault();

        var data ={
            name: $("#id_name").val(),
            vhost: $("#id_VHost").val(),
            datastore: $("#id_datastore").val(),
            cpu: $("#id_cpu").val(),
            mem: $("#id_mem").val(),
            ostype: $("#id_ostype").val(),
            dsize: $("#id_size").val(),
            vswitch: $("#id_vswitch").val(),
            driver: $("#id_driver").val(),
            image: $("#image").val(),
            rdpuser: $("#rdp_user").val(),
            rdpport: $("#rdp_port").val(),
            rdppass: $("#rdp_pass").val(),
        }

        console.log(data)

        $.ajax(
             {
                 "type": "POST",
                 "dataType": "json",
                 "url": "/vmachine/new/",
                 "data": data,
                 "success": function(data) {
                     $("#info_msg").text(data.msg);
                     $("#md_msg_form").modal();
                 },
                 error: function(){
                     alert(data.message);
                 },
             }
         );


    });

    //Delete VM

    $('input[id^="delete_vm"]').click(function(e) {
            e.preventDefault();
            var pdiv = $(this).parent().attr('id');
            var data = {
                vmid: $("#"+ pdiv + "> #vmid").val(),
            }
            $.ajax(
                {
                    "type": "POST",
                    "dataType": "json",
                    "url": "/ajax/deletevm/",
                    "data": data,
                    "success": function(data) {
                         $("#info_msg").text(data.msg);
                         $("#md_msg").modal();
                    },
                    error: function(){
                        alert("Error detected");
                    },
                }
            );
        });

    //Modify VM

    $('input[id^="modify_vm"]').click(function(e) {
            e.preventDefault();
            var pdiv = $(this).parent().attr('id');
            var data = {
                vmid: $("#"+ pdiv + "> #vmid").val(),
                jqreq: "get_data",
            }
            $.ajax(
                {
                    "type": "POST",
                    "dataType": "json",
                    "url": "/ajax/modifyvm/",
                    "data": data,
                    "success": function(data) {
                        console.log(data) //quit only for debugging
                        console.log(data.vhostname)

                        var vswlist = JSON.parse(data.vswlist);
                        var oslist = JSON.parse(data.oslist);
                        var isos = JSON.parse(data.isolist);
                        var drivers = data.drivers;
                        var vendor = data.vendor;


                        $("#mod_id_name").attr('value',data.vmname)
                        $("#mod_id_vhost").attr('value',data.vhostname)
                        $("#mod_id_cpu").attr('value',data.cpu)
                        $("#mod_id_mem").attr('value',data.mem)
                        $("#mod_id_vmid").attr('value',data.vmid)
                        $("#mod_id_vhost").attr('value',data.vhostid)


                        if (vendor == "ZN"){
                            $("#Net_Body").empty();
                            $("#Net_Body").append(
                                '<div class="row"><div class="form-group">'+
                                        '<div class="col-md-2"><label for="mod_id_vswitch">Networks</label></div>'+
                                        '<div class="col-md-4"><select class="form-control" id="mod_id_vswitch"><option value="0">- Select -</option></select></div>'+
                                '</div><!-- .form-group --></div><!-- .row -->'
                            );
                            $("#mod_id_vswitch").empty();
                            for (key in vswlist){
                                if (vswlist[key].id == data.vswid) {
                                    $("#mod_id_vswitch").append("<option value='" + vswlist[key].id + "' selected>" + vswlist[key].vsw + "</option>");
                                }
                                else{
                                    $("#mod_id_vswitch").append("<option value='" + vswlist[key].id + "'>" + vswlist[key].vsw + "</option>");
                                }
                            }
                            $("#Medium").empty()
                        }
                        else {
                        $("#Net_Body").empty();
                        $("#Net_Body").append(
                            '<div class="row"><div class="form-group">'+
                                    '<div class="col-md-2"><label for="mod_id_vswitch">Networks</label></div>'+
                                    '<div class="col-md-4"><select class="form-control" id="mod_id_vswitch"><option value="0" selected>- Select -</option></select></div>'+
                                    '<div class="col-md-2"><label for="mod_id_driver">Driver</label></div>'+
                                    '<div class="col-md-4"><select class="form-control" id="mod_id_driver"><option value="0" selected>- Select -</option></select></div>'+
                            '</div><!-- .form-group --></div><!-- .row -->'
                        );
                        $("#mod_id_vswitch").empty();
                        for (key in vswlist){
                            if (vswlist[key].id == data.vswid) {
                                $("#mod_id_vswitch").append("<option value='" + vswlist[key].id + "' selected>" + vswlist[key].vsw + "</option>");
                            }
                            else{
                                $("#mod_id_vswitch").append("<option value='" + vswlist[key].id + "'>" + vswlist[key].vsw + "</option>");
                            }
                        }
                        $("#mod_id_driver").empty();
                        for (key in drivers){
                            $("#mod_id_driver").append("<option value='"+drivers[key]+"'>"+drivers[key] +"</option>");
                        }
                        $("#Medium").empty();
                        $("#Medium").append(
                            '<div class="panel box box-primary"><div class="box-header with-border"><h4 class="box-title">Medium Data</h4></div>'+
                                '<div class="box-body"><div class="row"><div class="form-group">' +
                                    '<div class="col-md-2"><label for="image">Image:</label></div>'+
                                    '<div class="col-md-4"><select class="form-control" type="text" id="image"></select></div>' +
                                '</div><!-- ./form group --></div><!-- .row --></div><!-- .box-body -->'+
                            '</div><!-- Medium Data -->'
                        )
                        for (key in isos){
                            if (isos[key].id == data.isoid){
                                   $("#image").append("<option value='"+isos[key].id+"' selected>"+isos[key].name +"</option>");
                            }
                            else {
                                $("#image").append("<option value='"+isos[key].id+"'>"+isos[key].name +"</option>");
                            }
                        }
                    }

                        $("#mod_id_ostype").empty();
                        for (key in oslist){
                            if (data.osname == oslist[key].os){
                                $("#mod_id_ostype").append("<option value='"+oslist[key].id+"' selected >"+oslist[key].os +"</option>");
                            }
                            else{
                                $("#mod_id_ostype").append("<option value='"+oslist[key].id+"'>"+oslist[key].os +"</option>");

                            }
                        }
                        if (vendor == "VW"){
                            $("#Remote_Body").empty();
                            $("#Remote_Body").append(
                                '<div class="row"><div class="form-group">' +
                                    '<div class="col-md-2"><label class="control-label" for="mod_rdp_pass">Password:</label></div>'+
                                    '<div class="col-md-4"><input class="form-control" type="text"  id="mod_rdp_pass" value="'+ data.rdppass+'"></div>' +
                                    '<div class="col-md-2"><label class="control-label" for="mod_rdp_port">Port</label></div>'+
                                    '<div class="col-md-4"><input class="form-control" type="text"  id="mod_rdp_port" value="' + data.rdpport + '" ></div>'+
                                '</div><!-- ./form group --></div>'
                            )
                        }
                        else {
                            $("#Remote_Body").empty();
                            $("#Remote_Body").append(
                                '<div class="row"><div class="form-group">' +
                                    '<div class="col-md-2"><label for="mod_rdp_user">User:</label></div>' +
                                    '<div class="col-md-4"><input class="form-control" type="text" id="mod_rdp_user" maxlength="30" value="' + data.rdpuser + '" ></div>'+
                                    '<div class="col-md-2"><label class="control-label" for="mod_rdp_pass">Password:</label></div>'+
                                    '<div class="col-md-4"><input class="form-control" type="text"  id="mod_rdp_pass" value="'+ data.rdppass+'"></div>' +
                                '</div><!-- ./form group --></div>'+
                                '<div class="row"><div class="form-group">'+
                                    '<div class="col-md-2"><label class="control-label" for="mod_rdp_port">Port</label></div>'+
                                    '<div class="col-md-4"><input class="form-control" type="text"  id="mod_rdp_port" value="' + data.rdpport + '" ></div>'+
                                '</div><!-- ./form group --></div>'
                            );
                        }

                        $("#VMmodify_modal").modal()
                    },
                    error: function() {
                        alert("Error detected");
                    } ,
                }
             );
        });

    $("#modify_form").click(function (e) {
            e.preventDefault();
            var data = {
                name: $("#mod_id_name").val(),
                vhostid: $("#mod_id_vhostid").val(),
                vmid: $("#mod_id_vmid").val(),
                cpu: $("#mod_id_cpu").val(),
                mem: $("#mod_id_mem").val(),
                osid: $("#mod_id_ostype").val(),
                vswid: $("#mod_id_vswitch").val(),
                driver: $("#mod_id_driver").val(),
                rpduser: $("#mod_rdp_user").val(),
                rdppass: $("#mod_rdp_pass").val(),
                rdpport: $("#mod_rdp_port").val(),
                image: $("#image").val(),
                jqreq: "modify" ,
            }

            $("#VMmodify_modal").modal('hide')

            $.ajax(
                {
                    "type": "POST",
                    "dataType": "json",
                    "url": "/ajax/modifyvm/",
                    "data": data,
                    "success": function (data) {
                         $("#info_msg").text(data.msg);
                         $("#md_msg").modal();
                    },
                    error: function () {
                        alert("Error detected");
                    }
                }
            );
        });

    //Clone VM

    $('input[id^="clone_vm"]').click(function(e) {
            e.preventDefault();
            var pdiv = $(this).parent().attr('id');
            var vmid = $("#"+ pdiv + "> #vmid").val();

            $("#clone_vmid").attr('value',vmid)
            $("#clone_modal").modal()
    });

    $("#clone_form").click(function (e) {
            e.preventDefault();
            var data = {
                clid:  $("#clone_vmid").val(),
                name: $("#clone_name").val(),
            }
            $("#clone_modal").modal('hide')
            $.ajax(
                {
                    "type": "POST",
                    "dataType": "json",
                    "url": "/ajax/clonevm/",
                    "data": data,
                    "success": function (data) {
                         $("#info_msg").text(data.msg);
                         $("#md_msg").modal();
                    },
                    error: function () {
                        alert("Error detected");
                    }
                }
            );
        });


    //Control VM

    $('input[id^="start_vm"]').click(function(e) {
            e.preventDefault();
            var pdiv = $(this).parent().attr('id');
            var data = {
                vmid: $("#"+ pdiv + "> #vmid").val(),
            }
            console.log(data)
            $.ajax(
                {
                    "type": "POST",
                    "dataType": "json",
                    "url": "/ajax/startvm/",
                    "data": data,
                    "success": function(data) {
                         $("#info_msg").text(data.msg);
                         $("#md_msg").modal();


                    },
                    error: function(){
                        alert("Error detected");
                    },
                }
            );
        });

    $('input[id^="stop_vm"]').click(function(e) {
            e.preventDefault();
            var pdiv = $(this).parent().attr('id');
            var data = {
                vmid: $("#"+ pdiv + "> #vmid").val(),
            }
            $.ajax(
                {
                    "type": "POST",
                    "dataType": "json",
                    "url": "/ajax/stopvm/",
                    "data": data,
                    "success": function(data) {
                         $("#info_msg").text(data.msg);
                         $("#md_msg").modal();
                    },
                    error: function(){
                        alert("Error detected");
                    },
                }
            );
        });

    $('input[id^="pause_vm"]').click(function(e) {
            e.preventDefault();
            var pdiv = $(this).parent().attr('id');
            var data = {
                vmid: $("#"+ pdiv + "> #vmid").val(),
            };
            $.ajax(
                {
                    "type": "POST",
                    "dataType": "json",
                    "url": "/ajax/pausevm/",
                    "data": data,
                    "success": function(data) {
                         $("#info_msg").text(data.msg);
                         $("#md_msg").modal();
                    },
                    error: function(){
                        alert("Error detected");
                    },
                }
            );

        });


    //Snapshots

    $('input[id^="mng_snap"]').click(function(e) {
            e.preventDefault();
            var pdiv = $(this).parent().attr('id');
            var data = {
                vmid: $("#"+ pdiv + "> #vmid").val(),
            }
            $.ajax(
                {
                    "type": "POST",
                    "dataType": "json",
                    "url": "/ajax/mngsnap/",
                    "data": data,
                    "success": function(data) {
                        var modal_snap= $("#Snap_modal > .modal-dialog > .box > .box-body > .table > tbody ")  ;
                        var modal_snap_header=$("#Snap_modal > .modal-dialog > .box > .box-header > h3")
                        var snap = JSON.parse(data.snaplist);

                        modal_snap.html('');
                        modal_snap_header.html('');

                        modal_snap_header.append("Snapshots for the Virtual Machine: <b>" + data.vm_name + "</b>")

                        for (key in snap){

                            if (snap[key].current == "True"){
                                var current =   "<i class='fa fa-2x fa-arrow-circle-up fa-fw text-success'></i>"
                            }
                            else {
                                var current =   "<i class='fa fa-2x fa-arrow-circle-left fa-fw text-warning'></i>"
                            }

                            modal_snap.append(
                                "<tr>" +
                                    "<td>" + snap[key].name + "</td>"    +
                                    "<td>" + snap[key].suuid + "</td>" +
                                    "<td>" + current + "</td>" +
                                    "<td>" +
                                        "<div class='btn-group-xs btn-group-lg' id='snap_ctrl_modal"+ snap[key].suuid + "'>"  +
                                            "<input type='hidden' id='vmid' name='vmid' value='" + data.vm_id + "'>"+
                                            "<input type='hidden' id='suuid' name='suuid' value='" + snap[key].suuid + "'>"+
                                            "<input type='button' id='snap_restore' class='btn btn-primary' value='Restore'>" +
                                            "<input type='button' id='snap_delete' class='btn btn-danger' value='Delete'>  " +
                                        "</div>" +
                                    "</td>"  +
                                "</tr>"
                            );
                        }


                        $('input[id^="snap_restore"]').click(
                            function(e) {
                                e.preventDefault();
                                var pdiv = $(this).parent().attr('id');
                                var data = {
                                    vmid: $("#"+ pdiv + "> #vmid").val(),
                                    suuid: $("#"+ pdiv + "> #suuid").val(),
                                }
                                console.log (pdiv)  //quit only for debugging
                                console.log (data)  //quit only for debugging

                                $.ajax(
                                    {
                                        "type": "POST",
                                        "dataType": "json",
                                        "url": "/ajax/rstsnap/",
                                        "data": data,
                                        "success": function(data) {
                                             $("#Snap_modal").modal('hide');
                                             $("#info_msg").text(data.msg);
                                             $("#md_msg").modal();
                                        },
                                        error: function(){
                                            alert("Error detected");
                                            location.reload();
                                        },
                                    }
                                );
                            }
                        )
                        $('input[id^="snap_delete"]').click(
                            function(e) {
                                e.preventDefault();
                                var pdiv = $(this).parent().attr('id');
                                var data = {
                                    vmid: $("#"+ pdiv + "> #vmid").val(),
                                    suuid: $("#"+ pdiv + "> #suuid").val(),
                                }
                                console.log (pdiv)  //quit only for debugging
                                console.log (data)  //quit only for debugging

                                $.ajax(
                                    {
                                        "type": "POST",
                                        "dataType": "json",
                                        "url": "/ajax/delsnap/",
                                        "data": data,
                                        "success": function(data) {
                                             $("#Snap_modal").modal('hide');
                                             $("#info_msg").text(data.msg);
                                             $("#md_msg").modal();
                                        },
                                        error: function(){
                                            alert("Error detected");
                                            location.reload();
                                        },
                                    }
                                );
                            }
                        )
                        $("#Snap_modal").modal();
                    },
                    error: function(){
                        alert("Error detected");
                    },
                }
            );
        });

    $('input[id^="mk_snap"]').click(function(e) {
            e.preventDefault();
            var pdiv = $(this).parent().attr('id');
            var data = {
                vmid: $("#"+ pdiv + "> #vmid").val(),
            }
            $.ajax(
                {
                    "type": "POST",
                    "dataType": "json",
                    "url": "/ajax/mksnap/",
                    "data": data,
                    "success": function(data) {
                         $("#info_msg").text(data.msg);
                         $("#md_msg").modal();
                    },
                    error: function(){
                        alert("Error detected");
                    },
                }
            );
        });


    //Console
    $('button[id^="btn_console"]').on('click',function (e) {
        e.preventDefault();

        var pdiv = $(this).parent().attr('id');
        var data = {
            vmid: $("#"+ pdiv + "> #vmid").val(),
        }
        $.ajax(
            {
                "type": "POST",
                "dataType": "json",
                "url": "/ajax/remote/",
                "data": data,
                "success": function(data) {

                    var remote = data.remote;

                    if (remote == "True"){
                        var name = data.name;
                        var cnx = data.cnx;
                        var athml = data.athml;
                        var url = data.url;
                        var client = window.btoa([name, cnx, athml].join('\0'));
                        console.log(client+url) //debug
                        var myWindow = window.open(url+client);

                    }
                    else {
                        $("#info_msg").text(data.msg);
                        $("#md_msg").modal();
                    }
                },
                error: function(){
                    alert("Error detected");
                },
            }
        );
    });


    //Referesh
    $("#btn_update").on('click',function (e) {
        e.preventDefault();

        var data = {
            type: "vmachine",
        }
        $.ajax(
            {
                "type": "POST",
                "dataType": "json",
                "url": "/ajax/updatedb/",
                "data": data,
                success: function(data) {
                    console.log(data.msg)
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

    $("#md_msg_form").on('hidden.bs.modal', function () {
        window.location.href="/vmachine";
    });

    $("#md_msg").on('hidden.bs.modal', function () {
        location.reload();
    });


    /*$("#id_name").keyup(function(){
        $("#id_dname").val(this.value);
    });*/

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


