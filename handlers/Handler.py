# coding:utf-8

import pymysql
import logging

from handlers.BaseHandler import BaseHandler


class TjHandler(BaseHandler):
    '''获取各种文件数量和数据大小'''
    def post(self):
        database = self.get_argument("database")
        table = self.get_argument("table")
        time_start = self.get_argument("time_start")
        time_end = self.get_argument("time_end")
        try:
            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   passwd='123456',
                                   db='nbufiles',
                                   port=3306,
                                   charset='utf8')
            cur = conn.cursor()  # 获取一个游标
            if len(time_end) == 0 and len(time_start) == 0:
                time_start = "--"
                time_end = "--"
                sql = "select @files_total := count(*) from %s"%(table,)
                cur.execute(sql)
                files_number = cur.fetchone()[0]  #文件总数
                sql = "select @files_size := sum(size)/1024/1024/1024 from %s"%(table,)
                cur.execute(sql)
                files_size = cur.fetchone()[0]  #文件总数据量
                if files_number == 0:
                    files_size = 0
                sql = "select @duplic_total := count(*) from %s"%(table+"_duplic",)
                cur.execute(sql)
                duplicname_number = cur.fetchone()[0]  #同名文件数
                sql = "select @duplic_size := sum(size)/1024/1024/1024 from %s"%(table+"_duplic",)
                cur.execute(sql)
                duplicname_size = cur.fetchone()[0]  #同名文件数据量
                if duplicname_number == 0:
                    duplicname_size = 0
                sql = "select @duplic_uniqe_total := count(*) from %s where filename in (select filename from %s group by attr,fuser,fgroup,size,date,filename having count(*)=1)"%(table+"_duplic", table+"_duplic")
                cur.execute(sql)
                duplicname_uniqe_number = cur.fetchone()[0]  #同名但属性不同文件数
                sql = "select @duplic_uniqe_size := sum(size)/1024/1024/1024 from %s where filename in (select filename from %s group by attr,fuser,fgroup,size,date,filename having count(*)=1)"%(table+"_duplic", table+"_duplic")
                cur.execute(sql)
                duplicname_uniqe_size = cur.fetchone()[0]  #同名但属性不同文件数据量
                if duplicname_uniqe_number == 0:
                    duplicname_uniqe_size = 0
                uniqe_number = files_number-(duplicname_number-duplicname_uniqe_number)  #不重复文件数
                uniqe_size = files_size-(duplicname_size-duplicname_uniqe_size)  #不重复文件数据量
            elif len(time_end) > 0 and len(time_start) > 0:
                sql_time = """str_to_date(date, '%b%d%Y') between str_to_date("{}", '%Y-%m-%d') AND str_to_date("{}", '%Y-%m-%d')""".format(str(time_start), str(time_end))
                sql = "select @files_total := count(*) from %s where %s"%(table, sql_time)
                cur.execute(sql)
                files_number = cur.fetchone()[0]  # 文件总数
                sql = "select @files_size := sum(size)/1024/1024/1024 from %s where %s"%(table, sql_time)
                cur.execute(sql)
                files_size = cur.fetchone()[0]  # 文件总数据量
                if files_number == 0:
                    files_size = 0
                sql = "select @duplic_total := count(*) from %s where %s"%(table + "_duplic", sql_time)
                cur.execute(sql)
                duplicname_number = cur.fetchone()[0]  # 同名文件数
                sql = "select @duplic_size := sum(size)/1024/1024/1024 from %s where %s"%(
                table + "_duplic", sql_time)
                cur.execute(sql)
                duplicname_size = cur.fetchone()[0]  # 同名文件数据量
                if duplicname_number == 0:
                    duplicname_size = 0
                sql = "select @duplic_uniqe_total := count(*) from %s where (filename in (select filename from %s group by attr,fuser,fgroup,size,date,filename having count(*)=1)) and (%s)"%(
                table+"_duplic", table+"_duplic", sql_time)
                cur.execute(sql)
                duplicname_uniqe_number = cur.fetchone()[0]  # 同名但属性不同文件数
                sql = "select @duplic_uniqe_size := sum(size)/1024/1024/1024 from %s where (filename in (select filename from %s group by attr,fuser,fgroup,size,date,filename having count(*)=1)) and (%s)"%(
                table+"_duplic", table+"_duplic", sql_time)
                cur.execute(sql)
                duplicname_uniqe_size = cur.fetchone()[0]  # 同名但属性不同文件数据量
                if duplicname_uniqe_number == 0:
                    duplicname_uniqe_size = 0
                uniqe_number = files_number-(duplicname_number-duplicname_uniqe_number)  #不重复文件数
                uniqe_size = files_size-(duplicname_size-duplicname_uniqe_size)  #不重复文件数据量
            cur.close()
            conn.close()
        except Exception as e:
            logging.error(e)
            return self.write('查询出错！')
        data={
            "database": database,
            "table": table,
            "time_start": time_start,
            "time_end": time_end,
            "files_number": files_number,
            "files_size": files_size,
            "uniqe_number": uniqe_number,
            "uniqe_size": uniqe_size,
            "duplicname_number": duplicname_number,
            "duplicname_size": duplicname_size,
            "duplicname_uniqe_number": duplicname_uniqe_number,
            "duplicname_uniqe_size": duplicname_uniqe_size
        }
        self.render("2.html", **data)

