var container = document.getElementById('replycontainer');
var skeleton = document.getElementById('loading');
var sender = document.getElementById('sender');
var time = document.getElementById('time');
var sendbtn = document.getElementById('sendcontent');
var contentArea = document.getElementById('replys');
window.onload = function(){
$.get('/api/ticket/ticketdata?id=' + window.ticketID,function(data){
   if (data['code'] != 0){
       ElementPlus.ElMessage.error(data['msg']);
   }else{
       sender.innerHTML = data['data']['sender'];
       time.innerHTML = data['data']['time'];
       var vnode = document.createElement('li');
       vnode.className = "mdui-list-item mdui-ripple";
       vnode.innerHTML = '<div class="mdui-list-item-avatar"><img src="/static/img/useravatar.jpg"/></div><div class="mdui-list-item-content"><div class="mdui-list-item-title">' + data['data']['content'] + '</div><div class="mdui-list-item-text mdui-list-item-two-line"><span class="mdui-text-color-theme-text">' + data['data']['sender'] + '<div class="el-badge item"><sup class="el-badge__content el-badge__content--primary">原始工单内容</sup></div></span> ' + data['data']['time'] + '</div></div>';
       container.appendChild(vnode);
       if(data['data']['images'].length != 0){
               var vnode = document.createElement('li');
               vnode.className = "mdui-list-item mdui-ripple";
               vnode.innerHTML = '<div class="mdui-list-item-avatar"><img src="/static/img/useravatar.jpg"/></div><div class="mdui-list-item-content"><div class="mdui-list-item-title"><img src="' + data['data']['images'] + '"/></div><div class="mdui-list-item-text mdui-list-item-two-line"><span class="mdui-text-color-theme-text">' + data['data']['sender'] + '<div class="el-badge item"><sup class="el-badge__content el-badge__content--primary">原始工单图片</sup></div></span> ' + data['data']['time'] + '</div></div>'
               container.appendChild(vnode);
       }
   }
})
    $.get('/api/ticket/reply?id=' + window.ticketID,function(data){
        if (data['code'] != 0){
            ElementPlus.ElMessage.Error(data['msg']);
        }else{
            loading.remove()
            for (var i=0;i<data['reply'].length;i++){
                if (data['reply'][i]['isAdmin'] == true){
                    var vnode = document.createElement('li');
                    vnode.className = "mdui-list-item mdui-ripple";
                    vnode.innerHTML = '<div class="mdui-list-item-avatar"><img src="/static/img/serviceavatar.jpg"/></div><div class="mdui-list-item-content"><div class="mdui-list-item-title">' + data['reply'][i]['content'] + '</div><div class="mdui-list-item-text mdui-list-item-two-line"><span class="mdui-text-color-theme-text">' + data['reply'][i]['sender'] + '<div class="el-badge item"><sup class="el-badge__content el-badge__content--danger">管理组</sup></div></span> ' + data['reply'][i]['time'] + '</div></div>';
                    container.appendChild(vnode);
                }
                else{
                    var vnode = document.createElement('li');
                    vnode.className = "mdui-list-item mdui-ripple";
                    vnode.innerHTML = '<div class="mdui-list-item-avatar"><img src="/static/img/useravatar.jpg"/></div><div class="mdui-list-item-content"><div class="mdui-list-item-title">' + data['reply'][i]['content'] + '</div><div class="mdui-list-item-text mdui-list-item-two-line"><span class="mdui-text-color-theme-text">' + data['reply'][i]['sender'] + '</span> ' + data['reply'][i]['time'] + '</div></div>';
                    container.appendChild(vnode);
                }
            }
        }
    })


}
sendbtn.onclick = function(){
    var data = {'content': contentArea.value};
    $.post('/api/ticket/sendreply?id=' + window.ticketID, data, function(data){
        if (data['code'] != 0){
            ElementPlus.ElMessage.error(data['msg']);
        }else{
            ElementPlus.ElMessage.success(data['msg']);
            window.location.reload();
        }
    })
}