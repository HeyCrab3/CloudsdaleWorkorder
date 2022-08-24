var qacontainer = document.getElementById('qacontainer')
$.get('/api/question/hot',function(data){
    if (data['code'] != 0){
        swal("错误","加载问题时出错！","error")
    }else{
        console.log("获取到的Q&A：" + data['result'])
        for (var i=0;i<data['result'].length;i++){
            var vnode = document.createElement('div')
            vnode.className = "el-collapse-item"
            vnode.innerHTML = '<div role="tab" aria-expanded="false" aria-controls="el-collapse-content-9656" aria-describedby="el-collapse-content-9656"><div id="el-collapse-head-9656" class="el-collapse-item__header" role="button" tabindex="0">' + data['result'][i]['Q'] + '<i class="el-icon el-collapse-item__arrow"><svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M340.864 149.312a30.592 30.592 0 0 0 0 42.752L652.736 512 340.864 831.872a30.592 30.592 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></div></div><div id="el-collapse-content-9656" class="el-collapse-item__wrap" role="tabpanel" aria-hidden="true" aria-labelledby="el-collapse-head-9656" style="display: none;" data-old-padding-top="" data-old-padding-bottom="" data-old-overflow=""><div class="el-collapse-item__content"><div>' + data['result'][i]['A'] + '</div><div></div></div></div>'
            qacontainer.appendChild(vnode)
        }
    }
})