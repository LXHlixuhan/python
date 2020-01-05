from flask import Flask, render_template, request, escape, abort
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

from pyecharts.globals import CurrentConfig
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.components import Table
import plotly as py
import cufflinks as cf
import pandas as pd
import numpy as np
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType, ThemeType
from pyecharts.charts import Bar, Tab, Line, Map, Timeline, Grid,Pie
from pyecharts.commons.utils import JsCode

app = Flask(__name__, template_folder='../templates', static_folder="", static_url_path="")

df = pd.read_csv('high-tech export.csv')
Income = [str(x) for x in df.Income_Group.values]
Region = [str(x) for x in df.Region.values]
high = Income.count('高收入国家')
low = Income.count('低收入国家')
middle_low = Income.count('中低等收入国家')
middle_high = Income.count('中高等收入国家')


def grid_horizontal() -> Grid:
    bar0 = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(['高收入国家', '低收入国家', '中低等收入国家', '中高等收入国家'])
            .add_yaxis("Income_Group", [high, low, middle_low, middle_high])
            .set_global_opts(title_opts=opts.TitleOpts(title="Income_Group", subtitle="2019", pos_left="2%"),
                             legend_opts=opts.LegendOpts(pos_left="20%"))
    )
    bar = (
        Bar()

            .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(
                        # 控制整体的位置
                        left="52%",
                        top="7%",
                    ),
                    children=[

                        # opts.GraphicRect控制方框的显示
                        # 如果不需要方框，去掉该段即可
                        opts.GraphicRect(
                            graphic_item=opts.GraphicItem(
                                z=100,
                                left="center",
                                top="middle",
                            ),
                            graphic_shape_opts=opts.GraphicShapeOpts(
                                width=415, height=440,
                            ),
                            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                fill="#fff",
                                stroke="#555",
                                line_width=2,
                                shadow_blur=8,
                                shadow_offset_x=3,
                                shadow_offset_y=3,
                                shadow_color="rgba(0,0,0,0.3)",
                            )
                        ),
                        # opts.GraphicText控制文字的显示
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(
                                left="center",
                                top="middle",
                                z=100,
                            ),
                            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                # 可以通过jsCode添加js代码，也可以直接用字符串
                                text=JsCode(
                                    "['世界银行是按人均国民总收入对世界各国经济发展水平进行分组。 ',"
                                    "'通常把世界各国分成四组，',"
                                    "'即低收入国家、中等偏下收入国家、',"
                                    "'中等偏上收入国家和高收入国家。',"
                                    "'但以上标准不是固定不变的，而是随着经济的发展不断进行调整。',"
                                    "'中等偏下收入国家和中等偏上收入国家合称为中等收入国家。',"
                                    "'  ',"
                                    "'按世界银行(World Bank)公布的数据，',"
                                    "'2018年的最新收入分组标准为：',"
                                    "'人均国民总收入低于995美元为低收入国家，',"
                                    "'在996至3895美元之间为中等偏下收入国家，',"
                                    "'在3896至12055元之间为中等偏上收入国家，',"
                                    "'高于12055美元为高收入国家。',"
                                    "'  ',"
                                    "'此图所统计的217个经济体中，',"
                                    "'高收入国家79个，低收入国家31个，',"
                                    "'中低等收入国家47个，中高等收入国家60个。',"
                                    "'由此看出，',"
                                    "'全球大多数国家收入水平都处于中等收入水平或者高收入水平，',"
                                    "'只有少部分国家处于低收入水平。',"
                                    "'  ',"
                                    "'美国、日本、英法德以及韩国等为高收入国家；',"
                                    "'俄罗斯、巴西、中国、土耳其、马来西亚等',"
                                    "'目前是中高等收入国家；',"
                                    "'印度、巴基斯坦、越南、菲律宾等国为中低收入国家；',"
                                    "'阿富汗、坦桑尼亚、柬埔寨、尼泊尔、埃塞俄比亚等',"
                                    "'为低收入国家。'].join('\\n')"
                                ),
                                font="14px Microsoft YaHei",
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                    fill="#333"
                                )
                            )
                        )
                    ]
                )
            ],
        )
    )

    grid = (
        Grid()
            .add(bar, grid_opts=opts.GridOpts(pos_left="55%"))
            .add(bar0, grid_opts=opts.GridOpts(pos_right="55%"))
    )
    return grid


