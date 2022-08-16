var getDataBtn = document.getElementById('getData')
var refreshBtn = document.getElementById('refresh')
var container = document.getElementsByTagName('tbody')
var readdbbtn = document.getElementById('readdb')
var dbname = document.getElementById('dbname')
var ticketId = document.getElementById('ticketId')
var reply = document.getElementById('reply')
var sendreplybtn = document.getElementById('sendreply')

getDataBtn.onclick = function(){
    $.get('/api/admin/userData',function(data){
        if(data['code'] != 0){
            ElementPlus.ElMessage.error(data['msg'])
        }else{
            ElementPlus.ElMessage.success(data['msg'])
            for (var i=0;i<data['userdata'].length;i++){
                var vnode = document.createElement('tr')
                vnode.innerHTML = "<td>" + data['userdata'][i]['_id']['$oid'] + "</td><td>" + data['userdata'][i]['userName'] + "</td><td>" + data['userdata'][i]['nickName'] + "</td><td>" + data['userdata'][i]['gameID'] + "</td><td>" + data['userdata'][i]['perm'] + "</td>"
                container[0].appendChild(vnode)
            }
            $('#getData').attr('disabled','true')
            $('#getData').attr('aria-disabled','true')
            $('#getData').attr('class','el-button el-button--primary is-disabled')
        }
    })
}

readdbbtn.onclick = function(){
    $.get('/api/admin/readdb?db=' + dbname.value, function(data){
        if (data['code'] != 0){
            ElementPlus.ElMessage.error(data['msg'])
        }else{
            ElementPlus.ElMessage.success(data['msg'])
            /**require.config({ paths: { 'vs': '../static/js/monaco' }});
            require.config({'vs/nls': {availableLanguages: {'*':'zh-cn'}}});
            require(['vs/editor/editor.main'],function(){     
                monaco.editor.create(document.getElementById('monaco'), {
                    value: data['result'], 
                    language: 'javascript',
                    theme:'vs'
                });
            });**/
        }
    })
}

sendreplybtn.onclick = function(){
    var data = {'ticketID': ticketId.value, 'reply': reply.value}
    $.post('/api/admin/ticket/reply', data, function(data){
        if (data['code'] != 0){
            ElementPlus.ElMessage.error(data['msg'])
        }
        else{
            ElementPlus.ElMessage.success(data['msg'])
        }
    })
}