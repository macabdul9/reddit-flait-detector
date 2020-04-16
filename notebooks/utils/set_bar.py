def autolabel(ax, dtype=int):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for bar in ax.patches:
        height = dtype(bar.get_height())
        ax.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')