class SsHandler(BaseHandler):

    def get(self, tiaojian, page):
        if tiaojian == 'inbody':
            table = self.get_argument('table')
            filename = self.get_argument('filename')
            tiaojian = table+'+'+filename
        else:
            table, filename = tiaojian.split('+')
        try:
            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   passwd='123456',
                                   db='nbufiles',
                                   port=3306,
                                   charset='utf8')
            cur = conn.cursor()  # 获取一个游标
            sql = "select count(*) from {} where filename like '%{}%'".format(table, filename)
            cur.execute(sql)
            number = cur.fetchone()[0]
            page_obj = Pagination(page, number)
            sql = "select * from {} where filename like '%{}%' limit {}, {}".format(table, filename, page_obj.start, page_obj.end - page_obj.start)
            cur.execute(sql)
            list = cur.fetchall()
            cur.close()
            conn.close()

        except Exception as e:
            logging.error(e)
            return self.write('查询出错！')
        # 当前页显示的数据
        current_list = list
        # 当前页显示的页码数相关html代码
        url = '/api/ss/%s/' % (tiaojian,)
        str_page = page_obj.page_num_show(url)
        self.render('4.html',
                    table=table,
                    filename=filename,
                    list_info=current_list,
                    current_page=page_obj.current_page,
                    str_page=str_page)


class Pagination:
    """
    分页
    """
    def __init__(self, current_page='1', page_item=1):
        all_page, c = divmod(page_item, 5)
        if c > 0:
            all_page += 1
        try:
            current_page = int(current_page)
        except:
            current_page = 1
        if current_page < 1:
            current_page = 1

        self.current_page = current_page  # 当前页
        self.all_page = all_page  # 总页数

    @property
    def start(self):
        """
        显示数据的起点索引
        """
        return (self.current_page - 1) * 5

    @property
    def end(self):
        """
        显示数据的末尾索引
        """
        return self.current_page * 5

    def page_num_show(self, baseurl):
        """
        写入{% raw str_page %}模板中的内容
        :return: 返回一段字符串形式的html代码块，包括首页，页码数，上一页等等内容
        """
        # 计算9个页码的起始索引
        list_page = []
        if self.current_page <= 4:
            s = 0
            e = min(self.all_page, 9)
        elif self.current_page > self.all_page - 4:
            s = max(0, self.all_page - 9)
            e = self.all_page
        else:
            s = self.current_page - 5
            e = self.current_page + 4
        # 首页
        first_page = '<a href="%s1">首页</a>' % (baseurl)
        list_page.append(first_page)

        # 上一页current_page-1
        if self.current_page <= 1:
            prev_page = '<a href="javascript:void(0);">上一页</a>'
        else:
            prev_page = '<a href="%s%s">上一页</a>' % (baseurl, self.current_page - 1)
        list_page.append(prev_page)

        # 9个页码数
        for p in range(s, e):
            if p + 1 == self.current_page:
                temp = '<a href="%s%s" class="active">%s</a>' % (baseurl, p + 1, p + 1)
                list_page.append(temp)
            else:
                temp = '<a href="%s%s">%s</a>' % (baseurl, p + 1, p + 1)
                list_page.append(temp)

        # 下一页next_page+1
        if self.current_page >= self.all_page:
            next_page = '<a href="javascript:void(0);">下一页</a>'
        else:
            next_page = '<a href="%s%s">下一页</a>' % (baseurl, self.current_page + 1)
        list_page.append(next_page)

        # 尾页
        last_page = '<a href="%s%s">尾页</a>' % (baseurl, self.all_page)
        list_page.append(last_page)

        # 页面跳转
        jump = """<input type="text"/><a onclick="Jump('%s',this);">go</a>""" % (baseurl,)
        script = """<script>
            function Jump(url,self){
                var v=self.previousElementSibling.value;
                if (v.trim().length>0){
                    location.href=url+v;
                }
        }
        </script>"""
        list_page.append(jump)
        list_page.append(script)

        str_page = "".join(list_page)
        return str_page

