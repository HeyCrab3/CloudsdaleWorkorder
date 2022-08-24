const login = document.getElementById('login')
const inputs = document.getElementsByClassName('mdui-textfield-input')

login.onclick = function(){
    var data = {"userName": inputs[0].value, "passWord": inputs[1].value, "challenge": window.captchaData['challenge'], "validate": window.captchaData['validate'], "seccode": window.captchaData['seccode']}
    console.log('准备提交 -> ' + data)
    console.log(data)
    $.post("/api/user/login",data,function(data){
        if (data['code'] == 0){
            ElementPlus.ElMessage.success(data['msg'])
            window.location = '/'
        }else{
            ElementPlus.ElMessage.error(data['msg'])
            window.captchaObj.reset();
        }
    })
}