from datetime import datetime
import math
from lunar_python.util import LunarUtil
from lunar_python import Solar
from datetime import datetime

def calculate_fate(solar_year, solar_month, solar_day, hour, minute, second, gender):
    # 阳历日期转换为阴历日期
    solar = Solar.fromYmdHms(solar_year, solar_month, solar_day, hour, minute, second)
    lunar = solar.getLunar()
    
    # 获取八字信息
    eight_char = lunar.getEightChar()
    
    # 设置流派，此处假设为2
    sect = 2
    eight_char.setSect(sect)

    # 设置 CSS 样式
    style = '''
    <style>
        .eight-char { font-size: 36px; }
        .char-group { display: inline-block; margin-right: 15px; vertical-align: top; }
        .char { display: block; text-align: center; font-weight: bold; }
        .info { font-size: 14px; text-align: center; }
    </style>
    '''

    # 打印基本信息
    print(style)
    print('<div class="eight-char">')
    for char, hide_gan, na_yin in zip(
        [eight_char.getYear(), eight_char.getMonth(), eight_char.getDay(), eight_char.getTime()],
        [eight_char.getYearHideGan(), eight_char.getMonthHideGan(), eight_char.getDayHideGan(), eight_char.getTimeHideGan()],
        [eight_char.getYearNaYin(), eight_char.getMonthNaYin(), eight_char.getDayNaYin(), eight_char.getTimeNaYin()]):
        print(f'<div class="char-group"><span class="char">{char[0]}</span><span class="char">{char[1]}</span><div class="info">{"".join(hide_gan)}</div><div class="info">{na_yin}</div></div>')
    print('</div><br>')
    
    return eight_char


def analyze_five_elements_balance(eight_char):
    # 初始化五行计数器
    elements_count = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
    yin_yang_count = {'阴': 0, '阳': 0}
    
    # 天干地支对应的五行
    gan_zhi = eight_char.getYear() + eight_char.getMonth() + eight_char.getDay() + eight_char.getTime()
    hide_gan = "".join(eight_char.getYearHideGan() + eight_char.getMonthHideGan() + eight_char.getDayHideGan() + eight_char.getTimeHideGan())

    # 统计八字中的五行元素
    for gz in gan_zhi:
        if gz in LunarUtil.WU_XING_GAN:
            elements_count[LunarUtil.WU_XING_GAN.get(gz)] += 1
        elif gz in LunarUtil.WU_XING_ZHI:
            elements_count[LunarUtil.WU_XING_ZHI.get(gz)] += 1

    # 统计藏干中的五行元素
    for cg in hide_gan:
        if cg in LunarUtil.WU_XING_GAN:
            elements_count[LunarUtil.WU_XING_GAN.get(cg)] += 1

    # 统计阴阳
    for gz in gan_zhi:
        if gz in LunarUtil.GAN:
            index = LunarUtil.GAN.index(gz)
            yin_yang = '阳' if index % 2 else '阴'
            yin_yang_count[yin_yang] += 1
    
    for zhi in gan_zhi:
        if zhi in LunarUtil.ZHI:
            index = LunarUtil.ZHI.index(zhi)
            yin_yang = '阳' if index % 2 else '阴'
            yin_yang_count[yin_yang] += 1

    return elements_count, yin_yang_count


def generate_pie_chart(elements_count):
    # 定义五行颜色
    colors = {
        '金': 'rgba(254, 251, 240, 1)',
        '木': 'rgba(60, 94, 101, 1)',
        '水': 'rgba(21, 23, 34, 1)',
        '火': 'rgba(179, 55, 51, 1)',
        '土': 'rgba(232, 195, 85, 1)',
        '阳': 'rgba(225, 225, 225, 1)',
        '阴': 'rgba(30, 30, 30, 1)'
    }

    # 计算总数
    total_count = sum(elements_count.values())

    # SVG绘制参数
    cx, cy, r = 50, 50, 40  # 圆心坐标和半径
    start_angle = 0

    svg_elements = []
    for element, angle in elements_count.items():
        angle = (angle / total_count) * 360  # Recalculate angle based on proportion

        # 特殊处理360度的情况
        if angle >= 360:
            # 绘制一个完整的圆，避免起点和终点重合的问题
            svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{colors[element]}" />')
        else:
            # 计算起始和结束点
            x0 = cx + r * math.sin(math.radians(start_angle))
            y0 = cy - r * math.cos(math.radians(start_angle))
            end_angle = start_angle + angle
            x1 = cx + r * math.sin(math.radians(end_angle))
            y1 = cy - r * math.cos(math.radians(end_angle))

            # 大弧标志（大于180度使用1，否则0）
            large_arc_flag = 1 if angle > 180 else 0

            # 构建SVG路径
            path_d = f"M {cx},{cy} L {x0},{y0} A {r},{r} 0 {large_arc_flag},1 {x1},{y1} Z"
            svg_elements.append(f'<path d="{path_d}" fill="{colors[element]}" />')
        
        start_angle += angle

    # 将所有SVG元素合并成一个SVG
    svg_content = '\n'.join(svg_elements)
    svg = f'<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg">{svg_content}</svg>'

    return svg


print('<p style="margin: 10px 0;">')

now = datetime.now()
eight_char = calculate_fate(now.year, now.month, now.day, now.hour, now.minute, now.second, 1)
elements_count, yin_yang_count = analyze_five_elements_balance(eight_char)

print('<div class="charts" style="display: flex; justify-content: space-around;">')  # 使用flex布局使元素水平排列

# 生成第一个饼图及其注释
elements_chart_svg = generate_pie_chart(elements_count)
print(f'<div style="text-align: center;">')  # 包裹图表和注释的div
print(elements_chart_svg)
print('<div style="margin-top: 10px;">五行分布</div>')  # 注释
print('</div>')

# 生成第二个饼图及其注释
yin_yang_chart_svg = generate_pie_chart(yin_yang_count)
print(f'<div style="text-align: center;">')  # 包裹图表和注释的div
print(yin_yang_chart_svg)
print('<div style="margin-top: 10px;">阴阳分布</div>')  # 注释
print('</div>')

print('</div>')

print('</p>')


