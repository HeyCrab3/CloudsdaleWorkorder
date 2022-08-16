var loginbtn = document.getElementById('login')
var inputs = document.getElementsByClassName('mdui-textfield-input')
loginbtn.onclick = function(){
    var data = {"userName": inputs[0].value,"passWord": inputs[1].value,"captcha":inputs[2].value}
    console.log('准备提交 -> ' + data)
    console.log(data)
    $.post("/api/user/login",data,function(data){
        if (data['code'] == 0){
            swal("登陆成功",data['msg'],"success").then(() => {window.location = '/'});
        }else{
            swal("错误",data['msg'],"error")
        }
    })
}