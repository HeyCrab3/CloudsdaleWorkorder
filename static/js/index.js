var qacontainer = document.getElementById('qacontainer')
$.get('/api/question/hot',function(data){
    if (data['code'] != 0){
        swal("错误","加载问题时出错！","error")
    }else{
        console.log("获取到的Q&A：" + data['result'])
        for (var i=0;i<data['result'].length;i++){
            var vnode = document.createElement('div')
            vnode.className = "mdui-panel-item"
            vnode.innerHTML = '<div class="mdui-panel-item-header"><div class="mdui-panel-item-title">Q:' + data['result'][i]['Q'] + '</div><i class="mdui-panel-item-arrow mdui-icon material-icons">keyboard_arrow_down</i></div><div class="mdui-panel-item-body"><p>A:' + data['result'][i]['A'] + '</p></div>'
            qacontainer.appendChild(vnode)
        }
    }
})