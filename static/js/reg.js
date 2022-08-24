var regbtn = document.getElementById('reg')
var inputs = document.getElementsByClassName('mdui-textfield-input')
regbtn.onclick = function(){
    if (inputs[1].value != inputs[2].value){
        swal("错误","两次输入的密码不一致","error")
    }else{
        var data = {"userName": inputs[0].value,"passWord": inputs[1].value,"gameID": inputs[3].value,"nickName": inputs[4].value, "challenge": window.captchaData['challenge'], "validate": window.captchaData['validate'], "seccode": window.captchaData['seccode']}
        console.log('准备提交 -> ' + data)
        console.log(data)
        $.post("/api/user/reg",data,function(data){
            if (data['code'] == 0){
                ElementPlus.ElMessage.success("注册成功，正在跳转登录页")
                window.location = '/user/login'
            }else{
                ElementPlus.ElMessage.error(data['msg'])
                window.captchaObj.reset()
            }
        })
    }
}