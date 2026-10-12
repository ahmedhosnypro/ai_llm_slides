from PIL import ImageFont
LIB='/usr/share/fonts/liberation/'
def fit(text, target_w, fonts, lo=8, hi=60):
    best=None
    for name,path in fonts.items():
        # binary search size so getlength == target
        lo_, hi_ = lo, hi
        for _ in range(40):
            mid=(lo_+hi_)/2
            f=ImageFont.truetype(path, int(round(mid*4)))  # 4x for precision
            w=f.getlength(text)/4.0
            if w<target_w: lo_=mid
            else: hi_=mid
        best=(name, round((lo_+hi_)/2,2))
        print(f'  {name}: {best[1]}pt -> advance {ImageFont.truetype(path,int(round(best[1]*4))).getlength(text)/4.0:.1f} (target {target_w})')
    return best
serif_b = LIB+'LiberationSerif-Bold.ttf'
sans_b  = LIB+'LiberationSans-Bold.ttf'
sans_r  = LIB+'LiberationSans-Regular.ttf'
serif_r = LIB+'LiberationSerif-Regular.ttf'
fonts={'SerifBold':serif_b,'SansBold':sans_b}
print('title1 (target 780, x57..837):')
fit('Update the weights by moving in the negative direction of the', 780, fonts)
print('title2 (target 810, x73..883):')
fit('Gradient of the Loss function with respect  to model weights', 810, fonts)
print('Let (target 35):')
fit('Let', 35, fonts)
print('then (target 48):')
fit('then', 48, fonts)
print('note1 "(For Sigmoid Function)" (target 178):')
fit('(For Sigmoid Function)', 178, {'SerifBold':serif_b,'SansBold':sans_b,'SerifReg':serif_r,'SansReg':sans_r})
print('note2 "(Error at Output layer ONLY)" (target 222):')
fit('(Error at Output layer ONLY)', 222, {'SerifBold':serif_b,'SansBold':sans_b,'SerifReg':serif_r,'SansReg':sans_r})
