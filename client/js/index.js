window.typedict = {}
var create_menu = function (arr, pid = 0) {
    for (var a = 0; a < arr.length; a++) {
        if (arr[a].children) {
            if (arr[a].children.length) {
                html = `<li class="nav-item" data-toggle="tooltip" data-placement="right"><a class="nav-link nav-link-collapse collapsed" data-toggle="collapse" href="#m${arr[a].id}" data-pid="#exampleAccordion"><i class="glyphicon glyphicon-align-center"></i><span class="nav-link-text">${arr[a].name}</span></a><ul class="sidenav-second-level collapse" id="m${arr[a].id}"></ul>`
                $(`#m${pid}`).append(html)
                if (arr[a].children) {
                    create_menu(arr[a].children, arr[a].id)
                }
            }
            //一级根节点
            else {
                html = `<li class="nav-item" data-toggle="tooltip" data-placement="right" title="Tables"> <a class="nav-link" href="#"  onclick="click_menu(${arr[a].id})"><i class="glyphicon glyphicon-indent-right"></i><span class="nav-link-text">${arr[a].name}</span></a></li>`
                $(`#m${pid}`).append(html)
                if (arr[a].children) {
                    create_menu(arr[a].children, arr[a].id)
                }
            }
        } else {
            //二级根节点
            html = `<li><a href="#" onclick="click_menu(${arr[a].id})"> ${arr[a].name}</a></li>`
            $(`#m${pid}`).append(html)
        }
    }
}
var show_menu = function () {
    $.ajax({
        url: PATHURL + '/v1/base_dict/jurisdiction?type=1',
        type: 'get',
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        async: false,
        success: function (req) {
            if (req.code == 200)
                create_menu(listtoTree(req.data))
            else {
                alert('请求权限异常')
            }
        }
    })
}

var click_menu = function (pid) {
    var arr = typedict[pid]
    var temp = []
    if (!arr) {
        return
    }
    for (var a = 0; a < arr.length; a++) {
        if (temp.length == 0) {
            temp.push(`<li role="presentation" class="active">`)
        } else {
            temp.push(`<li role="presentation">`)
        }
        temp.push(`
                <a href="#test" onclick="click_pages(${arr[a].id},'${arr[a].link}')" aria-controls="home" role="tab" data-toggle="tab">
                    ${arr[a].name}
                </a>
            </li>
        `)
    }
    $('#page_nav').html(temp.join(''))
    let url = ""
    if (typedict[pid][0].link.indexOf('?') == -1) {
        url = 'pages/' + typedict[pid][0].link
    } else {
        url = 'pages/' + typedict[pid][0].link + typedict[pid][0].id
    }
    $('.content ').attr('src', url)
}
var listtoTree = function (arr) {
    var parent = []
    var children = {}
    for (var a = 0; a < arr.length; a++) {
        if (arr[a].type == '分页') {
            if (!typedict[arr[a].pid]) {
                typedict[arr[a].pid] = []
            }
            typedict[arr[a].pid].push(arr[a])
            continue
        }
        if (arr[a].pid == 0) {
            parent.push(arr[a])
        } else {
            if (!children[arr[a].pid]) {
                children[arr[a].pid] = []
            }
            children[arr[a].pid].push(arr[a])
        }

    }
    for (var a = 0; a < parent.length; a++) {
        if (children[parent[a].id]) {
            parent[a].children = children[parent[a].id]
        } else {
            parent[a].children = []
        }
    }
    return parent
}


$(function () {
    $('.content').css('height', $('.content-wrapper').height() - 59 + 'px')
    show_menu()
    click_menu(7)

});

var click_pages = function (pid, link) {
    var url = ""
    if (link.indexOf('?') != -1) {
        url = 'pages/' + link + pid
    } else {
        url = 'pages/' + link
    }
    $('.content ').attr('src', url)
}