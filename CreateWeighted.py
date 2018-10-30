import maya.cmds as mc

xyz = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
swt = 0
def preparation():
    global sdv, sst, tar, atn, atr, many, tar_trs, sst_mat

    many = mc.intField(num, q=True, v=True)

    sst = mc.textField(stt, q=True, text=True)
    tar = mc.textField(end, q=True, text=True)
    sdv = mc.textField(drv, q=True, text=True)
    #sst_mat = mc.getAttr('{}.wm'.format(sst))
    tar_trs = mc.getAttr('{}.tx'.format(tar))
    atr = mc.listAttr(sdv, c=True)
    if many != 0:
        tar_trs = tar_trs / many
        atn = 1.0000 / many
    else:
        tar_trs = 0
    
    check()

def check():
    global atn, many, sdv, tar_trs, atr, exi, chk

    chk = mc.listRelatives('{}'.format(sdv), p=True)
    kep = mc.listRelatives('{}'.format(chk[0]))
    exi = 0

    if 'weighted' in '{}'.format(kep):
        cnt = len(kep)
        rem = list(range(0))

        for i in range(cnt):
            if 'weighted' in kep[i]:
                rem.append(kep[i])

        exi = len(rem)
    if 'weight' in '{}'.format(atr):
        atr_cnt = len(atr)
        wgt_atr = list(range(0))
        for i in range(atr_cnt):
            if 'weight' in atr[i]:
                wgt_atr.append(atr[i])

    if exi >= 1:
        for i in range(exi):
            mc.setAttr('{}.tx'.format(rem[i]), tar_trs*(i))

    if many < exi:
        for i in range(exi - many):
            rmv = exi - i - 1
            mc.delete(rem[rmv])
            if 'weight{}'.format(xyz[rmv]) in wgt_atr[rmv]:
                mc.deleteAttr('{0}.{1}'.format(sdv, wgt_atr[rmv]))
            
        mirror()

    nameEdit()

def nameEdit():
    global nme, ene

    nme = sdv
    ene = ''
    if '_L' in sdv:
        nme = sdv.replace('_L', '')
        ene = 'L'
    if '_R' in sdv:
        nme = sdv.replace('_R', '')
        ene = 'R'

    create()

def create():

    wgt = list(range(0))
    for i in range(many):
        f = i + exi

        cjo = mc.joint(n='{0}_weighted_{1}{2}'.format(nme, xyz[f], ene), rad=0.3, p=(0, 0, 0))
        pbd = mc.createNode('pairBlend', n='{0}_ifTwistWeightedBlend_{1}{2}'.format(sdv,xyz[f], ene))
        if 'weight{0}{1}'.format(xyz[f], ene) not in atr:
            mc.addAttr('{}'.format(sdv), ln='weight{0}{1}'.format(xyz[f], ene), min=0, max=1, dv=1)
        mc.parent('{}'.format(cjo), '{}'.format(chk[0]))
        mc.setAttr('{}.translate'.format(cjo), 0, 0, 0)
        mc.setAttr('{}.translateX'.format(cjo), tar_trs*(f))
        mc.setAttr('{}.jointOrient'.format(cjo), 0, 0, 0)
        mc.setAttr('{0}.weight{1}{2}'.format(sdv, xyz[f], ene), atn*f)
        mc.connectAttr('{0}.weight{1}{2}'.format(sdv, xyz[f], ene), '{}.weight'.format(pbd))
        mc.connectAttr('{}.rotateX'.format(sdv), '{}.inRotate2.inRotateX2'.format(pbd))
        mc.connectAttr('{}.outRotateX'.format(pbd), '{}.rotateX'.format(cjo))
        mc.select(cl=True)
        wgt.append(cjo)
        if f == many:
            break

    if exi >= 1:
        mc.delete('{}'.format(cjo))
        wgt.remove(cjo)

    mirror()

def mirror():
    global tar_trs, sdv, j, swt

    if swt == 0:
        return
    elif swt == 1:
        if j == len(coa):
            return

    cob = mc.listRelatives(coa[j], p=True)
    coc = mc.listRelatives(cob[0])

    for i in coc:
        if 'weighted' in '{}'.format(i):
            if 'weighted_BL' in '{}'.format(i):
                tar_trs = mc.getAttr('{}.tx'.format(i))
        else:
            sdv = i.replace('_L', '_R')
            print sdv

    j = j + 1
    check()

def mirrorswt():
    global swt, coa, k, j
    swt = 1
    con = list(range(0))
    coa = list(range(0))
    k = 0
    j = 0
    jnt = mc.ls(typ='joint')

    for i in jnt:
        if 'weighted' in '{}'.format(i):
            con.append(i)

    for i in con:    
        if 'weighted_AL' in '{}'.format(i):
            coa.append(i)
            k = k + 1 

    print con
    mirror()

def set_drv():
    global sdv
    sub = mc.ls(sl=True)
    sdv = mc.textField(drv, e=True, text='{}'.format(sub[0]))

def stt_set():
    global sst, tar
    sub = mc.ls(sl=True)
    con = mc.listRelatives(sub[0])
    sst = mc.textField(stt, e=True, text='{}'.format(sub[0]))
    tar = mc.textField(end, e=True, text='{}'.format(con[0]))

def end_set():
    global sst, tar
    sub = mc.ls(sl=True)
    con = mc.listRelatives(sub[0], p=True)
    sst = mc.textField(stt, e=True, text='{}'.format(con[0]))
    tar = mc.textField(end, e=True, text='{}'.format(sub[0]))


if mc.window('createWeighted', exists=True):
    mc.deleteUI('createWeighted')

createWin = mc.window('createWeighted', t='createWeighted', w=300, h=200)
mc.columnLayout(adj=True)

mc.frameLayout(l='weighted')
mc.rowLayout(nc=2, cat=[(1, 'left', 0), (2, 'left', 5)])
mc.text(' Create many weighted : ')
num = mc.intField('num', w=145)
mc.setParent('..')
mc.rowLayout(nc=3, cat=[(1, 'left', 0), (2, 'left', 5)])
mc.text(' set drover :')
drv = mc.textField('drv', w=170)
mc.button(l='set', w=50, h=20, c='set_drv()')
mc.setParent('..')

mc.frameLayout(l='Range to create weighted')
mc.rowLayout(nc=3, cat=[(1, 'left', 0), (2, 'left', 5)])
mc.text('       start :')
stt = mc.textField('stt', w=170)
mc.button(l='set', w=50, h=20, c='stt_set()')
mc.setParent('..')
mc.rowLayout(nc=3, cat=[(1, 'left', 0), (2, 'left', 5)])
mc.text('         end :')
end = mc.textField('end', w=170)
mc.button(l='set', w=50, h=20, c='end_set()')
mc.setParent('..')

mc.rowLayout(nc=2, w=300)
mc.button(l='weighted', w=150, h=40, c='preparation()')
mc.button(l='mirror', w=150, h=40, c='mirrorswt()')
mc.setParent('..')


mc.showWindow(createWin)