class ListHandler(BaseHandler):
    '''获取具体文件'''
    def get(self, tiaojian, page):
        try:
            select_type, database, table, number, time_start, time_end = tiaojian.split("+")
        except Exception as e:
            logging.error(e)
            return self.write('传入参数错误！')
        number = int(number)
        page_obj = Pagination(page, number)
        try:
            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   passwd='123456',
                                   db='nbufiles',
                                   port=3306,
                                   charset='utf8')
            cur = conn.cursor()  # 获取一个游标
            if time_start == "--" and time_end == "--":
                if select_type == "all":
                    select_content = '全部文件'
                    sql = "select * from %s limit %d, %d"%(table, page_obj.start, page_obj.end-page_obj.start)
                    cur.execute(sql)
                    list = cur.fetchall()
                elif select_type == "duplic":
                    select_content = '重名文件'
                    sql = "select * from %s limit %d, %d"%(table + "_duplic", page_obj.start, page_obj.end-page_obj.start)
                    cur.execute(sql)
                    list = cur.fetchall()
                elif select_type == "duplic_uniqe":
                    select_content = '重名但属性不同文件'
                    sql = "select * from %s where filename in (select filename from %s group by attr,fuser,fgroup,size,date,filename having count(*)=1) limit %d, %d"%(table+"_duplic", table+"_duplic", page_obj.start, page_obj.end-page_obj.start)
                    cur.execute(sql)
                    list = cur.fetchall()
            else:
                sql_time = """str_to_date(date, '%b%d%Y') between str_to_date("{}", '%Y-%m-%d') AND str_to_date("{}", '%Y-%m-%d')""".format(
                    str(time_start), str(time_end))
                if select_type == "all":
                    select_content = '全部文件'
                    sql = "select * from %s where %s limit %d, %d"%(table, sql_time, page_obj.start, page_obj.end-page_obj.start)
                    cur.execute(sql)
                    list = cur.fetchall()
                elif select_type == "duplic":
                    select_content = '重名文件'
                    sql = "select * from %s where %s limit %d, %d"%(table + "_duplic", sql_time, page_obj.start, page_obj.end-page_obj.start)
                    cur.execute(sql)
                    list = cur.fetchall()
                elif select_type == "duplic_uniqe":
                    select_content = '重名但属性不同文件'
                    sql = "select * from %s where (filename in (select filename from %s group by attr,fuser,fgroup,size,date,filename having count(*)=1)) and (%s) limit %d, %d"%(table+"_duplic", table+"_duplic",sql_time, page_obj.start, page_obj.end-page_obj.start)
                    cur.execute(sql)
                    list = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            logging.error(e)
            return self.write('查询出错！')
        # 当前页显示的数据
        current_list = list
        # 当前页显示的页码数相关html代码
        url = '/api/list/%s/'%(tiaojian,)
        str_page = page_obj.page_num_show(url)
        self.render('3.html',
                    database=database,
                    table=table,
                    time_start=time_start,
                    time_end=time_end,
                    select_content=select_content,
                    list_info=current_list,
                    current_page=page_obj.current_page,
                    str_page=str_page)


