from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import csv
import webbrowser
import os

KV = '''
<SearchScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "管控查询系统"
            elevation: 2
        MDTextField:
            id: search_input
            hint_text: "输入企业名称关键词"
            mode: "fill"
            on_text: root.search_enterprise(self.text)
        ScrollView:
            MDList:
                id: results_list

<DetailScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "详情"
            left_action_items: [["arrow-left", lambda x: setattr(root.manager, 'current', 'search')]]
        ScrollView:
            MDBoxLayout:
                id: container
                orientation: 'vertical'
                adaptive_height: True
                padding: "15dp"
                spacing: "10dp"
'''

class SearchScreen(Screen):
    def search_enterprise(self, text):
        self.ids.results_list.clear_widgets()
        if len(text) < 1: return
        app = MDApp.get_running_app()
        unique_names = set()
        for row in app.data:
            name = row.get('企业名称*', '')
            if text in name:
                unique_names.add(name)
        from kivymd.uix.list import OneLineListItem
        for name in sorted(list(unique_names)):
            self.ids.results_list.add_widget(OneLineListItem(
                text=name, on_release=lambda x, n=name: self.go_to_detail(n)))

    def go_to_detail(self, name):
        self.manager.current_enterprise = name
        self.manager.current = 'detail'

class DetailScreen(Screen):
    def on_pre_enter(self):
        self.ids.container.clear_widgets()
        app = MDApp.get_running_app()
        target_name = self.manager.current_enterprise
        rows = [r for r in app.data if r.get('企业名称*') == target_name]
        if not rows: return
        first_row = rows[0]
        self.add_info_row(f"🏢 {target_name}", font_style="H6")
        self.add_info_row(f"📍 地址: {first_row.get('详细地址*', '未知')}")
        gov_phone = first_row.get('县级审核人员电话*', '无')
        from kivymd.uix.button import MDRaisedButton
        btn = MDRaisedButton(text=f"📞 拨打监管电话: {gov_phone}", 
                             on_release=lambda x: webbrowser.open(f"tel:{gov_phone}"))
        self.ids.container.add_widget(btn)
        from kivymd.uix.label import MDLabel
        for row in rows:
            self.ids.container.add_widget(MDLabel(text=f"\n▶ 生产线: {row.get('生产线/工序*', '-')}", bold=True))
            self.ids.container.add_widget(MDLabel(text=f"🔴 红色: {row.get('红色预警_减排措施*', '-')}", theme_text_color="Error"))
            self.ids.container.add_widget(MDLabel(text=f"🟠 橙色: {row.get('橙色预警_减排措施*', '-')}", text_color=(1, .5, 0, 1), theme_text_color="Custom"))
            self.ids.container.add_widget(MDLabel(text=f"🟡 黄色: {row.get('黄色预警_减排措施*', '-')}", text_color=(.7, .7, 0, 1), theme_text_color="Custom"))

    def add_info_row(self, text, font_style="Body1"):
        from kivymd.uix.label import MDLabel
        self.ids.container.add_widget(MDLabel(text=text, font_style=font_style, adaptive_height=True))

class PollutionApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.data = []
        try:
            # 兼容多种编码读取
            for enc in ['utf-8', 'gb18030', 'gbk']:
                try:
                    with open('data.csv', mode='r', encoding=enc) as f:
                        self.data = list(csv.DictReader(f))
                    break
                except: continue
        except: pass
        sm = ScreenManager()
        sm.current_enterprise = ""
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(DetailScreen(name='detail'))
        return Builder.load_string(KV)

if __name__ == '__main__':
    PollutionApp().run()