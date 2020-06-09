from cmfz_permission.models import Permission


def init_permission(admin, request):
    """获取当前登录用户的权限列表"""

    permission_url = admin.roles.filter(permissions__isnull=False).values("permissions__url", "permissions__is_menu",
                                                                          "permissions__title").distinct()

    # 权限url列表
    permission_list = [i['permissions__url'] for i in permission_url]

    # 菜单列表
    menu_list = [[], [], [], [], []]
    for i in permission_url:
        if i['permissions__is_menu']:
            if '/user/' in i['permissions__url']:
                menu_list[0].append({'title': i['permissions__title'], 'url': i['permissions__url']})
            elif '/article/' in i['permissions__url']:
                menu_list[1].append({'title': i['permissions__title'], 'url': i['permissions__url']})
            elif '/album/' in i['permissions__url']:
                menu_list[2].append({'title': i['permissions__title'], 'url': i['permissions__url']})
            elif '/carousel/' in i['permissions__url']:
                menu_list[3].append({'title': i['permissions__title'], 'url': i['permissions__url']})
            elif '/admin/' in i['permissions__url']:
                menu_list[4].append({'title': i['permissions__title'], 'url': i['permissions__url']})

    print('验证',permission_list)
    print('验证',menu_list)
    request.session['permission_list'] = permission_list
    request.session['menu_list'] = menu_list


