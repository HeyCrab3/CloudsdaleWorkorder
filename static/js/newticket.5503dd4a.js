window.onload = function(){
    ElementPlus.ElMessageBox.alert('请先阅读提问的智慧 https://lug.ustc.edu.cn/wiki/doc/smart-questions/ 再提问，没看直接提问题或者提出愚蠢的问题的工单不予受理，自行解决','提问前注意！',{confirmButtonText: '我看完了，不会提傻子问题'})
}
var submitbtn = document.getElementById('submit')
var inputs = document.getElementsByClassName('mdui-textfield-input')
var addimage = document.getElementById('add')
var imageContainer = document.getElementById('image')
var imageLinks = document.getElementsByClassName('image-link')
var imageList = []
submitbtn.onclick = function(){
    for (var i=0;i<imageLinks.length;i++){
            imageList.push(imageLinks[i].value)
            console.log(imageList)
    }
    var data = {'title':inputs[0].value,'content':inputs[1].value,'images':imageList}
    $('#submit').attr('loading','true')
    $('#submit').attr('disabled','true')
    console.log(data)
    var loadingservice = ElementPlus.ElLoading.service({lock: true,text: '正在提交工单'})
    $.post('/api/ticket/new',data,function(data){
        if (data['code'] != 0){
            loadingservice.close()
            ElementPlus.ElMessage.error(data['msg'] + ' (' + data['code'] + ')')
            $('#submit').removeAttr('disabled')
        }else{
            loadingservice.close()
            ElementPlus.ElMessage.success(data['msg'])
            $('#submit').removeAttr('disabled')
            window.location = '/ticket/overview'
        }
    })
}

addimage.onclick = function(){
    var vnode = document.createElement('div')
    vnode.className = 'mdui-textfield mdui-textfield-floating-label'
    vnode.innerHTML = '<label class="mdui-textfield-label">图片（Beta，仅限图片链接，一行一个）</label><input class="mdui-textfield-input image-link" type="text"/>'
    imageContainer.appendChild(vnode)
    ElementPlus.ElMessage.success('成功')
}