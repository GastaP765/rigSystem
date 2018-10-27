import maya.cmds as mc

xyz = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
jnt = list(range(0))
whi = list(range(0))
jnt_trs = 0
tar_trs = 0
num = 0
exi = 0
atn = 0

def definition():
	global jnt, tar, num, k, swt
	k = 0
	swt = 0
	jnt = mc.ls(sl=True)
	num = mc.intField(txt, q=True, v=True)
	calculation()

def calculation():
	global jnt, tar, atr, jnt_trs, tar_trs, num, atn, swt

	tar = mc.listRelatives('{}'.format(jnt[k]))
	atr = mc.listAttr(tar[0], c=True)
	jnt_trs = mc.getAttr('{}.worldMatrix[0]'.format(jnt[k]))
	tar_trs = mc.getAttr('{}.translateX'.format(tar[0]))
	if num > 0:
		tar_trs = tar_trs / num
		atn = 1.0000 / num
	mc.select(cl=True)

	nameEdit()

def nameEdit():
	global nme, swt

	nme = list(range(0))
	nme.append(jnt[k].split('_'))
	if swt != 0:
		create();
	else:
		check()

def check():
	global jnt, tar, exi, tar_trs, num
	print 'check'

	rem = list(range(0))
	exi = 0
	ajo = mc.ls(typ='joint')
	cnt = len(ajo)
	for i in range(cnt):
		if nme[0][0] + '_weighted' in ajo[i]:
			rem.append(ajo[i])
			exi = exi + 1

	if exi >= 1:
		for i in range(exi):
			mc.setAttr('{}.translateX'.format(rem[i]), tar_trs*(i))

	if num < exi:
		for i in range(exi - num):
			rmv = exi - i - 1
			mc.delete('{}'.format(rem[rmv]))
			if 'weight{}L'.format(xyz[rmv]) in atr:
				print tar[0]
				mc.deleteAttr('{0}.weight{1}{2}'.format(tar[0], xyz[rmv], nme[0][1]))

		next()
	else:
		create()

def create():
	global jnt, tar, atr, wgt, exi, nme, atn
	wgt = list(range(0))

	for i in range(num):
		f = i + exi
		cjo = mc.joint(n='{0}_weighted_{1}{2}'.format(nme[0][0], xyz[f], nme[0][1]), rad=0.3, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
		pbd = mc.createNode('pairBlend', n='{0}_ifTwistWeightedBlend_{1}{2}'.format(nme[0][0],xyz[f], nme[0][1]))
		if 'weight{0}{1}'.format(xyz[f], nme[0][1]) not in atr:
			mc.addAttr('{}'.format(tar[0]), ln='weight{0}{1}'.format(xyz[f], nme[0][1]), min=0, max=1, dv=1)
		mc.parent('{}'.format(cjo), '{}'.format(jnt[k]))
		mc.setAttr('{}.translateX'.format(cjo), tar_trs*(f))
		mc.setAttr('{}.jointOrient'.format(cjo), 0, 0, 0)
		mc.setAttr('{0}.weight{1}{2}'.format(tar[0], xyz[f], nme[0][1]), atn*i)
		mc.connectAttr('{0}.weight{1}{2}'.format(tar[0], xyz[f], nme[0][1]), '{}.weight'.format(pbd))
		mc.connectAttr('{}.rotateX'.format(tar[0]), '{}.inRotate2.inRotateX2'.format(pbd))
		mc.connectAttr('{}.outRotateX'.format(pbd), '{}.rotateX'.format(cjo))
		mc.select(cl=True)
		wgt.append(cjo)
		if f == num:
			break

	if exi >= 1:
		mc.delete('{}'.format(cjo))
		wgt.remove(cjo)
	next()

def next():
	global k, jnt, swt, rim
	row = len(jnt) - 1
	if swt != 0:
		if rim < swt - 1:
			mirrorCnt()
	elif k < row:
		k = k + 1
		calculation()


def mirror():
	global mrj, jnt, mnt, swt, rim, mir, whi, k
	mrj = list(range(0))
	jnt = list(range(0))
	rim = 0
	swt = 0
	f = 0
	k = 0

	mir = mc.ls(typ='joint')
	mnt = len(mir)
	for i in range(mnt):
		if 'weighted_AL' in mir[i]:
			whi = mc.listRelatives('{}'.format(mir[i]), p=True)
			spr = whi[0]
			con = spr.strip('_L')
			mrj.append(con)
			jnt.append(con + '_R')
			swt = swt + 1

	mirrorNum()

def mirrorCnt():
	global rim, k
	rim = rim + 1
	k = k + 1
	mirrorNum()

def mirrorNum():
	global mrj, num, mnt, mir, whi
	num = 0

	for i in range(mnt):
		if mrj[k] + '_weighted' in mir[i]:
			num = num + 1

	mc.select('{}'.format(jnt[k]))
	calculation()


if mc.window('createWeighted', exists=True):
	mc.deleteUI('createWeighted')

createWin = mc.window('createWeighted', t='createWeighted', w=300, h=175)
mc.columnLayout(adj=True)
mc.rowLayout(nc=2, w=300)
mc.text('Create Weighted')
txt = mc.intField('txt', v=0, w=175)
mc.setParent('..')

mc.rowLayout(nc=2, w=300)
mc.button(l='weighted', w=150, h=40, c='definition()')
mc.button(l='mirror', w=150, h=40, c='mirror()')
mc.setParent('..')


mc.showWindow(createWin)
