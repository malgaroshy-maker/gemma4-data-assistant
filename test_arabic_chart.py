import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import arabic_reshaper
from bidi.algorithm import get_display
import os

# Register font
font_path = r"C:\Users\masal\AppData\Local\Microsoft\Windows\Fonts\NotoSansArabic-VariableFont_wdth,wght.ttf"
fm.fontManager.addfont(font_path)
prop = fm.FontProperties(fname=font_path)
family = prop.get_name()
plt.rcParams["font.family"] = family


def process_text(text):
    return get_display(arabic_reshaper.reshape(text))


# Create chart with Arabic text
fig, ax = plt.subplots()
ax.bar(["A", "B", "C"], [10, 20, 15])
ax.set_title("المبيعات حسب القسم")
ax.set_xlabel("القسم")
ax.set_ylabel("المتوسط")

# Draw first
fig.canvas.draw()

# Process ALL text elements
for ax_obj in fig.get_axes():
    title = ax_obj.get_title()
    if title:
        ax_obj.set_title(process_text(title))
    xlabel = ax_obj.get_xlabel()
    if xlabel:
        ax_obj.set_xlabel(process_text(xlabel))
    ylabel = ax_obj.get_ylabel()
    if ylabel:
        ax_obj.set_ylabel(process_text(ylabel))
    # Tick labels
    for tick in ax_obj.get_xticklabels():
        txt = tick.get_text()
        if txt:
            tick.set_text(process_text(txt))
    for tick in ax_obj.get_yticklabels():
        txt = tick.get_text()
        if txt:
            tick.set_text(process_text(txt))

# Redraw
fig.canvas.draw()

plt.savefig("test_arabic_final.png", dpi=100, bbox_inches="tight")
print("Chart saved successfully")
