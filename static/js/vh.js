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

        $('input[id^="shut_vm"]').click(
            function(e) {
                e.preventDefault();
                var pdiv = $(this).parent().attr('id');
                var data = {
                    vhid: $("#"+ pdiv + "> #vhid").val(),
                    command: "shutdown"
                }
                console.log(data)
                $.ajax(
                    {
                        "type": "POST",
                        "dataType": "json",
                        "url": "/ajax/control_vm/",
                        "data": data,
                        "success": function(data) {
                            alert (data.message);
                            window.location.href = data.URI
                        },
                        error: function(){
                            alert("Error detected");
                        },
                    }
                );
            }
        )

        $('input[id^="modify_vh"]').click(
            function(e) {
                e.preventDefault();
                var pdiv = $(this).parent().attr('id');
                var data = {
                    vhostid: $("#"+ pdiv + "> #vhid").val(),
                }
                console.log(data)
                $.ajax(
                    {
                        "type": "POST",
                        "dataType": "json",
                        "url": "/ajax/vhost_update_query/",
                        "data": data,
                        "success": function(data) {
                            console.log(data);
                            $("#id_vhost").attr('value', data.id);
                            $("#id_name").attr('value', data.name);
                            $("#id_VType").attr('value', data.VType);
                            $("#id_ip").attr('value', data.ipaddr);
                            $("#id_isopath").attr('value', data.isopath);
                            $("#id_user").attr('value', data.user);
                            $("#id_sshkey").attr('value', data.sshkey);
                            $("#id_sshport").attr('value', data.sshport);
                            $("#md_vhots_form").modal();
                        },
                        error: function(){
                            alert("Error detected");
                        },
                    }
                );
            }
        )

        $("#btn_mod_vhost").click(function(e){
            e.preventDefault();
            var data ={
                vhostid:$("#id_vhost").val(),
                name: $("#id_name").val(),
                ipaddr: $("#id_ip").val(),
                isopath: $("#id_isopath").val(),
                user: $("#id_user").val(),
                sshkey: $("#id_sshkey").val(),
                sshport: $("#id_sshport").val(),
            }

            $.ajax({
                     "type": "POST",
                     "dataType": "json",
                     "url": "/vhost/new/",
                     "data": data,
                     "success": function(data) {

                      //   console.log("añadiendo menssake")
                        $("#info_msg").text(data.msg);
                        $("#md_vhots_form").modal('hide');
                      //  console.log ("modal cerrdandose");
                        //$("#md_msg").modal('show');

                     },
                     error: function(){
                            alert("Error detected");
                     },
                 });


        });

        $('input[id^="delete_vh"]').click(function(e){
            e.preventDefault();


            var pdiv = $(this).parent().attr('id');
            var vh_name = $("#"+ pdiv + "> #vhname").val();
            var vh_id = $("#"+ pdiv + "> #vhid").val();
            $("#delete_msg").text("The Virtual Host " + vh_name +  " is going to be deleted from the DB. Please confirm action");
            $("#del_vh").attr("value",vh_id);
            $("#md_delete_vhost").modal();

        });


        $('#btn_delete_vhost_ok').click(function(e) {
                e.preventDefault();
                var data = {
                    vhostid: $("#del_vh").val(),
                }
                $.ajax(
                    {
                        "type": "POST",
                        "dataType": "json",
                        "url": "/ajax/deletevh/",
                        "data": data,
                        "success": function(data) {
                            $("#info_msg").text(data.msg);
                            $("#md_delete_vhost").modal('hide');
                        },
                        error: function(){
                            alert("Error detected");
                        },
                    }
                );
        });

        $("#md_vhots_form").on('hidden.bs.modal', function () {
            $("#md_msg").modal();
        });

        $("#md_delete_vhost").on('hidden.bs.modal', function () {
            $("#md_msg").modal();
        });


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




    }
);