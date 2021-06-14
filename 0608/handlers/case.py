#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .basic import BasicHandler, login


class Case1Handler(BasicHandler):

    @login
    def get(self):
        page = self.get_argument('page', 1)
        extra_info = self.user_ins.fetch_user_info_by_nickname(self.current_user)
        data_info_list = self.case_ins.fetch_case3_list(page)
        total_page = (self.case_ins.count_case3_num() + self.case_ins.count - 1)/self.case_ins.count
        self.render('case1.html', extra_info=extra_info, total_page=int(total_page), cur_page=int(page),
                    data_info_list=data_info_list)


class Case1CreateHandler(BasicHandler):
    @login
    def get(self):
        import xlrd
        xlsx = xlrd.open_workbook('./sourcedata/covdataadddate.xlsx')
        sheet = xlsx.sheets()[2]
        for i in range(1, sheet.nrows):
            swap = []
            for j in range(len(sheet.row_values(i))):
                if j == 1:
                    swap.append(int(sheet.row_values(i)[j]))
                else:
                    swap.append(sheet.row_values(i)[j])
            self.case_ins.insert_case3_data(tuple(swap))
        return self.write("添加新数据成功!!")


class SearchCase1Handler(BasicHandler):

    @login
    def get(self):
        p = self.get_argument("p", None)
        if not p:
            return
        extra_info = self.user_ins.fetch_user_info_by_nickname(self.current_user)
        tmp_list = self.case_ins.search_case3_info_by_p(p)
        data_info_list = list()
        for item in tmp_list:
            data_info_list.append(item)
        self.render('case1.html', extra_info=extra_info, total_page=1, cur_page=1,
                    data_info_list=data_info_list)


class DelCase1Handler(BasicHandler):
    @login
    def post(self):
        id = self.get_argument("data_id", "")
        if not id:
            return self.write("要删除的数据不存在!!")
        self.case_ins.del_case3_data_by_id(id)
        return self.write("删除数据成功!!")


class EditCase1Handler(BasicHandler):
    @login
    def get(self):
        id = self.get_argument("data_id", "")
        extra_info = self.user_ins.fetch_user_info_by_nickname(self.current_user)
        data_info_list = self.case_ins.search_case3_info_by_id(id)
        self.render('case2.html', extra_info=extra_info, total_page=1, cur_page=1,
                    data_info_list=data_info_list)

    def post(self):
        id = self.get_argument("data_id", "")
        province = self.get_argument("province")
        confirm = self.get_argument("confirm")
        dead = self.get_argument("dead")
        heal = self.get_argument("heal")
        newconfirm = self.get_argument("newconfirm")
        newheal = self.get_argument("newheal")
        newdead = self.get_argument("newdead", '')
        desp = self.get_argument("desp", '')
        self.case_ins.update_case3_by_id(id, (province,confirm, dead, heal, newconfirm, newheal, newdead, desp))
        return self.write("修改数据成功,请手动返回数据管理页面!!")

