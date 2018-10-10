$(function () {
    var user_error = false;
    var password_error = false;

    $('.name_input').blur(function () {
        // $(this) 表示获取当前操作的input标签
        if($(this).val() == ""){
            $('.user_error').html("输入用户名").show();
            user_error = true;
        }else{
            // 已经输入隐藏错误信息
            $('.user_error').hide();
            user_error = false;
        }
    });

    $('.pass_input').blur(function () {
        // $(this) 表示获取当前操作的input标签
        if($(this).val() == ""){
            $('.pwd_error').html("请输入密码").show();
            password_error = true;
        }else{
            // 已经输入隐藏错误信息
            $('.pwd_error').hide();
            password_error = false
        }
    });

    $('form').submit(function () {
        name = $('.name_input').val().length;
        password = $('.pass_input').val();
        if(name==0){
            user_error = true;
        }
        if(password==""){
            password_error = true;
        }

        if(user_error == false && password_error == false){
            // 只有用户和密码输入框同时输入的时候才不阻止提交
            return true;
        }else{
            return false;
        }
    });

});