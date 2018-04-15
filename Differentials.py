def DifferentialCheck(diff, prevobj, obj, data):
    AllowDecrease = False
    d = obj - prevobj
    diff.AddObj(d)
    Avg = diff.Av
    # print('Length of list:', len(diff.DL),'\nAverage:', Avg,'\nActual difference', d,'\n  DL:', diff.DL)
    if Avg >= d * data.params['Beta']:
        AllowDecrease = True

    return AllowDecrease
