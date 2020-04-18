import random

def get_random_rgb():
    """
        Function to generate rangom rgb values 
        two random values increase the etropy
        returns: rgb values as a tuple 
    """
    r = random.randint(0, 255) 
    g = random.randint(0, 255) 
    b = random.randint(0, 255) 
    rgb = (r,g,b)
    return rgb

def autolabel(ax, dtype=int):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for bar in ax.patches:
        if dtype==float:
            height = str(bar.get_height())[:4]
        else:
            height = str(int(bar.get_height()))
        ax.annotate(height,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')