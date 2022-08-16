var pwd = document.getElementById('pwd')
var confirmPwd = document.getElementById('confirmPwd')
var cpdbtn = document.getElementById('changePD')
var dataPrev = document.getElementsByClassName('dataPrev')
var changeNick = document.getElementById('changeN')
var nick = document.getElementById('nick')
window.onload = function(){
    $.get('/api/user/me', function(data){
        if (data['code'] != 0){
            dataPrev[0].innerHTML = "游戏ID " + data['msg']
            dataPrev[1].innerHTML = "昵称 " + data['msg']
            dataPrev[2].innerHTML = "权限 " + data['msg']
            dataPrev[3].innerHTML = data['msg']
        }else{
            dataPrev[0].innerHTML = "游戏ID " + data['userdata']['gameID']
            dataPrev[1].innerHTML = "昵称 " + data['userdata']['nickName']
            dataPrev[2].innerHTML = "权限 " + data['userdata']['perm']
            dataPrev[3].innerHTML = data['userdata']['_id']['$oid']
        }
    })
}
cpdbtn.onclick = function(){
    if (pwd.value != confirmPwd.value){
        var vnode = document.createElement('div')
        vnode.className = "alert alert-danger d-flex align-items-center"
        vnode.innerHTML = '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg><div>两次密码不一致</div>'
        document.getElementsByClassName('modal-body')[0].append(vnode)
    }else{
        var data = {'newPwd': pwd.value}
        $.post('/api/user/changepwd', data, function(data){
            if (data['code'] != 0)  {
                var vnode = document.createElement('div')
                vnode.className = "alert alert-danger d-flex align-items-center"
                vnode.innerHTML = '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg><div>' + data['msg'] + '</div>'
                document.getElementsByClassName('modal-body')[0].append(vnode)
            }else{
                var vnode = document.createElement('div')
                vnode.className = "alert alert-success d-flex align-items-center"
                vnode.innerHTML = '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg><div>' + data['msg'] + '</div>'
                document.getElementsByClassName('modal-body')[0].append(vnode)
            }
        })
    }
}
changeNick.onclick = function(){
    var data = {'newNick': nick.value}
    $.post('/api/user/changenick', data, function(data){
        if (data['code'] != 0)  {
            var vnode = document.createElement('div')
            vnode.className = "alert alert-danger d-flex align-items-center"
            vnode.innerHTML = '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg><div>' + data['msg'] + '</div>'
            document.getElementsByClassName('modal-body')[1].append(vnode)
        }else{
            var vnode = document.createElement('div')
            vnode.className = "alert alert-success d-flex align-items-center"
            vnode.innerHTML = '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg><div>' + data['msg'] + '</div>'
            document.getElementsByClassName('modal-body')[1].append(vnode)
        }
    })
}