def grid_horizontal1() -> Grid:
    bar1 = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(['南亚', '撒哈拉以南非洲地区（不包括高收入）', '欧洲与中亚地区（不包括高收入）',
                        '拉丁美洲与加勒比海地区（不包括高收入）', '东亚与太平洋地区（不包括高收入）', '中东与北非地区（不包括高收入）'])
            .add_yaxis("Region",
                       [Region.count('南亚'),
                        Region.count('撒哈拉以南非洲地区（不包括高收入）'),
                        Region.count('欧洲与中亚地区（不包括高收入）'),
                        Region.count('拉丁美洲与加勒比海地区（不包括高收入）'),
                        Region.count('东亚与太平洋地区（不包括高收入）'),
                        Region.count('中东与北非地区（不包括高收入）')])
            .set_global_opts(title_opts=opts.TitleOpts(title="Region", subtitle="2019", pos_left="2%"),
                             legend_opts=opts.LegendOpts(pos_left="20%"))
    )
    bar = (
        Bar()

            .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(
                        # 控制整体的位置
                        left="52%",
                        top="7%",
                    ),
                    children=[

                        # opts.GraphicRect控制方框的显示
                        # 如果不需要方框，去掉该段即可
                        opts.GraphicRect(
                            graphic_item=opts.GraphicItem(
                                z=100,
                                left="center",
                                top="middle",
                            ),
                            graphic_shape_opts=opts.GraphicShapeOpts(
                                width=400, height=440,
                            ),
                            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                fill="#fff",
                                stroke="#555",
                                line_width=2,
                                shadow_blur=8,
                                shadow_offset_x=3,
                                shadow_offset_y=3,
                                shadow_color="rgba(0,0,0,0.3)",
                            )
                        ),
                        # opts.GraphicText控制文字的显示
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(
                                left="center",
                                top="middle",
                                z=100,
                            ),
                            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                # 可以通过jsCode添加js代码，也可以直接用字符串
                                text=JsCode(
                                    "['根据世界银行(World Bank)统计数据， ',"
                                    "'南亚有8个国家、',"
                                    "'撒哈拉以南非洲地区有48个国家、',"
                                    "'欧洲与中亚地区有58个国家、',"
                                    "'拉丁美洲与加勒比海地区有42个国家、',"
                                    "'东亚与太平洋地区有37个国家、',"
                                    "'中东与北非地区有21个国家。',"
                                    "'  ',"
                                    "'此图除去了世界高收入国家，',"
                                    "'南亚8个国家、撒哈拉以南非洲地区47个国家、',"
                                    "'欧洲与中亚地区有21个国家、',"
                                    "'拉丁美洲与加勒比海地区有25个国家、',"
                                    "'东亚与太平洋地区有24个国家、',"
                                    "'中东与北非地区有13个国家不属于高收入国家。',"
                                    "'  ',"
                                    "'各地区高收入国家占比分别为（四舍五入取整）：',"
                                    "'南亚0%、撒哈拉以南非洲地区98%、',"
                                    "'欧洲与中亚地区36%、',"
                                    "'拉丁美洲与加勒比海地区60%、',"
                                    "'东亚与太平洋地区65%、',"
                                    "'中东与北非地区62%',"
                                    "'  ',"
                                    "'收入与生活水平有一定联系。',"
                                    "'就各地区高收入国家占比，',"
                                    "'可对各地区生活水平做出以下排序（高到低）：',"
                                    "'撒哈拉以南非洲地区>东亚与太平洋地区>',"
                                    "'中东与北非地区>拉丁美洲与加勒比海地区>',"
                                    "'欧洲与中亚地区>南亚'].join('\\n')"
                                ),
                                font="14px Microsoft YaHei",
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                    fill="#333"
                                )
                            )
                        )
                    ]
                )
            ],
        )
    )

    grid1 = (
        Grid()
            .add(bar, grid_opts=opts.GridOpts(pos_left="55%"))
            .add(bar1, grid_opts=opts.GridOpts(pos_right="55%"))
    )
    return grid1


def timeline_map() -> Timeline:
    tl = Timeline()
    for i in range(2007, 2019):
        map0 = (
            Map()
                .add(
                "high-tech export", list(zip(list(df.Country_Name_en), list(df["{}".format(i)]))), "world",
                is_map_symbol_show=False)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}高科技出口".format(i), subtitle="",
                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=18,
                                                                                     font_style="italic")),
                visualmap_opts=opts.VisualMapOpts(min_=0, max_=30),

            )
        )
        tl.add(map0, "{}".format(i))
    return tl


