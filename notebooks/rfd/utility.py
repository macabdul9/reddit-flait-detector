import random


title_font = {"fontsize":20}
label_font = {"fontsize":16}
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

# Function to change the bar plot bar width
def change_width(ax, new_value) :
    """
        ax: axes
        new_value: new width
    """
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)

def autolabel(ax, dtype=int):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for bar in ax.patches:
        if dtype==float:
            text = str(bar.get_height())[:4]
        else:
            text = str(int(bar.get_height()))
        ax.annotate(text,
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


# Function to iterate over month
def month_year_iter(start_month, start_year, end_month, end_year, dfs):
    '''
        start_month: start month
        start_year: start year
        end_month: end month
        end_year: end year

        returns: iterator from start till end
        Note: All value should be numerical
    '''
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for i, ym in enumerate(range(ym_start, ym_end)):
        y, m = divmod( ym, 12)
        yield y, m+1, dfs[i]
