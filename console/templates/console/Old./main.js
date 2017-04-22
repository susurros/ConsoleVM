$(document).ready(
    function() {


        // AJAX ControlVM

        /*
            http://coreymaynard.com/blog/performing-ajax-post-requests-in-django/
            http://www.w3schools.com/jquery/jquery_ref_selectors.asp
            http://www.w3schools.com/jquery/tryit.asp?filename=tryjquery_dom_attr_get
            http://www.w3schools.com/js/js_regexp.asp
            http://pythoniza.me/ajax-en-django-con-jquery/
            http://entredesarrolladores.com/6979/actualizar-contenido-con-ajax-en-django
            http://twigstechtips.blogspot.de/2009/09/django-how-to-perform-ajax-post-request.html
            https://realpython.com/blog/python/django-and-ajax-form-submissions/
            http://stackoverflow.com/questions/1208067/wheres-my-json-data-in-my-incoming-django-request
            https://godjango.com/18-basic-ajax/
            Modal Windows:https://dmorgan.info/posts/django-views-bootstrap-modals/
        */




        
        $('input[id^="delete_vm"]').click(
            function(e) {
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
                            alert (data.message);
                            location.reload()


                        },
                        error: function(){
                            alert("Error detected");
                        },
                    }
                );
            }
        );
        
        $('input[id^="modify_vm"]').click(
            function(e) {
                e.preventDefault();
                var pdiv = $(this).parent().attr('id');
                var data = {
                    vmid: $("#"+ pdiv + "> #vmid").val(),
                    step: "1",
                }
                $.ajax(
                    {
                        "type": "POST",
                        "dataType": "json",
                        "url": "/ajax/modifyvm/",
                        "data": data,
                        "success": function(data) {
                            
                            if (data.action == "modal"){
                                console.log(data.name) //quit only for debugging
                                $("#Mod_name").val(data.name)
                                $("#Mod_vmid").val(data.id)
                                $("#Mod_rdport").val(data.rdport)
                                $("#Mod_cpu").val(data.ncpu)
                                $("#Mod_mem").val(data.mem)
                                $("#VMmodify_modal").modal()
                            }else if (data.action == "PWOFF"){
                                alert(data.message)
                                
                            }else if (data.action == "NOEXIST"){
                                alert(data.message)
                            }
                        },
                        error: function() {
                            alert("Error detected");
                        } ,   
                    }
                 );
            }
        );
        
        $("#modify_form").click(
            function (e) {
                e.preventDefault();
                data = {
                    'name': $("#Mod_name").val(),
                    'vmid' : $("#Mod_vmid").val(),
                    'rdport': $("#Mod_rdport").val(),
                    'cpu': $("#Mod_cpu").val(),
                    'mem': $("#Mod_mem").val(),
                    'step': "2"
                }
                $.ajax(
                    {
                        "type": "POST",
                        "dataType": "json",
                        "url": "/ajax/modifyvm/",
                        "data": data,
                        "success": function (data) {
                            alert(data.message);
                            location.reload()
                            $("#VMmodify_modal").modal();
                        },
                        error: function () {
                            alert("Error detected");
                        }
                    }
                );
            }
        );
        // VBOX Create VM Forms Funcions

         $("#cont_form").click(
             function(e) {
                 e.preventDefault();
                 
                 if ($("#form_step").val() == '1'){
                     

                     if ($("#vm_vhost_vendor").val() == 'VB'){

                         if ($("#iface_type").val() =="intnet"){

                         var iface_data ={
                             type: $("#iface_type").val(),
                             driver: $("#iface_driver").val(),
                             intnet: $("#intnet").val()
                         }

                         }else if ($("#iface_type").val() =="bridged"){

                             var iface_data ={
                                 type: $("#iface_type").val(),
                                 driver: $("#iface_driver").val(),
                                 phy: $("#phy").val(),
                             }

                         }else{

                             var iface_data ={
                                 type: $("#iface_type").val(),
                                 driver: $("#iface_driver").val(),
                             }
                         }

                         var data = {
                             step: $("#form_step").val(),
                             name: $("#vm_name").val(),
                             cpu: $("#vm_cpu").val(),
                             mem: $("#vm_mem").val(),
                             os: $("#vm_ostype").val(),
                             dstore: $("#vm_datastore").val(),
                             dsksz: $("#vm_dsk_sz").val(),
                             ifaces: JSON.stringify(iface_data),
                             rdpuser: $("#rdp_user").val(),
                             rdppass : $("#rdp_pass").val(),
                             rdpport: $("#rdp_port").val(),
                             meddpath: $("#med_dpath").val(),

                         }

                     }

                     else if ($("#vm_vhost_vendor").val() == 'VW'){

                         var iface_data = {
                             type: $("#iface_type").val(),
                             driver: $("#iface_driver").val(),
                         }

                         var data = {
                             step: $("#form_step").val(),
                             name: $("#vm_name").val(),
                             cpu: $("#vm_cpu").val(),
                             mem: $("#vm_mem").val(),
                             os: $("#vm_ostype").val(),
                             dstore: $("#vm_datastore").val(),
                             dsksz: $("#vm_dsk_sz").val(),
                             ifaces: JSON.stringify(iface_data),
                             rdppass : $("#rdp_pass").val(),
                             rdpport: $("#rdp_port").val(),
                             meddpath: $("#med_dpath").val(),

                         }
                     }

                     else if ($("#vm_vhost_vendor").val() == 'ZN'){

                         var data = {
                             step: $("#form_step").val(),
                             name: $("#vm_name").val(),
                             cpu: $("#vm_cpu").val(),
                             mem: $("#vm_mem").val(),
                             os: $("#vm_ostype").val(),
                             dstore: $("#vm_datastore").val(),
                             dsksz: $("#vm_dsk_sz").val(),
                             ifaces:  $("#iface_type").val(),
                             rdpuser: $("#rdp_user").val(),
                             rdppass : $("#rdp_pass").val(),
                             rdpport: $("#rdp_port").val(),

                         }
                     }

                     console.log(data)

                     $.ajax(
                         {
                             "type": "POST",
                             "dataType": "json",
                             "url": "/ajax/form_vm/",
                             "data": data,
                             "success": function(data) {
                                 window.location.href = data.URI;
                             },
                             error: function(){
                                 alert(data.message);  
                             },
                         }
                     );
                     
                 }
                 
                 else if ($("#form_step").val() == '2'){
                     
                     
                     var data ={
                         step: $("#form_step").val(),
                         confirm : "ok",
                     }
                     
                     
                     $.ajax(
                         {
                             "type": "POST",
                             "dataType": "json",
                             "url": "/ajax/form_vm/",
                             "data": data,
                             "success": function(data) {
                                 alert (data,message)
                                 window.location.href = data.URI;
                             },
                             error: function(){
                                 alert("Error detected");
                             },
                         }
                     );
                     
                     
                 }else {
                     var data = {
                         vhid: $("#vhost_select").val(),
                     }

                     $.ajax(
                         {
                             "type": "POST",
                             "dataType": "json",
                             "url": "/ajax/form_vm/",
                             "data": data,
                             "success": function(data) {
                                 window.location.href = data.URI;
                             },
                             error: function(){
                                 alert("Error detected");
                             },
                         }
                     );
                 };

             }
         )


        // Control Display hiden forms

        $('#iface_type').change(function(){
            if ($(this).val() == "intnet"){
                $("#phy_form").hide();
                $('#intnet_form').show();
            }else if ($(this).val() == "bridged"){

                $("#intnet_form").hide();
                $("#phy_form").show();

            }else{
                $("#intnet_form").hide();
                $("#phy_form").hide();
            }

        });





        // Add Internal Network
        
    
        // When the user clicks on the button, open the modal
        $('#intnet').change (function () {
            if ($(this).val() == "new_int") {
                console.log("Inside Modal")
                $("#intnet_set").modal();
            }
        });
        
        $("#add_net_modal").click (function() {
            $("#intnet").append($('<option>', {
                value:  $("#new_net").val(),
                text: $("#new_net").val(),
            }));
            $("#intnet_set").modal("hide");
            
        });
        
        // When the user clicks on <span> (x), close the modal
        $(".close").click(function() {
            $("#intnet_set").modal("hide");
        });
        
        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
            if (event.target == $("#intnet_set")) {
                $("#intnet_set").modal("hide");
            }
        }

        
        $("#reset_form").click(
            function(e) {
                console.log("Function First Step");  //Quit Only for Debugging
                e.preventDefault();

                var data = {
                        step: $("#form_step").val(),
                        action: "close",
                    }


                console.log(data);  //Quit Only for Debugging
                $.ajax(
                    {
                        "type": "POST",
                        "dataType": "json",
                        "url": "/ajax/form_vm/",
                        "data": data,
                        "success": function(data) {
                            window.location.href = data.URI;
                        },
                        error: function(){
                            alert("Error detected");
                            console.log(data);  //Quit Only for Debugging
                        },
                    }
                );
            }
        );


        $("#back_form").click(
            function(e) {
                console.log("Function First Step");  //Quit Only for Debugging
                e.preventDefault();

                var data = {
                        step: $("#form_step").val(),
                        action: "back",
                    }


                console.log(data);  //Quit Only for Debugging
                $.ajax(
                    {
                        "type": "POST",
                        "dataType": "json",
                        "url": "/ajax/form_vm/",
                        "data": data,
                        "success": function(data) {

                            console.log("Calling ajax func");  //Quit Only for Debugging
                            window.location.href = data.URI;
                        },
                        error: function(){
                            alert("Error detected");
                            console.log(data);  //Quit Only for Debugging
                        },
                    }
                );
            }
        );


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




    }
);


