def bar_base() -> Line:
    bar = (
        Bar()

            .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(
                        # 控制整体的位置
                        left="5%",
                        top="10%",
                    ),
                    children=[

                        # opts.GraphicRect控制方框的显示
                        # 如果不需要方框，去掉该段即可
                        opts.GraphicRect(
                            graphic_item=opts.GraphicItem(
                                z=100,
                                left="center",
                                top="middle",
                            ),
                            graphic_shape_opts=opts.GraphicShapeOpts(
                                width=800, height=400,
                            ),
                            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                fill="#fff",
                                stroke="#555",
                                line_width=2,
                                shadow_blur=8,
                                shadow_offset_x=3,
                                shadow_offset_y=3,
                                shadow_color="rgba(0,0,0,0.3)",
                            )
                        ),
                        # opts.GraphicText控制文字的显示
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(
                                left="center",
                                top="middle",
                                z=100,
                            ),
                            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                # 可以通过jsCode添加js代码，也可以直接用字符串
                                text=JsCode(
                                    "['根据世界银行(World Bank)统计数据， ',"
                                    "'  ',"
                                    "'亚洲地区在近十几年来，有着越来越多的国家增加高科技的出口，并且大体上呈现逐年增加的趋势。',"
                                    "'  ',"
                                    "'  ',"
                                    "'欧洲地区，随着大多数经济体的衰落或者停滞不前，',"
                                    "'  ',"
                                    "'欧洲各地的高科技出口都难以取得进展，但仍然处于世界高科技出口的中上行列。',"
                                    "'  ',"
                                    "'  ',"
                                    "'北美洲，得益于美国加拿大等强国，一直都保持的稳定的高科技出口。',"
                                    "'  ',"
                                    "'  ',"
                                    "'南美洲，在金融危机之后，开始出现了高科技出口，并且也是大体上呈现高科技出口国家逐年增加的趋势；',"
                                    "'  ',"
                                    "'  ',"
                                    "'非洲地区是目前世界上高科技出口水平较弱的地区，近十几年来无明显变化趋势，处于世界高科技出口的下游，水平有待加强。',"
                                    "'  ',"
                                    "'  ',"
                                    "'说明经济的不确定性对世界的发展状况息息相关，国际政治格局和贸易关系迅速变化导致全球市场高度不确定，',"
                                    "'  ',"
                                    "'在这样的十几年里，制度的质量似乎是促进繁荣的重要因素。',"
                                    "'  ',"
                                    "'强有力的制度框架为企业投资和创新提供了稳定性，确保了公民更高的生活质量。'].join('\\n')"
                                ),
                                font="14px Microsoft YaHei",
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                    fill="#333"
                                )
                            )
                        )
                    ]
                )
            ],
        )
    )
    return bar


def timeline_pie() -> Timeline:
    attr = Faker.choose()
    tl = Timeline()
    for i in range(2007, 2019):
        pie = (
            Pie(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
                .add(
                "high-tech export",
                list(zip(list(df.Country_Name_en), list(df["{}".format(i)]))),
                rosetype="radius",
                radius=["30%", "85%"],
                label_opts=opts.LabelOpts(is_show=False),
            )
                .set_global_opts(
                title_opts=opts.TitleOpts("高科技出口-{}年数据".format(i)),
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"))
        )
        tl.add(pie, "{}年".format(i))
    return tl


def line_base() -> Line:
    bar = (
        Bar()

            .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(
                        # 控制整体的位置
                        left="5%",
                        top="10%",
                    ),
                    children=[

                        # opts.GraphicRect控制方框的显示
                        # 如果不需要方框，去掉该段即可
                        opts.GraphicRect(
                            graphic_item=opts.GraphicItem(
                                z=100,
                                left="center",
                                top="middle",
                            ),
                            graphic_shape_opts=opts.GraphicShapeOpts(
                                width=800, height=400,
                            ),
                            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                fill="#fff",
                                stroke="#555",
                                line_width=2,
                                shadow_blur=8,
                                shadow_offset_x=3,
                                shadow_offset_y=3,
                                shadow_color="rgba(0,0,0,0.3)",
                            )
                        ),
                        # opts.GraphicText控制文字的显示
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(
                                left="center",
                                top="middle",
                                z=100,
                            ),
                            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                # 可以通过jsCode添加js代码，也可以直接用字符串
                                text=JsCode(
                                    "['根据世界银行(World Bank)统计数据: ',"
                                    "'  ',"
                                    "'2007-2009年中，新加坡、马耳他、冰岛以及哥斯达黎加等国，位列世界高科技出口的前列，高科技出口数量远超其他国家。',"
                                    "'  ',"
                                    "'  ',"
                                    "'2010-2014年中，随着各国家的发展，越来越多的国家开始出口高科技，比如马来西亚，格陵兰岛，尼日尔、哈萨克斯坦等国家，',"
                                    "'  ',"
                                    "'开始增加自己的高科技出口，在世界高科技出口中开始崭露头角。',"
                                    "'  ',"
                                    "'  ',"
                                    "'2015-2018年中，高科技出口的前列国家变化很大，有塞舌尔，阿拉伯联合酋长国，百慕大群岛等国的昙花一现，',"
                                    "'  ',"
                                    "'也有帕劳共和国以及菲律宾等国经久不衰，世界高科技出口的国家朝着多极化方向发展。',"
                                    "'  ',"
                                    "'  ',"
                                    "'表明近十几年来，世界各国都认识到了高科技出口的重要性，',"
                                    "'  ',"
                                    "'  ',"
                                    "'开始利用先进的技术基础设施、商业政策环境以及获得商业融资渠道的便利性等因素，',"
                                    "'  ',"
                                    "'出口本国的高科技产品，以增加国家在世界上的竞争力。'].join('\\n')"
                                ),
                                font="14px Microsoft YaHei",
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                    fill="#333"
                                )
                            )
                        )
                    ]
                )
            ],
        )
    )
    return bar


@app.route("/")
def index():
    tab = Tab()
    tab.add(grid_horizontal(), "Income_Group")
    tab.add(grid_horizontal1(), "Region")
    tab.add(timeline_map(), "map")
    tab.add(bar_base(), "map-data story")
    tab.add(timeline_pie(), "pie")
    tab.add(line_base(), "pie-data story")
    return Markup(tab.render_embed())


if __name__ == "__main__":
    app.run(debug=True, port=8952, use_reloader=False)
