var countNum = document.getElementsByClassName('countNum')
var ticketContainer = document.getElementById('container-ticket')
window.onload = function(){
    $.get('/api/ticket/overall',function(data){
        if (data['code'] != 0){
            ElementPlus.ElMessage.error(data['msg'])
            swal("错误！",data['msg'],"error")
        }else{
            countNum[0].innerHTML = data['platformTicketNum']
            countNum[1].innerHTML = data['userTicketNum']
            countNum[2].innerHTML = data['processingNum']
            countNum[3].innerHTML = data['closeNum']
            countNum[4].innerHTML = data['userPerm']
        }
    })
    $.get('/api/ticket/myticket',function(data){
        if (data['code'] != 0){
            ElementPlus.ElMessage.error(data['msg'])
            swal("错误！",data['msg'],"error")
        }else{
            for (var i=0;i<data['ticketList'].length;i++){
                var vnode = document.createElement('tr')
                if (data['ticketList'][i]['status'] == 0){
                    vnode.innerHTML = '<td>' + data['ticketList'][i]['_id']['$oid'] + '</td><td>' + data['ticketList'][i]['sender'] + '</td><td>' + data['ticketList'][i]['title'] + '</td><td><div class="el-badge item"><sup class="el-badge__content el-badge__content--primary">未处理</sup></div></td><td><a style="text-decoration:none" href="/ticket/view?id=' + data['ticketList'][i]['_id']['$oid'] + '" class="el-button">查看工单</a></td>'    
                }
                else if (data['ticketList'][i]['status'] == 1){
                    vnode.innerHTML = '<td>' + data['ticketList'][i]['_id']['$oid'] + '</td><td>' + data['ticketList'][i]['sender'] + '</td><td>' + data['ticketList'][i]['title'] + '</td><td><div class="el-badge item"><sup class="el-badge__content el-badge__content--success">处理中</sup></div></td><td><a style="text-decoration:none" href="/ticket/view?id=' + data['ticketList'][i]['_id']['$oid'] + '" class="el-button">查看工单</a></td>'    
                }
                else if (data['ticketList'][i]['status'] == 2){
                    vnode.innerHTML = '<td>' + data['ticketList'][i]['_id']['$oid'] + '</td><td>' + data['ticketList'][i]['sender'] + '</td><td>' + data['ticketList'][i]['title'] + '</td><td><div class="el-badge item"><sup class="el-badge__content el-badge__content--warning">需要更多信息</sup></div></td><td><a style="text-decoration:none" href="/ticket/view?id=' + data['ticketList'][i]['_id']['$oid'] + '" class="el-button">查看工单</a></td>'    
                }
                else{
                    vnode.innerHTML = '<td>' + data['ticketList'][i]['_id']['$oid'] + '</td><td>' + data['ticketList'][i]['sender'] + '</td><td>' + data['ticketList'][i]['title'] + '</td><td><div class="el-badge item"><sup class="el-badge__content el-badge__content--info">已关闭</sup></div></td><td><a style="text-decoration:none" href="/ticket/view?id=' + data['ticketList'][i]['_id']['$oid'] + '" class="el-button">查看工单</a></td>'
                }
                ticketContainer.appendChild(vnode)
            }
        }
    })
}