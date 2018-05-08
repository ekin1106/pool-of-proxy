from proxy import *
proxy_go = proxy('test','ip_pool')
# proxy_go.clear()
# proxy_go.get_ip_port('https://www.kuaidaili.com/free/inha/1/')
# time.sleep(5)
# proxy_go.get_ip_port('https://www.kuaidaili.com/free/intr/1/')
# list = proxy_go.pop_ip()
# proxy_go.check_ip(list)
# proxy_go.reset()
print('''
*********************代理池*********************
*               请选择代理范围                 *
*               1.国内高匿代理                 *
*               2.国内普通代理                 *
*               3.检测代理池                   *
*               4.可用代理数量                 *
*               5.重置代理池                   *
*               6.清空代理池                   *
************************************************''')
choice = int(input('请选择:'))
if choice == 1:
    print('国内高匿采集中...')
    proxy_go.get_ip_port('https://www.kuaidaili.com/free/inha/1/')
elif choice == 2:
    print('国内高匿采集中...')
    proxy_go.get_ip_port('https://www.kuaidaili.com/free/intr/1/')
elif choice == 3:
    print('检测中...')
    list = proxy_go.pop_ip()
    proxy_go.check_ip(list)
    print('检测完成')
elif choice == 4:
    print('可用:%s'%proxy_go.ok_count()[0]+'\n'+'无法连接:%s'%proxy_go.ok_count()[1])
elif choice == 5:
    proxy_go.reset()
    print('重置完成，可以检测')

elif choice == 6:
    proxy_go.clear()
    print('清空完成')
elif choice == 7:
    proxy_go.get_xs_proxy('http://www.xsdaili.com/')
